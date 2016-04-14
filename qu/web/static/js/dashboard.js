
function play(trackId) {
  var track = document.getElementById('track-' + trackId);
  var audio = document.getElementById('audio');
  audio.setAttribute('src', '/stream/' + trackId);
  audio.setAttribute('type', track.getAttribute('data-track-mime'));
  audio.load();
  audio.play();

  var currentTrack = document.getElementById('current-track');
  currentTrack.innerText = track.getAttribute('data-track-title');
  var currentArtist = document.getElementById('current-artist');
  currentArtist.innerText = track.getAttribute('data-track-artist');
  var currentAlbum = document.getElementById('current-album');
  currentAlbum.innerText = track.getAttribute('data-track-album');
  var currentAlbumPic = document.getElementById('current-album-pic');
  currentAlbumPic.setAttribute('src', '/pic/' + trackId);
}


function sortTracks(attr) {
  // TODO
}
