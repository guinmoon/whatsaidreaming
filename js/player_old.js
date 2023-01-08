$(document).ready(function(){
    wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: '#7987b5',
        progressColor: 'purple',
        barWidth:3,
        responsive:true

    });
    wavesurfer.load('http://185.228.233.129:8000/HabraRadio_320');
    // wavesurfer.playPause();
});
