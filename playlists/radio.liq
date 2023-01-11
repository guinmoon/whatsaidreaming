
#!/usr/bin/liquidsoap
# Log dir
set("log.file.path","/home/m_vs_m/whatsaidreaming/playlists/radio.log")

# Music
myplaylist = playlist(reload = 360,"/home/m_vs_m/whatsaidreaming/parts/")
radio = myplaylist

out = output.icecast(
	host = "127.0.0.1",
	port = 8000,
	user = "source",
	password = "hackme",
	name = "AI generated radio.",
	genre = "AI Ambient",
	url = "https://aliceghome.online/",
	encoding = "UTF-8"
)

# добавляем crossfade
radio = crossfade(start_next=1., fade_out=1., fade_in=1., radio)



out(
 %mp3(bitrate = 192, id3v2 = true),
 description = "MP3 192 Kbps",
 mount = "ai_radio_192",
 mksafe(radio)
)

# out(
#  %mp3(bitrate = 320, id3v2 = true),
#  description = "MP3 320 Kbps",
#  mount = "ai_radio_320",
#  mksafe(radio)
# )

# out(
#  %vorbis.abr(samplerate = 44100, channels = 1, bitrate = 128, max_bitrate = 192, min_bitrate = 96),
#  description = "Average vorbis 96-128-192 Kbps",
#  mount = "vorbis_avg_128",
#  mksafe(radio)
# )

# out(
#  %opus(samplerate = 48000, channels = 2, bitrate = 128),
#  description = "opus 128 Kbps",
#  mount = "vorbis_opus_128",
#  mksafe(radio)
# )