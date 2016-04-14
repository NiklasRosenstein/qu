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

from . import config
from .pathutils import getsuffix
import os
import importlib


class MetaDataProvider(object):
  """
  Interface for metadata providers that can be installed to a
  #MusicFinder object. Common metadata keys are

  * `mime`- the file's mimetype
  * `title` - the track title
  * `artist` - the artist name
  * `album`- the album name
  * `modified_by` - reinterpretation artist, eg. remixer
  * `grouping` - preferred identifier over `artist` for grouping
  * `copyright` - copyright information
  * `publisher` - publisher name(s)
  * `composer` - composer name(s)
  * `track` - track number as `X` or `X/Y`
  * `set` - CD/set number as `X` or `X/Y`
  * `bmp` - beats per minute as number
  * `year` - release date
  * `genre` - genre name
  * `cover` - #MimeData object for the album cover art
  * `codec` - file codec information
  * `encoded_by` - file encoder information
  """

  def read_metadata(self, filename):
    """
    Called to read metadata from the specified #filename. The
    file is garuanteed to exist and ends with the suffix that
    the provider was registered for.

    :return: A #dict mapping the metadata. Common metadata
      keys are listed in the docstring of #MetaDataProvider.
      Keys are case-sensitive.
    """

    raise NotImplementedError


class MimeData(object):
  """
  Represents binary data accompanied by a mime-type.
  """

  def __init__(self, mime, data):
    self.mime = mime
    self.data = data

  def __repr__(self):
    size = len(self.data)
    return 'MimeData(mime={!r}, len(data)={})'.format(self.mime, size)


providers = {}


def load_extension(*extensions):
  """
  Imports the module(s) specified by #extensions and runs its
  `install_metadata_provider()` function, passing the #MusicFinder
  as argument.
  """

  for ext in extensions:
    module = importlib.import_module(ext)
    module.install_metadata_provider(register_provider)


def register_provider(provider, suffix):
  """
  Register a #MetaDataProvider for the specified #suffix.
  """

  providers[suffix] = provider


def read_metadata(filename):
  """
  Selects the appropriate #MetaDataProvider for the specified #filename
  and returns the metadata dictionary it extracts, or returns None if
  no metadata could be extracted.
  """

  suffix = getsuffix(filename)
  if suffix not in providers:
    return None

  return providers[suffix].read_metadata(filename)
