import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
ASSETS_DEBUG = False

CACHE_TYPE = 'memcached'
CACHE_KEY_PREFIX = 'c2o_dev'

ADMINS = frozenset(['matteson@obstructures.org'])
SECRET_KEY = 'REPLACEME'

SQLALCHEMY_DATABASE_URI = 'postgresql://chicagoclimateonline@localhost/chicagoclimateonline_001D'
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'REPLACEME'

SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = 'REPLACEME'
SECURITY_TRACKABLE = True
SECURITY_RECOVERABLE = True
SECURITY_POST_LOGIN_VIEW = '/admin'
SECURITY_POST_LOGOUT_VIEW = '/login'

UPLOADS_DEFAULT_URL = '/static/images/'
UPLOADS_DEFAULT_DEST = os.path.join(_basedir, 'obstructures', 'static', 'images')

# RECAPTCHA_USE_SSL = False
# RECAPTCHA_PUBLIC_KEY = 'REPLACEME'
# RECAPTCHA_PRIVATE_KEY = 'REPLACEME'
# RECAPTCHA_OPTIONS = {'theme': 'white'}