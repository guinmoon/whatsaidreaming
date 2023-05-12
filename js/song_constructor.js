var generate_song_text_interval= null;
var generate_music_interval= null;
var synth_music_interval = null;
// generate_song_text_interval = window.setInterval(function(){ check_song_generating();},1000);
// generate_music_interval = window.setInterval(function(){ check_music_generating();},1000);
// synth_music_interval = window.setInterval(function(){ check_music_synth();},1000);
var abcjsEditor;
var synthControl;
var tuneBook;
var cursorControl;
var cursor=null;
var wavesurfer = null;
var mp3_download_url=null;

var current_tunes_count=0;


function check_song_generating(){
    i_was_here=getCookie('i_was_here');
    $.post("/check_song_generating", {"i_was_here":i_was_here},function(returned , status){
        status=JSON.parse(returned);
        if (status[0]==""){
            return;
        }
        $("#song_status").text(status[0]);
        if (status[0]=="done"){
            $("#song_text").val(status[1]);
            on_song_text_change(status[1]);
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

// This is a traditional Irish dance music.
// Note Length-1/8
// Meter-6/8
// Key-D

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
            let full_abc=$("#abc_text").val();
            full_abc=full_abc+"\n"+status[1];
            $("#abc_text").val(full_abc);
            init_tune_selector($("#abc_text").val())
            initEditor();
            clearInterval(generate_song_text_interval);  
            generate_song_text_interval = null;
        }
    })
}

function generate_music(){
    i_was_here=getCookie('i_was_here');
    var song_text = $("#song_text").val();
    var music_options_raw = $("#music_options").val();
    let music_options_arr = music_options_raw.split('+');
    var music_options = "";
    music_options_arr.forEach(music_option => {
        music_options = music_options+music_option.trim()+"\n";
    });
    $.post("/generate_music", {"song_text": song_text,"music_options":music_options,"i_was_here":i_was_here},function(returned , status){
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



function check_music_synth(){
    i_was_here=getCookie('i_was_here');
    $.post("/check_music_synth", {"i_was_here":i_was_here},function(returned , status){
        status=JSON.parse(returned);
        if (status[0]==""){
            return;
        }
        $("#song_status").text(status[0]);
        if (status[0]=="done"){
            let mp3_link=status[1];
            mp3_download_url = mp3_link;
            $('#download_mp3').attr({target: '_blank', href  : mp3_download_url,download:mp3_download_url});
            // $("#mp3_player").text(mp3_link);
            $("#mp3_player").empty();
            $("#player_wrapper").css("display","block");
            clearInterval(synth_music_interval);  
            synth_music_interval = null;
            wavesurfer = WaveSurfer.create({
                container: '#mp3_player',
                waveColor: '#7987b5',
                progressColor: '#eb8ca5',
                barWidth:2,
                barHeight:3,
                responsive:false
        
            });
            wavesurfer.load('/'+mp3_link);
        }
    })
}

function synth_music(){
    i_was_here=getCookie('i_was_here');
    var full_abc=$("#abc_text").val();
    var synth_options_raw = $("#synth_options").val();
    let synth_options_arr = synth_options_raw.split(',');
    var synth_options = synth_options_arr;
    // var synth_options = "";
    // synth_options_arr.forEach(music_option => {
    //     synth_options = synth_options+music_option.trim()+"\n";
    // });
    $.post("/synth_music", {"abc_text": full_abc,"synth_options":synth_options_raw,"i_was_here":i_was_here},function(returned , status){
        status=JSON.parse(returned);
        if (synth_music_interval==null){
            synth_music_interval = window.setInterval(function(){ check_music_synth();},1000);
        }
        if (status.length<2){
            $("#song_status").text(status);
            return;
        }
        $("#song_status").text(status[0]);
        if (status[0]=="done"){
            clearInterval(synth_music_interval);  
            synth_music_interval = null;
        }
    })
}


function mp3_player_play_pause(){
    wavesurfer.playPause();
    if (wavesurfer.isPlaying()){
        $("#play_pause_mp3").attr('class', 'fa fa-pause');
    }
    else{
        $("#play_pause_mp3").attr('class', 'fa fa-play');
    }
}

function download_mp3(){

}

function clickListener(abcElem, tuneNumber, classes, analysis, drag, mouseEvent) {

    cursor.setAttribute("x1", abcElem.abselem.notePositions[0].x-abcElem.abselem.w+2);
    cursor.setAttribute("x2", abcElem.abselem.notePositions[0].x-abcElem.abselem.w+2);
    cursor.setAttribute("y1", abcElem.abselem.notePositions[0].y-40);
    cursor.setAttribute("y2", abcElem.abselem.notePositions[0].y+40);    
    
    synthControl.seek(abcElem.currentTrackMilliseconds/1000,"seconds");
    
    var lastClicked = abcElem.midiPitches;
    if (!lastClicked){
        return;
    }
    // abcjsEditor.synth.synthControl.seek(lastClicked[0].start+lastClicked[0].duration,"seconds");
    ABCJS.synth.playEvent(lastClicked, abcElem.midiGraceNotePitches,synthControl.visualObj.millisecondsPerMeasure()).then(function (response) {
    //   console.log("note played");        
    }).catch(function (error) {
      console.log("error playing note", error);
    });
}

function selectionChangeCallback(start, end) {
    if (abcjsEditor) {
        var el = abcjsEditor.tunes[0].getElementFromChar(start);
        rebind_cursor(cursor);
        let abc=$("#abc_text").val();
        let tuneBook = new ABCJS.TuneBook(abc);
        if (tuneBook.tunes.length!=current_tunes_count){
            init_tune_selector(abc);
        }
        setCookie('abc_text', abc.replaceAll("\n","\\n"),365);
    //   console.log(el);
    }
}

function reset_cursor(cursor){
    cursor.setAttributeNS(null, 'x1', 0);
    cursor.setAttributeNS(null, 'y1', 0);
    cursor.setAttributeNS(null, 'x2', 0);
    cursor.setAttributeNS(null, 'y2', 0);    
}
  
function createCursor() {    
    var cursor = document.createElementNS("http://www.w3.org/2000/svg", "line");
    cursor.setAttribute("class", "abcjs-cursor");
    reset_cursor(cursor);
    rebind_cursor(cursor);
    return cursor;
}

function rebind_cursor(cursor){
    var svg = document.querySelector("#abc_paper0 svg");
    svg.appendChild(cursor);
}


var lastEls = [];
function colorElements(els) {
    var i;
    var j;
    for (i = 0; i < lastEls.length; i++) {
        for (j = 0; j < lastEls[i].length; j++) {
            lastEls[i][j].classList.remove("color");
        }
    }
    for (i = 0; i < els.length; i++) {
        for (j = 0; j < els[i].length; j++) {
            els[i][j].classList.add("color");
        }
    }
    lastEls = els;
}


function CursorControl() {
    var self = this;
    // if (cursor==null){
    //     cursor = createCursor();
    // }
    self.onReady = function() {
        // var downloadLink = document.querySelector(".download");
        // downloadLink.addEventListener("click", download);
        // downloadLink.setAttribute("style", "");
        // var clickEl = document.querySelector(".click-explanation")
        // clickEl.setAttribute("style", "");
        if (cursor==null){
            cursor = createCursor();
        }
    };
    self.onStart = function() {
        if (cursor==null){
            cursor = createCursor();
        }
    };
    self.beatSubdivisions = 2;
    self.onBeat = function(currentBeat,totalBeats,lastMoment,position, debugInfo){
        var x1, x2, y1, y2;
        if (currentBeat === totalBeats) {
            // showAllMeasures();
            x1 = 0;
            x2 = 0;
            y1 = 0;
            y2 = 0;
        } else {
            x1 = position.left - 2;
            x2 = position.left - 2;
            y1 = position.top;
            y2 = position.top + position.height;
        }
        cursor.setAttribute("x1", x1);
        cursor.setAttribute("x2", x2);
        cursor.setAttribute("y1", y1);
        cursor.setAttribute("y2", y2);
    };
    self.onEvent = function(ev) {
        if (!ev) {
            return;
        }
        colorElements(ev.elements);
    };
    self.onFinished = function() {
        var els = document.querySelectorAll("svg .highlight");
        for (var i = 0; i < els.length; i++ ) {
            els[i].classList.remove("highlight");
        }
        // cursor = null;
    };
}

function init_tune_selector(abc) {
    var tuneBook = new ABCJS.TuneBook(abc)
    var select = $("#tune_selector")
    select.empty();
    var option = document.createElement("option");
    var optionContent = document.createTextNode("-- select tune --");
    // option.appendChild(optionContent);
    // select.append(option)
    current_tunes_count = tuneBook.tunes.length;
    for (var i = 0; i < tuneBook.tunes.length; i++) {
        option = document.createElement("option");
        title=tuneBook.tunes[i].title
        if (title==undefined  ||  title==""){
            title=i;
        }
        optionContent = document.createTextNode(title);
        option.appendChild(optionContent);
        option.setAttribute('value', i)
        select.append(option)
    }
    select.bind("change", setTune)
}

function setTune() {
    var index = this.value;
    initEditor(index);
    reset_cursor(cursor);
}

function initEditor(startingTune=0) {    
    cursorControl = new CursorControl();
    var audioParams = { chordsOff: true };
    var abcOptions = { add_classes: true,
            startingTune: startingTune,
            responsive: "resize",
            clickListener: clickListener };
    abcjsEditor = new ABCJS.Editor("abc_text", { paper_id: "abc_paper0", 
        synth: {
            el: "#abc_audio_control",
            cursorControl,
            options: { displayLoop: true, displayRestart: false, displayPlay: true, displayProgress: true, displayWarp: false
                /*,soundFontUrl: "https://aliceghome.online/synth/guinmoon-lite.sf2"*/ }
        },
        generate_warnings: false,
        // warnings_id:"abc_warnings",
        abcjsParams: abcOptions,
        selectionChangeCallback: selectionChangeCallback
    });
    synthControl = abcjsEditor.synth.synthControl;
    var createSynth = new ABCJS.synth.CreateSynth();
    createSynth.init({ visualObj: abcjsEditor.tunes[0] }).then(function () {
        synthControl.setTune(abcjsEditor.tunes[0], false, audioParams).then(function () {
            console.log("Audio successfully loaded.")
        }).catch(function (error) {
            console.warn("Audio problem:", error);
        });
    }).catch(function (error) {
        console.warn("Audio problem:", error);
    });
    
    if (cursor==null){
        cursor = createCursor();
    }
    

    // var abc= $("#abc_text").val();
    // var audioParams = { chordsOff: true };

    // if (ABCJS.synth.supportsAudio()) {
    //     synthControl = new ABCJS.synth.SynthController();
    //     synthControl.load("#abc_audio_control", 
    //         cursorControl, 
    //         {
    //             displayLoop: true, 
    //             displayRestart: true, 
    //             displayPlay: true, 
    //             displayProgress: true, 
    //             displayWarp: true
    //         }
    //     );

    //     var visualObj = ABCJS.renderAbc("abc_paper0",abc, abcOptions);
    //     var createSynth = new ABCJS.synth.CreateSynth();
    //     createSynth.init({ visualObj: visualObj[0] }).then(function () {
    //         synthControl.setTune(visualObj[0], false, audioParams).then(function () {
    //             console.log("Audio successfully loaded.")
    //         }).catch(function (error) {
    //             console.warn("Audio problem:", error);
    //         });
    //     }).catch(function (error) {
    //         console.warn("Audio problem:", error);
    //     });
    //     abcjsEditor = new ABCJS.Editor("abc_text",createSynth);
    // } else {
    //     document.querySelector("#abc_audio_control").innerHTML = 
    //         "Audio is not supported in this browser.";
    // }
}

function on_song_text_change(text){
    setCookie('song_text', text.replaceAll("\n","\\n"),365);
}

function on_music_options_change(text){
    setCookie('music_options', text.replaceAll("\n","\\n"),365);
}


function on_synth_options_change(text){
    setCookie('synth_options', text.replaceAll("\n","\\n"),365);
}

function first_load(){
    let abc_text=getCookie('abc_text');
    if (!(abc_text==undefined||abc_text=="")){
        $("#abc_text").val(abc_text.replaceAll("\\n","\n"));
    }
    let song_text=getCookie('song_text');
    if (!(song_text==undefined||song_text=="")){
        $("#song_text").val(song_text.replaceAll("\\n","\n"));
    }
    let music_options=getCookie('music_options');
    if (!(music_options==undefined||music_options=="")){
        $("#music_options").val(music_options.replaceAll("\\n","\n"));
    }
    let synth_options=getCookie('synth_options');
    if (!(synth_options==undefined||synth_options=="")){
        $("#synth_options").val(synth_options.replaceAll("\\n","\n"));
    }
    $('#song_text').bind('input propertychange', function() {
        on_song_text_change(this.value);
    });
    $('#music_options').bind('input propertychange', function() {
        on_music_options_change(this.value);
    });
    $('#synth_options').bind('input propertychange', function() {
        on_synth_options_change(this.value);
    });
    // $('#song_text').bind('input propertychange', on_song_text_change(this.value));
}