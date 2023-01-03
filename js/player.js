$(document).ready(function(){
    wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: '#7987b5',
        progressColor: 'purple',
        barWidth:3,
        responsive:true

    });
    wavesurfer.load('/parts/2.mp3');
    // wavesurfer.playPause();
});
