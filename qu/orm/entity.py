# Copyright (c) 2016  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from sqlalchemy import event
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


class EntityMeta(DeclarativeMeta):
  """
  Metaclass for an SQLAlchemy declarative base class that
  implements the event registration to enable event callbacks.
  The supported callbacks are

  * `save()` - invoked by `before_insert` and `before_update`
  * `delete()` - invoked by `before_delete`
  * `validate_X(v, oldv, initiator)` - invoked by `set`,
    where `X` is the name of a column. return the new value

  For more information on SQLAlchemy ORM events, see
  http://docs.sqlalchemy.org/en/latest/orm/events.html

  Additionally, this metaclass will take care of the following:

  * set `__tablename__` if it is not defined
  """

  def __new__(cls, name, bases, data):

    # validate_X() method - used to validate when a parameter is set.
    for key in data:
      if key.startswith('validate_'):
        attr_name = key[len('validate_'):]
        attr = data.get(attr_name)
        if isinstance(attr, InstrumentedAttribute):
          def callback(target, value, oldvalue, initiator):
            return getattr(target, key)(value, oldvalue, initiator)
          event.listen(attr, 'set', callback, retval=True)

    # save() method - used in before_update and before_insert.
    if 'save' in data:
      @event.listens_for(cls, 'before_update')
      @event.listens_for(cls, 'before_insert')
      def callback(mapper, connection, target):
        target.save()

    # delete() method - used in before_delete.
    if 'delete' in data:
      @event.listens_for(cls, 'before_delete')
      def callback(mapper, connection, target):
        target.delete()

    if '_decl_class_registry' not in data:
      # This is not a declarative base class.
      if '__tablename__' not in data:
        data['__tablename__'] = name.lower()

    return super().__new__(cls, name, bases, data)


def new_entity(name='Entity', metaclass=EntityMeta):
  return declarative_base(name=name, metaclass=metaclass)
