fluidsynth "A320U.sf2" 2023-01-23_14_56_101.mid -g 2


python miditools/midisox_py -m 2023-01-24_21_42_391.mid 2023-01-24_21_42_392.mid 2023-01-24_21_42_393.mid
fluidsynth "A320U.sf2" 2023-01-24_15_28_151.mid -g 2 -i -f progr0.txt -nli -r 48000 -o synth.cpu-cores=2 -T oga -F example.ogg

player_start
player_stop

inst 1

prog 0 10


interesting 
piano: 5, 8, 11, 100
fx: 32, 33, 39, 44, 45, 48, 49, 50, 52, 53, 55, 63, 73, 74, 78, 86, 88, 
fx2: 89, 92
fx3: 96
guitar: 24