$(document).ready(function(){
    $("#queryInput").on('input',function(){
        var serializedData = $("#searchForm").serialize();
        $.ajax({
            url: $("#searchForm").data('url'),
            data: serializedData,
            type: 'get',
            success: function(response){
                var songs_list = JSON.parse(response.users)
                
                var finallySongHtml = ""
                songs_list.forEach(function(song){
                    finallySongHtml += `<li class="result-item" onclick="plusFormSong(${song.pk},'${song.fields.username}')" data-id=${song.pk}><p>${song.fields.username}</p></li>`
                })

                $("#results-song").html(finallySongHtml)
                
            }
        })
    });
});

function plusFormSong(id,title){
    var selectElement = document.getElementById("id_authors");
    var options = selectElement.options;
    for (let i = 0; i < options.length; i++) {
        var option = options[i];
        var dataId = option.value;
        var dataTitle = option.textContent;
        var userData = document.querySelector("#data").dataset
        if (dataId == id && dataTitle == title) { 
            if(option.selected){
                if(userData.id!=dataId && userData.name!=dataTitle){
                    console.log(userData.id)
                    option.selected = false;
                }
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
function minusOption(id, title) {
    var selectElement = document.getElementById("id_authors");
    var options = selectElement.options;
    for (let i = 0; i < options.length; i++) {
        var option = options[i];
        var dataId = option.value;
        var dataTitle = option.textContent;
        var userData = document.querySelector("#data").dataset
        if (dataId == id && dataTitle == title) {
            if(userData.id!=dataId && userData.name!=dataTitle){
                option.selected = false;
            }
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

