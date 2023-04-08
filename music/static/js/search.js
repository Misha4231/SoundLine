$(document).ready(function(){
    $("#queryInput").on('input',function(){
        var serializedData = $("#searchForm").serialize();
       
        $.ajax({
            url: $("#searchForm").data('url'),
            data: serializedData,
            type: 'post',
            success: function(response){
                var songs_list = JSON.parse(response.songs)
                var playlists = JSON.parse(response.playlists)
                var finallySongHtml = ""
                var finallyPlaylistHtml = ""
                songs_list.forEach(function(song){
                    console.log(song)
                    finallySongHtml += `<a href="${song.fields.link}"><li class="result-item" data-id=${song.pk}><img src="/media/${song.fields.image}"><p>${song.fields.title}</p></li></a>`
                })
                playlists.forEach(function(playlist){
                    finallyPlaylistHtml += `<a class="result-item-link" href="${playlist.fields.link}"><li class="result-item" data-id=${playlist.pk}><img src="/media/${playlist.fields.image}"><p>${playlist.fields.title}</p></li></a>`
                })
                $("#results-song").html(finallySongHtml)
                $("#results-playlist").html(finallyPlaylistHtml)
            }
        })
    });
});


