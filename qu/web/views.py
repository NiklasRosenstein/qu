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

from . import app, utils
from .. import config
from ..pathutils import from_dbpath
from ..database import Session, Track
from ..metadata import read_metadata
from flask import request, render_template, stream_with_context, redirect, url_for, Response
import os


@app.route('/')
@Session.wraps
def home():
  tracks = Session.current().query(Track).order_by(Track.grouping, Track.artist, Track.album, Track.title).all()
  return render_template('dashboard.html', tracks=tracks)


@app.route('/stream/<int:track_id>')
@Session.wraps
def stream(track_id):
  track = Session.current().query(Track).get(track_id)
  if not track:
    return "Track not found", 404
  filename = os.path.join(config.library_root, from_dbpath(track.path))
  if not os.path.isfile(filename):
    return "Track not found", 404

  return Response(stream_with_context(utils.stream_file(filename)), 200, [
    ('Content-type', track.mime), ('Accept-Ranges', 'bytes')])


@app.route('/pic/<int:track_id>')
@Session.wraps
def pic(track_id):
  track = Session.current().query(Track).get(track_id)
  if track:
    filename = os.path.join(config.library_root, from_dbpath(track.path))
    if filename:
      metadata = read_metadata(filename)
      if metadata and 'cover' in metadata:
        cover = metadata['cover']
        return Response(cover.data, 200, [('Content-type', cover.mime)])
  return redirect(url_for('static', filename='img/nocover.png'))
