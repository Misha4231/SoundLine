var playButtons = document.querySelectorAll('.play-button');
var isPlaying = false;
let currentAudio = null;
let currentIndex = -1;
let audioList = document.querySelectorAll('.audio-song');
var selectedTrackIndex = -1;

var pausePath = document.querySelector("#path").dataset.pause;
var playPath = document.querySelector("#path").dataset.play;

function resetAllCurrentTime(){
    audioList.forEach(function(audio){
        audio.currentTime = 0
    })
}

function resetIcons(){
    audioList.forEach(function(audio){
        audio.parentNode.querySelector('.play-button').innerHTML = `<img class="icon-1 currimg" src="${playPath}" height="20" width="20" alt="">`
    })
}

function formatTime(timeInSeconds) {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    return minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
}

function get_time(audio){
    document.querySelector('#lenght-varibe-value').innerHTML = '0:00'
    document.querySelector('#length-value').innerHTML = formatTime(audio.duration)
}

function changeCurrentInfo(audio){
    var song_title = audio.parentNode.querySelector('.song-title').textContent
    var song_link = audio.parentNode.querySelector('.song-title').href
    var song_image_src = audio.parentNode.querySelector('.song-image').src
    document.querySelector('#current-song-image').style.display = 'block'
    document.querySelector('#current-song-image').src = song_image_src
    document.querySelector('#current-song-title').textContent = song_title
    document.querySelector('#current-song-title').href = song_link
    document.querySelector('#current-song-image').height = 100
    document.querySelector('#current-song-image').width = 100
}

audioList.forEach(function(audio){
    audio.volume ='0.2'
})

playButtons.forEach(function(button, index) {
    button.addEventListener('click', function() {
        var audio = this.parentNode.querySelector('.audio-song');
        if (isPlaying && currentAudio) {
            currentAudio.pause();
            currentAudio.parentNode.querySelector('.play-button').innerHTML = `<img class="icon-1 currimg" src="${playPath}" height="20" width="20" alt="">`
            document.querySelector('.play-button-down').innerHTML = `<img class="icon-1 currimg" src="${playPath}" height="20" width="20" alt="">`
        }
        if (isPlaying && currentAudio==audio){
            audio.pause()
            this.innerHTML = `<img class="icon-1 currimg" src="${playPath}" height="20" width="20" alt="">`
            document.querySelector('.play-button-down').innerHTML = `<img class="icon-1 currimg" src="${playPath}" height="20" width="20" alt="">`
            isPlaying = false;
        } else{
            audio.play()
            this.innerHTML = `<img class="icon-2 currimg" src="${pausePath}" height="20" width="20" alt="">`
            document.querySelector('.play-button-down').innerHTML = `<img class="icon-2 currimg" src="${pausePath}" height="20" width="20" alt="">`
            isPlaying = true;
        }
        currentAudio = audio;

        currentIndex = index;
        selectedTrackIndex = index
        currentAudio.addEventListener('ended', playNext);
        resetAllCurrentTime()
        get_time(audio)
        changeCurrentInfo(audio)
        
    });
});

function playNext() {
    if (currentAudio) {
        currentAudio.pause();
        isPlaying = false;
    }
    currentIndex += 1;
    if (currentIndex >= audioList.length) {
        currentIndex = 0;
    }
    currentAudio = audioList[currentIndex];
    currentAudio.play();
    isPlaying = true;
    resetIcons()
    currentAudio.parentNode.querySelector('.play-button').innerHTML = `<img class="icon-2 currimg" src="${pausePath}" height="20" width="20" alt="">`
    document.querySelector('.play-button-down').innerHTML = `<img class="icon-2 currimg" src="${pausePath}" height="20" width="20" alt="">`
    currentAudio.addEventListener('ended', playNext);
    selectedTrackIndex += 1
    if (selectedTrackIndex >= audioList.length) {
        selectedTrackIndex = 0;
    }
    resetAllCurrentTime()
    get_time(currentAudio)
    changeCurrentInfo(currentAudio)
}

function playPrevious(){
    if (currentAudio) {
        currentAudio.pause();
        isPlaying = false;
    }
    currentIndex -=1
    if (currentIndex < 0) {
        currentIndex = audioList.length-1;
    }
    currentAudio = audioList[currentIndex];
    currentAudio.play();
    resetIcons()
    currentAudio.parentNode.querySelector('.play-button').innerHTML = `<img class="icon-2 currimg" src="${pausePath}" height="20" width="20" alt="">`
    document.querySelector('.play-button-down').innerHTML = `<img class="icon-2 currimg" src="${pausePath}" height="20" width="20" alt="">`
    isPlaying = true;
    selectedTrackIndex -= 1
    if (selectedTrackIndex < 0) {
        selectedTrackIndex = audioList.length-1;
    }
    currentAudio.addEventListener('ended', playNext);
    resetAllCurrentTime()
    get_time(currentAudio)
    changeCurrentInfo(currentAudio)
}

var playButttonDown = document.querySelector('#play2');
playButttonDown.addEventListener('click', function() {
    if (isPlaying) {
        isPlaying = false;
        currentAudio.pause();
        document.querySelector('.play-button-down').innerHTML = `<img class="icon-1 currimg" src="${playPath}" height="20" width="20" alt="">`
        currentAudio.parentNode.querySelector('.play-button').innerHTML = `<img class="icon-1 currimg" src="${playPath}" height="20" width="20" alt="">`
    } else {
        isPlaying = true;
        if (currentAudio) {
            currentAudio.play();
            document.querySelector('.play-button-down').innerHTML = `<img class="icon-2 currimg" src="${pausePath}" height="20" width="20" alt="">`
            currentAudio.parentNode.querySelector('.play-button').innerHTML = `<img class="icon-2 currimg" src="${pausePath}" height="20" width="20" alt="">`
        } else {
            playNext();
        }
    }
    
    
});


var nextButton = document.querySelector('#play-next')
nextButton.addEventListener('click', playNext)

var prevButton = document.querySelector('#play-prev')
prevButton.addEventListener('click', playPrevious)

var volumeSlider = document.querySelector('#volume-slider')

volumeSlider.addEventListener('change',function(){
    var value = this.value
    audioList.forEach(function(audio) {
        audio.volume = value
    });
})


var progress = document.querySelector('.progress')

audioList.forEach(function(audio){
    audio.addEventListener('timeupdate', function(e){
        var {duration, currentTime} = e.srcElement
        var progressPersent = (currentTime/duration)*100
        progress.style.width = `${progressPersent}%`
        document.querySelector('#lenght-varibe-value').innerHTML = formatTime(currentTime)
    })
})

var progressConteiner = document.querySelector('.progress__container')
var width = progressConteiner.clientWidth
progressConteiner.addEventListener('click', function(e){
    var clickX = e.offsetX
    var duration = currentAudio.duration
    currentAudio.currentTime = (clickX/width) * duration
})

var countHearings = 0;

function plusHearing(){
    var link = currentAudio.dataset.link
    var xhr = new XMLHttpRequest();
    xhr.open('GET', link);
    xhr.send();

    countHearings += 1
    if(countHearings<=1){
        var saveLink = document.querySelector("#history_save_link").dataset.url
        var req = new XMLHttpRequest()
        req.open("GET", saveLink)
        req.send()
    }
}

$('.like').each(function(){
    $(this).click(function(){
        var link = $(this).data('url')
        var xhr = new XMLHttpRequest()
        xhr.open('GET', link)
        xhr.send()
        let prevLikes = parseInt($(this).closest('li').find('.total').text());
        
        if ($(this).find('> img').attr('class') == 'like-photo'){
            $(this).html(`<img src="${$(this).data('black')}" class="unlike-photo">`)
            $(this).closest('li').find('.total').text(String(prevLikes+1))
        } else{
            $(this).html(`<img src="${$(this).data('transparent')}" class="like-photo">`)
            $(this).closest('li').find('.total').text(String(prevLikes-1))
        }
    })
})