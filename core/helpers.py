import base64
import uuid
import os
import subprocess
from config import WEB_UPLOADDIR
from jwt import decode
from core.models import ServerMode

def run_cmd(cmd):
  return os.popen(cmd).read()

def run_argv(argv, timeout=10):
  """Run a fixed program without a shell, so no user input is ever interpreted by /bin/sh."""
  try:
    completed = subprocess.run(argv, shell=False, capture_output=True, text=True, timeout=timeout, check=False)
  except (OSError, subprocess.SubprocessError):
    return 'Command failed.'
  return completed.stdout

def initialize():
  return run_cmd('python3 setup.py')

def generate_uuid():
  return str(uuid.uuid4())[0:6]

def decode_base64(text):
  return base64.b64decode(text).decode('utf-8')

def get_identity(token):
  return decode(token, options={"verify_signature":False, "verify_exp":False}).get('identity')

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
