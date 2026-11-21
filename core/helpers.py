import base64
import uuid
import os
from config import WEB_UPLOADDIR
from jwt import decode
from flask import current_app
from core.models import ServerMode

def run_cmd(cmd):
  return os.popen(cmd).read()

def initialize():
  return run_cmd('python3 setup.py')

def generate_uuid():
  return str(uuid.uuid4())[0:6]

def decode_base64(text):
  return base64.b64decode(text).decode('utf-8')

def get_identity(token):
  # Verify signature, pin the algorithm (rejects alg=none and key confusion) and enforce expiry.
  claims = decode(
    token,
    current_app.config['JWT_SECRET_KEY'],
    algorithms=['HS256'],
    options={'require': ['exp', 'identity']}
  )
  if claims.get('type') != 'access':
    raise ValueError('Not an access token')
  return claims.get('identity')

def save_file(filename, text):
  try:
    f = open(WEB_UPLOADDIR + filename, 'w')
    f.write(text)
    f.close()
  except Exception as e:
    text = str(e)
  return text

def is_level_easy():
  mode = ServerMode.query.one()
  return mode.hardened == False

def is_level_hard():
  mode = ServerMode.query.one()
  return mode.hardened == True

def set_mode(mode):
  mode = ServerMode.set_mode(mode)
