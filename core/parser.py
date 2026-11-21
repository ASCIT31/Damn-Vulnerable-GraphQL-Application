from graphql.language import ast


def get_operation_depth(operation, fragments=None):
  """Maximum field nesting of an operation, computed on the parsed AST.

  Fragment spreads and inline fragments are expanded, so the depth limit
  cannot be bypassed by formatting tricks or by hiding nesting in fragments.
  """
  return _selection_depth(getattr(operation, 'selection_set', None), fragments or {}, frozenset())


def _selection_depth(selection_set, fragments, visited):
  if selection_set is None:
    return 0
  deepest = 0
  for selection in selection_set.selections:
    if isinstance(selection, ast.Field):
      depth = 1 + _selection_depth(selection.selection_set, fragments, visited)
    elif isinstance(selection, ast.InlineFragment):
      depth = _selection_depth(selection.selection_set, fragments, visited)
    elif isinstance(selection, ast.FragmentSpread):
      name = selection.name.value
      fragment = fragments.get(name)
      if fragment is None or name in visited:
        depth = 0
      else:
        depth = _selection_depth(fragment.selection_set, fragments, visited | {name})
    else:
      depth = 0
    deepest = max(deepest, depth)
  return deepest


def get_fields_from_query(q):
  fields = [k for k in q.split() if k.isalnum()]
  return fields

def get_depth(q):
  depth = 0
  for i in q.split():
    if i == '{':
      depth += 1
  return depth
