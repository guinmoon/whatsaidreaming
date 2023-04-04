$(document).ready(function(){
    // stream_player = new Audio('radio/ai_radio_192'); //FOR RAW HTML5 
    
    const onMetadata = (metadata) => {
        document.getElementById("metadata").innerHTML = metadata.StreamTitle;
    };

    const onMetadataEnqueue = (metadata) => {
        document.getElementById("metadata").innerHTML = metadata.StreamTitle;
    };

    stream_player = 
    new IcecastMetadataPlayer(
        "radio/ai_radio_192", // stream endpoint
        // "radio/vorbis_avg_128", // stream endpoint
        { onMetadata,onMetadataEnqueue }                        // options (onMetadata callback)
    );
    // const { mediasource, html5, webaudio } = IcecastMetadataPlayer.canPlayType();
    stream_player.playbackMethod = "html5";
    // stream_player.playbackMethod = "webaudio";
});

function play_pause_stream(player){    
    // if (player.paused){
    //     player.play();
    // }
    // else{
    //     player.pause();
    // } //FOR RAW HTML5     
    if (player.state!="playing"){
        player.play();
        $("#play_pause_cat").attr('class', 'fa fa-pause');
        $("#play_pause_cat_top").attr('class', 'fa fa-pause');
    }
    else{
        player.stop();
        $("#play_pause_cat").attr('class', 'fa fa-play');
        $("#play_pause_cat_top").attr('class', 'fa fa-play');
    }
}



