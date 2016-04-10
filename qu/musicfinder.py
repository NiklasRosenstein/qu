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

from .pathutils import getsuffix
import os
import importlib


class MusicFinder(object):
  """
  This class implements searching for music files by adressing
  the correct metadata provider based on the file suffix. The
  metadata is then returned to the user of the #MusicFinder.
  """

  def __init__(self):
    self.providers = {}

  def install_provider(self, provider, file_suffix):
    """
    Install a provider to the #MusicFinder for the specified
    #file_suffix.

    :param provider: #MetaDataProvider object
    :param file_suffix: #str object starting with a period
    :raise ValueError: if the #file_suffix is already occupied
    """

    if not isinstance(provider, MetaDataProvider):
      raise TypeError('provider must be MetaDataProvider object')
    if not isinstance(file_suffix, str):
      raise TypeError('file_suffix must be str')
    if file_suffix in self.providers:
      raise ValueError('file_suffix "{}" already occupied'.format(file_suffix))

    self.providers[file_suffix] = provider

  def load_extension(self, *extensions):
    """
    Imports the module(s) specified by #extensions and runs its
    `install_metadata_provider()` function, passing the #MusicFinder
    as argument.
    """

    for ext in extensions:
      module = importlib.import_module(ext)
      module.install_metadata_provider(self)

  def discover(self, library_root, skip_file = None):
    """
    This function discovers all music files in #library_root,
    invoking the appropriate #MetaDataProvider to retrieve the
    metadata and yields it in a tuple with the filename.

    The #skip_file function is used to skip files from extracting
    the metadata. This is useful to ignore files for which the
    metadata is already known and it is sure that it has not changed.
    Note that #skip_file is not called for files for which no
    provider is installed.

    :return: generator yielding `(filename, metadata, provider)`
    """

    if skip_file is None:
      skip_file = lambda f: False

    for root, dirs, files in os.walk(library_root):
      for filename in files:
        provider = self.providers.get(getsuffix(filename))
        if not provider:
          continue

        filename = os.path.join(root, filename)
        if skip_file(filename):
          continue

        metadata = provider.read_metadata(filename)
        if metadata is not None:
          yield (filename, metadata, provider)


class MetaDataProvider(object):
  """
  Interface for metadata providers that can be installed to a
  #MusicFinder object. Common metadata keys are

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
  * `encoded_by` - file encoder information
  * `year` - release date
  * `genre` - genre name
  * `codec` - file codec information
  * `cover` - #MimeData object for the album cover art
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
