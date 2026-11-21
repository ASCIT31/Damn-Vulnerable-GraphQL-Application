import config
import random
import ipaddress
import re
import socket
import time

from urllib.parse import quote

from core import helpers

def simulate_load():
  loads = [200, 300, 400, 500]
  count = 0
  limit = random.choice(loads)
  while True:
    time.sleep(0.1)
    count += 1
    if count > limit:
      return

def get_network(addr, style='cidr'):
  try:
    if style == 'cidr':
      return str(ipaddress.ip_network(addr))
    else:
      return str(ipaddress.ip_network(addr).netmask)
  except:
    return 'Could not identify network'

def is_port(port):
  if isinstance(port, int):
    if port >= 0 and port <= 65535:
      return True
  return False

def allowed_cmds(cmd):
  if helpers.is_level_easy():
    return True
  elif helpers.is_level_hard():
    if cmd.startswith(('echo', 'ps' 'whoami', 'tail')):
      return True
  return False

def strip_dangerous_characters(cmd):
  if helpers.is_level_easy():
    return cmd
  elif helpers.is_level_hard():
    return cmd.replace(';','').replace('&', '')
  return cmd

def check_creds(username, password, real_password):
  if username != 'admin':
    return (False, 'Username is invalid')

  if password == real_password:
    return (True, 'Password Accepted.')

  return (False, 'Password Incorrect')

def on_denylist(query):
  normalized_query = ''.join(query.split())
  queries = [
    'query{systemHealth}',
    '{systemHealth}'
  ]

  if normalized_query in queries:
    return True
  return False

def operation_name_allowed(operation_name):
  opnames_allowed = ['CreatePaste', 'CreateUser', 'EditPaste', 'getPastes', 'UploadPaste', 'ImportPaste']
  if operation_name in opnames_allowed:
    return True
  return False

def depth_exceeded(depth):
  depth_allowed = config.MAX_DEPTH
  if depth > depth_allowed:
    return True
  return False

def cost_exceeded(qry_fields):
  total_cost_allowed = config.MAX_COST
  total_query_cost   = 0

  field_cost = {
    'systemUpdate':10,
  }

  for field in qry_fields:
    if field in field_cost:
      total_query_cost += field_cost[field]

  if total_query_cost > total_cost_allowed:
    return True

  return False

IMPORT_ALLOWED_SCHEMES = ('http', 'https')
IMPORT_ALLOWED_PORTS = (80, 443)
IMPORT_MAX_BYTES = 64 * 1024
_HOSTNAME_RE = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?')

def build_safe_import_url(scheme, host, port, path):
  """Validate an importPaste destination and return the URL to fetch.

  Only http/https on the standard ports are allowed, and every address the
  host resolves to must be a public (globally routable) address, which blocks
  loopback, RFC1918, link-local (cloud metadata) and other internal targets.
  """
  scheme = (scheme or '').lower()
  if scheme not in IMPORT_ALLOWED_SCHEMES:
    raise ValueError('Scheme not allowed')
  if port is None:
    port = 443 if scheme == 'https' else 80
  if not is_port(port) or port not in IMPORT_ALLOWED_PORTS:
    raise ValueError('Port not allowed')
  if not isinstance(host, str) or not _HOSTNAME_RE.fullmatch(host):
    raise ValueError('Invalid host')
  try:
    addresses = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
  except (socket.gaierror, UnicodeError):
    raise ValueError('Host does not resolve')
  if not addresses:
    raise ValueError('Host does not resolve')
  for address in addresses:
    ip = ipaddress.ip_address(address[4][0])
    if not ip.is_global:
      raise ValueError('Destination not allowed')
  path = path if isinstance(path, str) else '/'
  if not path.startswith('/'):
    path = '/' + path
  return '{}://{}:{}{}'.format(scheme, host, port, quote(path, safe="/-._~%?=&"))
