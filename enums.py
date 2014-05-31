#!/usr/bin/python
#
# enums.
#
#   Color = enums.new('Color = RED GREEN BLUE ANY', wildcard='ANY')
#
# example usage in main().


class EnumManager():
  def __init__(self):
    self.next_id = 13370000

  def new(self, class_name, keys, base_classes):
    assert len(list(set(keys))) == len(keys)
    for s in ['to_s', 'from_s', 'values', 'first', 'last', 'is_valid']:
      assert s not in keys
    values = range(self.next_id, self.next_id + len(keys))
    key2value = dict(zip(keys, values))
    members = dict(key2value)
    members['to_s'] = dict(zip(values, keys))
    members['from_s'] = key2value
    members['values'] = set(values)
    first = self.next_id
    last = self.next_id + len(keys) - 1
    members['first'] = first
    members['last'] = last
    members['is_valid'] = lambda self, k: isinstance(k, int) and first <= k <= last
    klass = type(class_name, base_classes, members)
    self.next_id += len(keys)
    return klass()


enum_mgr = EnumManager()


def _insert_excl_wildcard(klass, wildcard_field_name):
  """if have an enum with an ANY field, add methods to it that exclude the ANY."""
  for name in ('values_excl_wildcard', 'is_valid_excl_wildcard'):
    assert not hasattr(klass, name)
  klass.wildcard = getattr(klass, wildcard_field_name)
  klass.values_excl_wildcard = klass.values - set([klass.wildcard])
  klass.is_valid_excl_wildcard = lambda k: (
      isinstance(k, int) and
      klass.first <= k <= klass.last and
      k != klass.wildcard)


def new(s, wildcard=None, base_classes=None):
  """given '<enum name> = <list of enum values>', create corresponding class."""
  # note: if you provide a base_class, it must be a new-style class (inherit
  # from object).
  if base_classes == None:
    base_classes = ()
  ss = s.split()
  assert 2 < len(ss)
  assert ss[1] == '='
  klass = enum_mgr.new(ss[0], ss[2:], base_classes)
  if wildcard:
    _insert_excl_wildcard(klass, wildcard)
  return klass


def main():
  Color = new('Color = RED GREEN BLUE ANY', wildcard='ANY')
  print Color.to_s
  print Color.from_s
  print Color.GREEN
  print Color.to_s[Color.GREEN]
  print Color.first, Color.GREEN, Color.last
  print Color.values
  print Color.values_excl_wildcard
  print Color.is_valid(Color.RED)
  print Color.is_valid_excl_wildcard(Color.RED)
  print Color.is_valid(Color.ANY)
  print Color.is_valid_excl_wildcard(Color.ANY)


if __name__ == '__main__':
  main()
