$(document).ready(function(){
    $("#queryInput").on('input',function(){
        var serializedData = $("#searchForm").serialize();
        $.ajax({
            url: $("#searchForm").data('url'),
            data: serializedData,
            type: 'get',
            success: function(response){
                var songs_list = JSON.parse(response.songs)
                var finallySongHtml = ""
                songs_list.forEach(function(song){
                    finallySongHtml += `<li class="result-item" onclick="plusFormSong(${song.pk},'${song.fields.title}')" data-id=${song.pk}><img src="/media/${song.fields.image}"><p>${song.fields.title}</p></li>`
                })

                $("#results-song").html(finallySongHtml)
                
            }
        })
    });
});

function plusFormSong(id,title){
    var selectElement = document.getElementById("id_song");
    var options = selectElement.options;
    for (let i = 0; i < options.length; i++) {
        var option = options[i];
        var dataId = option.value;
        var dataTitle = option.textContent;
        
        if (dataId == id && dataTitle == title) { 
            if(option.selected){
                option.selected = false;
            } else{
                option.selected = true;
            }
            var selectedOptionsList = selectElement.selectedOptions
            var finnalHtml = ""
            let title;
            for(let j=0;j<selectedOptionsList.length;j++){
                title = selectedOptionsList[j].textContent
                
                finnalHtml += `<li class="selected-songs-list-item" data-id="${id}">${title} <span class="del-option" onclick="minusOption(${id},'${title}')">-</span></li>`
            }
            document.querySelector('.selected-songs-list').innerHTML = finnalHtml
        }
      }

}
document.querySelector("#submit-button").addEventListener('click', () => {
    document.querySelector("#form-submit").click()
})

function minusOption(id, title) {
    var selectElement = document.getElementById("id_song");
    var options = selectElement.options;
    for (let i = 0; i < options.length; i++) {
        var option = options[i];
        var dataId = option.value;
        var dataTitle = option.textContent;

        if (dataId == id && dataTitle == title) {
            option.selected = false;
        }
    }

    var selectedOptionsList = selectElement.selectedOptions
    var finnalHtml = ""
    let sId
    let sTitle
    for (let i = 0; i < selectedOptionsList.length; i++) {
        sId = selectedOptionsList[i].value
        sTitle = selectedOptionsList[i].textContent
        finnalHtml += `<li class="selected-songs-list-item" data-id="${sId}">${sTitle} <span class="del-option" onclick="minusOption(${sId},'${sTitle}')">-</span></li>`
    }
    document.querySelector('.selected-songs-list').innerHTML = finnalHtml
}
