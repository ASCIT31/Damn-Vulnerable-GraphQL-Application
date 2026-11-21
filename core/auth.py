"""Request authentication helpers.

Identity is taken only from a signed access token sent in the
`Authorization: Bearer <token>` header. The signature, algorithm,
expiry and token type are all verified; an invalid token is treated
as anonymous.
"""
import jwt

from flask import request
from graphql import GraphQLError

from app import app

ADMIN_USERNAME = 'admin'


def bearer_token():
  header = request.headers.get('Authorization', '')
  if header[:7].lower() == 'bearer ':
    return header[7:].strip() or None
  return None


def decode_access_token(token):
  claims = jwt.decode(
    token,
    app.config['JWT_SECRET_KEY'],
    algorithms=['HS256'],
    options={'require': ['exp', 'identity']}
  )
  if claims.get('type') != 'access':
    raise jwt.InvalidTokenError('Not an access token')
  return claims.get('identity')


def current_identity():
  token = bearer_token()
  if not token:
    return None
  try:
    return decode_access_token(token)
  except jwt.PyJWTError:
    return None


def is_admin(identity):
  return identity == ADMIN_USERNAME


def require_login():
  identity = current_identity()
  if not identity:
    raise GraphQLError('Authentication required.')
  return identity


def require_admin():
  identity = require_login()
  if not is_admin(identity):
    raise GraphQLError('Administrator privileges required.')
  return identity
