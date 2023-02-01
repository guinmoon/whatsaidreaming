#!/bin/sh

abc2midi $1.abc
python3 ../miditools/midisox_py -M $1\1.mid $1\2.mid $1\full.mid