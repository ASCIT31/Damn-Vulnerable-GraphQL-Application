import os

# SQLAlchemy
SQLALCHEMY_FILE = f"{os.getcwd()}/dvga.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLALCHEMY_FILE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask
WEB_HOST  = os.environ.get('WEB_HOST', '127.0.0.1')
WEB_PORT  = os.environ.get('WEB_PORT', 5013)
WEB_DEBUG = os.environ.get('WEB_DEBUG', True)
WEB_UPLOADDIR = 'pastes/'

# Request and paste size limits
MAX_REQUEST_BYTES = 256 * 1024
MAX_PASTE_TITLE_LENGTH = 200
MAX_PASTE_CONTENT_LENGTH = 10 * 1024

# GraphQL Security Protection
MAX_DEPTH = 8
MAX_COST = 10