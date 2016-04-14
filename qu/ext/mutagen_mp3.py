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

from ..metadata import MetaDataProvider, MimeData
import importlib
import mutagen.mp3


class MutagenProvider(MetaDataProvider):

  def read_metadata(self, filename):
    try:
      tags = mutagen.mp3.Open(filename)
    except mutagen.MutagenError:
      return None

    metadata = {
      'mime': 'audio/mp3',
      'title': tags.get('TIT2'),
      'artist': tags.get('TPE1'),
      'album': tags.get('TALB'),
      'modified_by': tags.get('TPE4'),

      'grouping': tags.get('TPE2'),
      'copyright': tags.get('TCOP'),
      'publisher': tags.get('TPUB'),
      'composer': tags.get('TCOM'),

      'track': tags.get('TRCK'),
      'set': tags.get('TPOS'),
      'bmp': tags.get('TBPM'),
      'encoded_by': tags.get('TENC'),
      'year': tags.get('TDRC') or tags.get('TYER'),
      'genre': tags.get('TCON'),
      'codec': tags.get('TFLT'),
    }

    # Filter out empty metadata and convert all tags to strings.
    metadata = filter(lambda x: bool(x[1]), metadata.items())
    metadata = map(lambda x: (x[0], str(x[1])), metadata)
    metadata = dict(metadata)

    # Load the covert art, it must be converted to a MimeData object.
    covert_art = tags.get('APIC:')
    if covert_art:
      metadata['cover'] = MimeData(covert_art.mime, covert_art.data)

    return metadata


def install_metadata_provider(register_provider):
  register_provider(MutagenProvider(), '.mp3')
