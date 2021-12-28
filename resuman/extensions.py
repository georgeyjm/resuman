from flask_caching import Cache
from flask_login import LoginManager

login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'simple'})
