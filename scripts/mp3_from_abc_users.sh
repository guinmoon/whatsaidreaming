#!/bin/sh

pkill lame
../abcm2ps/abcm2ps -X $1.abc -O ../output_tunes/$2.svg
abc2midi $1.abc
# python3 ../miditools/midisox_py -M $1\1.mid $1\2.mid $1\3.mid $1\full.mid
python3 ../miditools/midisox_py -M $1\1.mid $1\full.mid
fluidsynth -l -T raw -F - ../synth/guinmoon.sf2 $1\full.mid -f ../synth/cur_prog.txt -g 0.5 | lame --tt "$3" -b 256 -r - ../output_tunes/$2.mp3 
# rm $1\1.mid $1\2.mid $1\3.mid $1\full.mid
rm $1\1.mid $1\full.mid