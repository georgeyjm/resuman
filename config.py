import os

class Config:
    '''Base configurations.'''

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED = True
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300


class DevelopmentConfig(Config):
    '''Development configurations.'''

    ENV = 'development'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ALLOWED_ORIGINS = []


class ProductionConfig(Config):
    '''Production configurations.'''

    ENV = 'production'
    TESTING = False
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_ORIGINS = []


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
