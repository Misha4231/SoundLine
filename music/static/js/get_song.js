var button = document.querySelector('#play2')
var isPlaying = false
var audio = document.querySelector('.player-audio')

function formatTime(timeInSeconds) {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    return minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
}

audio.addEventListener("loadedmetadata", function() {
    document.querySelector('#length-value').innerHTML = formatTime(audio.duration)
  });
audio.volume = '0.2'
button.addEventListener('click', function(){
    if(isPlaying){
        audio.pause()
        isPlaying = false
        document.getElementById('play2').innerHTML = 'play'
    } else{
        audio.play()
        isPlaying = true
        document.getElementById('play2').innerHTML = 'pause'
    }
})

var volumeSlider = document.querySelector('#volume-slider')
volumeSlider.addEventListener('input', function(){
    audio.volume = volumeSlider.value
})

function plusHearing(){
    var link = document.querySelector('#obj-l').value
    var xhr = new XMLHttpRequest();
    xhr.open('GET', link);
    xhr.send();
   
}

var progress = document.querySelector('.progress')
audio.addEventListener('timeupdate', function(e){
    var {duration, currentTime} = e.srcElement
    var progressPersent = (currentTime/duration)*100
    progress.style.width = `${progressPersent}%`
    document.querySelector('#lenght-varibe-value').innerHTML = formatTime(currentTime)
})

var progressConteiner = document.querySelector('.progress__container')
var width = progressConteiner.clientWidth
progressConteiner.addEventListener('click', function(e){
    var clickX = e.offsetX
    var duration = audio.duration
    audio.currentTime = (clickX/width) * duration

})