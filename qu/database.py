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

from . import config, orm, musicfinder, pathutils
import os, sys
import logging
import time

engine = orm.new_engine(config.database_url, encoding=config.database_encoding)
Entity = orm.new_entity()
Session = orm.Session.bind(engine)


class Track(Entity):
  id = orm.int(primary_key=True)

  # Mime type of the track.
  mime = orm.string()

  # Path to the file relative to the library root directory.
  path = orm.unicode(unique=True)

  # Time the track information was last updated.
  last_update_time = orm.int()

  # Metadata.
  title = orm.unicode()
  artist = orm.unicode()
  album = orm.unicode()
  modified_by = orm.unicode()
  grouping = orm.unicode()
  copyright = orm.unicode()
  publisher = orm.unicode()
  composer = orm.unicode()
  track = orm.int()
  set = orm.int()
  bmp = orm.int()
  year = orm.int()
  genre = orm.unicode()
  codec = orm.unicode()
  encoded_by = orm.unicode()

  @staticmethod
  def get(filename, or_create=False):
    session = Session.current()
    path = os.path.relpath(filename, config.library_root)
    path = pathutils.to_dbpath(path)
    track = session.query(Track).filter_by(path=path).one_or_none()
    if track is None and or_create:
      track = Track(path=path)
    return track


Entity.metadata.create_all(engine)


def check_skip_track(filename):
  """
  Checks if there is a #Track in the database for the specified
  *filename* and then checks if it hasn't been updated since the
  file was last changed. Returns True if the file does not need
  to be updated.

  Should be used with #musicfinder.MusicFinder.discover(). Requires
  an active #Session.
  """

  track = Track.get(filename)
  if track is None:
    return False

  mtime = os.path.getmtime(filename)
  if mtime > track.last_update_time:
    return False

  return True


@Session.wraps
def syncdb():
  print('qu syncdb')

  new_tracks = 0
  updated_tracks = 0
  session = Session.current()
  finder = musicfinder.MusicFinder()
  gen = finder.discover(config.library_root, check_skip_track)
  for filename, metadata, provider in gen:
    print('.', end='')
    sys.stdout.flush()
    track = Track.get(filename, or_create=True)
    if not track.last_update_time:
      new_tracks += 1
    else:
      updated_tracks += 1

    # Transfer the metadata to the track.
    for key, value in metadata.items():
      if hasattr(track, key):
        setattr(track, key, value)
    track.last_update_time = time.time()

    session.add(track)

  print()
  print('{} new tracks, {} updated'.format(new_tracks, updated_tracks))
