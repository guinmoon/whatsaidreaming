$(document).ready(function(){
    // stream_player = new Audio('radio/ai_radio_192'); //FOR RAW HTML5 
    
    const onMetadata = (metadata) => {
        // document.getElementById("metadata").innerHTML = metadata.StreamTitle;
    };

    stream_player = 
    new IcecastMetadataPlayer(
        "radio/ai_radio_192", // stream endpoint
        { onMetadata }                        // options (onMetadata callback)
    );
    // const { mediasource, html5, webaudio } = IcecastMetadataPlayer.canPlayType();
    // stream_player.playbackMethod = "html5";
    stream_player.playbackMethod = "webaudio";
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
    }
    else{
        player.stop();
    }
}



