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

from flask import request


def stream_file(filename, mode='rb', chunksize=2048, range=NotImplemented):
  """
  Stream the contents of the specified #filename with the specified
  #chunksize and #range. If #range is #NotImplemented, it will default
  be read from the current request's `Range` header. If #range is None,
  the whole file will be streamed.
  """

  if range is NotImplemented:
    range = parse_range(request.headers.get('Range'))
  elif range is None:
    range = (0, None)
  print(range)

  with open(filename, mode) as fp:
    fp.seek(range[0])
    bytes_read = 0
    while True:
      if range[1] is not None and bytes_read + chunksize > range[1]:
        data = fp.read(range[1] - bytes_read)
      else:
        data = fp.read(chunksize)

      if not data: break
      yield data


def parse_range(range):
  """
  Parse an HTTP range. Only supports byte ranges. Returns a tuple of
  the start and end offsets, where the end can be #None to indicate
  all up to the file's end.
  """

  if not range or not range.startswith('bytes='):
    return (0, None)

  parts = range[6:].split('-')
  if len(parts) != 2:
    return (0, None)

  try:
    return tuple(int(x) if x else None for x in parts)
  except ValueError:
    return (0, None)
