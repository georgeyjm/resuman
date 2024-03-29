from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from werkzeug.security import check_password_hash

from resuman.extensions import login_manager


db = SQLAlchemy()


class User(db.Model, UserMixin):
    '''Model for the users table.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, name={self.name!r})'

    def authenticate(self, password):
        '''Checks if provided password matches stored password.'''
        return check_password_hash(self.password, password)
    
    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


class Info(db.Model):
    '''Model for the infos table.'''

    __tablename__ = 'infos'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}: {self.key!r}={self.value!r})'


class Resume(db.Model):
    '''Model for the resumes table.'''

    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    info_ids = db.Column(ARRAY(db.Integer), nullable=False, default=[])
    section_ids = db.Column(ARRAY(db.Integer), nullable=False, default=[])

    @property
    def infos(self):
        return list(filter(lambda x: x is not None, [Info.query.get(i) for i in self.info_ids]))

    @property
    def sections(self):
        return list(filter(lambda x: x is not None, [Section.query.get(i) for i in self.section_ids]))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, name={self.name!r})'


class Section(db.Model):
    '''Model for the sections table.'''

    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(16), nullable=False, default='basic')
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    entry_ids = db.Column(ARRAY(db.Integer), nullable=False, default=[])

    @property
    def entries(self):
        return list(filter(lambda x: x is not None, [Entry.query.get(i) for i in self.entry_ids]))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, name={self.name!r}, type={self.type!r})'


class Entry(db.Model):
    '''Model for the entries table.'''

    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, default='')
    subtitle = db.Column(db.String(128), nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    start_year = db.Column(db.Integer, nullable=False)
    start_month = db.Column(db.Integer, nullable=True)
    end_year = db.Column(db.Integer, nullable=True)
    end_month = db.Column(db.Integer, nullable=True)
    is_ongoing = db.Column(db.Boolean, nullable=False, default=False)
    is_expected = db.Column(db.Boolean, nullable=False, default=False)
    description_ids = db.Column(ARRAY(db.Integer), nullable=False, default=[])

    @property
    def descriptions(self):
        return list(filter(lambda x: x is not None, [Description.query.get(i) for i in self.description_ids]))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, name={self.name!r})'


class Description(db.Model):
    '''Model for the descriptions table.'''

    __tablename__ = 'descriptions'

    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'))
    content = db.Column(db.String(512))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'


# class History(db.Model):
#     '''Model for the histories table (note that history functionality is still WIP).'''
#
#     __tablename__ = 'histories'
#
#     id = db.Column(db.Integer, primary_key=True)
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}({self.id})'
