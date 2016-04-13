
function play(trackId, mime) {
  var audio = document.getElementById('audio');
  var audioSource = document.getElementById('audio-source');
  audioSource.setAttribute('src', '/stream/' + trackId);
  audioSource.setAttribute('type', mime);
  audio.load();
  audio.play();
}
