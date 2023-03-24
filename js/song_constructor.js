
var generate_song_text_interval = window.setInterval(function(){ check_song_generating();},1000);
var generate_music_interval = window.setInterval(function(){ check_music_generating();},1000);


function check_song_generating(){
    i_was_here=getCookie('i_was_here');
    $.post("/check_song_generating", {"i_was_here":i_was_here},function(returned , status){
        status=JSON.parse(returned);
        if (status[0]==""){
            return;
        }
        $("#song_status").text(status[0]);
        if (status[0]=="done"){
            $("#song_text").text(status[1]);
            clearInterval(generate_song_text_interval);  
            generate_song_text_interval = null;
        }
    })
}

function generate_song_text(){
    i_was_here=getCookie('i_was_here');
    var song_text_query = $("#song_text_query").val();
    $.post("/generate_song_text", {"song_text_query": song_text_query,"i_was_here":i_was_here},function(returned , status){
        status=JSON.parse(returned);
        if (generate_song_text_interval==null){
            generate_song_text_interval = window.setInterval(function(){ check_song_generating();},1000);
        }
        if (status.length<2){
            $("#song_status").text(status);
            return;
        }
        $("#song_status").text(status[0]);
        if (status[0]=="done"){
            clearInterval(generate_song_text_interval);  
            generate_song_text_interval = null;
        }
    })
}



function check_music_generating(){
    i_was_here=getCookie('i_was_here');
    $.post("/check_music_generating", {"i_was_here":i_was_here},function(returned , status){
        status=JSON.parse(returned);
        if (status[0]==""){
            return;
        }
        $("#song_status").text(status[0]);
        if (status[0]=="done"){
            // $("#song_notes").empty();
            // var notes=`<img src="${status[1]}">`;
            // $("#song_notes").append(notes);
            $("#abc_text").text(status[1]);
            render_abc();
            clearInterval(generate_song_text_interval);  
            generate_song_text_interval = null;
        }
    })
}

function render_abc() {
    ABCJS.renderAbc("song_notes", $("#abc_text").text());
}


function generate_music(){
    i_was_here=getCookie('i_was_here');
    var song_text = $("#song_text").val();
    $.post("/generate_music", {"song_text": song_text,"i_was_here":i_was_here},function(returned , status){
        status=JSON.parse(returned);
        if (generate_music_interval==null){
            generate_music_interval = window.setInterval(function(){ check_music_generating();},1000);
        }
        if (status.length<2){
            $("#song_status").text(status);
            return;
        }
        $("#song_status").text(status[0]);
        if (status[0]=="done"){
            clearInterval(generate_music_interval);  
            generate_music_interval = null;
        }
    })
}