abc2midi $1.abc
python ../miditools/midisox_py -M $1\1.mid $1\2.mid $1\full.mid
fluidsynth "A320U.sf2" $1\full.mid -g 2 -i -f progr0.txt -nli -r 48000 -o synth.cpu-cores=8 -T oga -F $1.ogg