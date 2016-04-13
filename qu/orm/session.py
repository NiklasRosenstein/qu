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


class SessionBase(session.Session):
  """
  Custom SQLAlchemy session class that implements the
  Python contextmanager interface.
  """

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
  def bind(cls, bind, **kwargs):
    """
    Create a session bound to the engine #bind. This method
    simply wraps the #sessionmaker function.
    """

    return sessionmaker(bind=bind, class_=cls, **kwargs)


def new_session(bind, class_=SessionBase, *args, **kwargs):
  return sessionmaker(bind=bind, class_=class_, *args, **kwargs)
