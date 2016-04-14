
function play(trackId, mime) {
  var audio = document.getElementById('audio');
  audio.setAttribute('src', '/stream/' + trackId);
  audio.setAttribute('type', mime);
  audio.load();
  audio.play();

  var track = document.getElementById('track-' + trackId);
  var currentTrack = document.getElementById('current-track');
  currentTrack.innerText = track.getAttribute('data-track-title');
  var currentArtist = document.getElementById('current-artist');
  currentArtist.innerText = track.getAttribute('data-track-artist');
  var currentAlbum = document.getElementById('current-album');
  currentAlbum.innerText = track.getAttribute('data-track-album');
  var currentAlbumPic = document.getElementById('current-album-pic');
  currentAlbumPic.setAttribute('src', '/pic/' + trackId);
}
