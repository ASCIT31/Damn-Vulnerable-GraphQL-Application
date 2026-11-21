import base64
import uuid
import os
from config import WEB_UPLOADDIR
from jwt import decode
from werkzeug.utils import secure_filename
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
  return decode(token, options={"verify_signature":False, "verify_exp":False}).get('identity')

def save_file(filename, text):
  """Write an uploaded paste inside WEB_UPLOADDIR only.

  The client filename is reduced to a safe basename and the resolved path
  must stay inside the upload directory. Raises ValueError otherwise.
  """
  safe_name = secure_filename(filename or '')
  if not safe_name:
    raise ValueError('Invalid filename')
  upload_dir = os.path.realpath(WEB_UPLOADDIR)
  destination = os.path.realpath(os.path.join(upload_dir, safe_name))
  if os.path.dirname(destination) != upload_dir:
    raise ValueError('Invalid filename')
  with open(destination, 'w') as f:
    f.write(text)
  return text

def is_level_easy():
  mode = ServerMode.query.one()
  return mode.hardened == False

def is_level_hard():
  mode = ServerMode.query.one()
  return mode.hardened == True

def set_mode(mode):
  mode = ServerMode.set_mode(mode)
