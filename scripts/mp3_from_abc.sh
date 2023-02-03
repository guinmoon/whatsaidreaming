#!/bin/sh

abc2midi $1.abc
python3 ../miditools/midisox_py -M $1\1.mid $1\2.mid $1\full.mid
fluidsynth -l -T raw -F - ../synth/guinmoon.sf2 $1\full.mid -f ../synth/cur_prog.txt -g 0.5 | lame --tt "$2" -b 256 -r - $1.mp3 
rm $1\1.mid $1\2.mid $1\full.mid
mv $1.mp3 ../parts