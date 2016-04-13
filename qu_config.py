# qu configuration file.

from os.path import join, dirname
here = dirname(__file__)

host = '0.0.0.0'
port = 5000

# Extension modules for the qu.musicfinder.MusicFinder class.
# This specifies what music file types are supported by qu.
musicfinder_extensions = [
  'qu.ext.mutagen_mp3',
]

# Path to your music library root directory. This directory
# will be scanned for music.
library_root = '/Users/niklas/Music/iTunes/iTunes Media'

# URL to the database that caches the library information.
database_url = 'sqlite:///' + join(here, 'database.sqlite')
database_encoding = 'utf-8'
