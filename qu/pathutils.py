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

import os


def getsuffix(filename):
  filename = os.path.basename(filename)
  index = filename.rfind('.')
  if index > 0:
    return filename[index:]
  return ''


def to_dbpath(path):
  """
  Normalize *path* to Unix-style format on all platforms. This is used
  for storing paths in a database to keep the data consistent if migrated
  to a different platform.
  """

  return path.replace('\\', '/')


def from_dbpath(path):
  """
  Convert from a Unix-style path to a path appropriate for the current
  platform. This should be used with paths from the database.
  """

  return path.replace('/', os.sep)
