#!/bin/sh

abc2midi $1.abc
python ../miditools/midisox_py -M $1\1.mid $1\2.mid $1\full.mid
fluidsynth -l -T raw -F - A320U.sf2 $1\full.mid -f progr0.txt -g 2 | lame -b 256 -r - $1.mp3 