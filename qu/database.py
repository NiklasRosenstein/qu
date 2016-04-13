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

from . import orm, config

engine = orm.new_engine(config.database_url, encoding=config.database_encoding)
Entity = orm.new_entity()
Session = orm.new_session(engine)


class Track(Entity):
  id = orm.int(primary_key = True)

  # Path to the file relative to the library root directory.
  path = orm.string()

  # Time the track information was last updated.
  last_update_time = orm.int()

  # Metadata.
  title = orm.string()
  artist = orm.string()
  album = orm.string()
  modified_by = orm.string()
  grouping = orm.string()
  copyright = orm.string()
  publisher = orm.string()
  composer = orm.string()
  track = orm.int()
  set = orm.int()
  bmp = orm.int()
  year = orm.int()
  genre = orm.string()
  codec = orm.string()
  encoded_by = orm.string()


Entity.metadata.create_all(engine)
