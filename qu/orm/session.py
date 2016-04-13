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

from sqlalchemy.orm import session, sessionmaker
from threading import local as threadlocal
from weakref import ref as weakref


class Session(session.Session):
  """
  Custom SQLAlchemy session class. Supports the Python contextmanager
  interface and a thread-local current session stack. The current
  #Session can be retrieved using #Session.current().
  """

  local = threadlocal()

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._clean_stack()
    self.local.stack.append(weakref(self))

  def __enter__(self):
    return self

  def __exit__(self, exc_value, exc_type, exc_tb):
    """
    Rollback on error, commit otherwise. Finally close
    the session.
    """
    try:
      if exc_value is not None:
        self.rollback()
      else:
        self.commit()
    finally:
      self.close()

  @classmethod
  def bind(cls, bind, *args, **kwargs):
    """
    Creates a new subclass of the specified #cls which automatically
    constructs using the specified arguments. This is different from
    the #sqlalchemy.orm.sessionmaker() function in that it returns an
    actual class object that inherits from #cls.
    """

    class Session(cls):
      def __init__(self):
        super().__init__(bind=bind, *args, **kwargs)
    return Session

  @staticmethod
  def _clean_stack():
    local = Session.local
    if not hasattr(local, 'stack'):
      local.stack = []
    else:
      local.stack = [ref for ref in local.stack if ref() is not None]

  @staticmethod
  def current():
    Session._clean_stack()
    local = Session.local
    if not local.stack:
      raise RuntimeError("no current Session")
    return local.stack[-1]()

  @classmethod
  def wraps(cls, func):
    def decorator(*args, **kwargs):
      with cls():
        return func(*args, **kwargs)
    return decorator
