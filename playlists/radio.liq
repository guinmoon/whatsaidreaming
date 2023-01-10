
#!/usr/bin/liquidsoap
# Log dir
set("log.file.path","/home/m_vs_m/whatsaidreaming/playlists/basic-radio.log")

# Music
myplaylist = playlist(reload = 60,"/home/m_vs_m/whatsaidreaming/parts/")
# Some jingles
#jingles = playlist("~/radio/jingles.m3u")
# If something goes wrong, we'll play this
#security = single("~/radio/sounds/default.ogg")

# Start building the feed with music
radio = myplaylist
# Now add some jingles
#radio = random(weights = [1, 4],[jingles, radio])
# And finally the security
#radio = fallback(track_sensitive = false, [radio, security])

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


#out(
# %fdkaac(channels=2, samplerate=44100, bandwidth="auto", bitrate=64, afterburner=false, aot="mpeg2_he_aac_v2", transmux="adts", sbr_mode=false),
# description = "FDKAAC",
# mount = "ai_radio_aac",
# mksafe(radio)
#)

#out(
# %opus(samplerate=48000),
# description = "OPUS",
# mount = "ai_radio_opus",
# mksafe(radio)
#)

#out(
#	%vorbis.abr(samplerate = 44100, channels = 1, bitrate = 128, max_bitrate = 192, min_bitrate = 96),
#	description = "Average vorbis 96-128-192 Kbps",
#	mount = "ai_radio_vorbis_avg",
#	mksafe(radio)
#)

radio = crossfade(start_next=1., fade_out=1., fade_in=1., radio)
 
out(
	%mp3(bitrate = 192, id3v2 = true),
	description = "MP3 192 Kbps",
	mount = "ai_radio_192",
	mksafe(radio)
)

#out(
#       %vorbis.abr(samplerate = 44100, channels = 1, bitrate = 128, max_bitrate = 192, min_bitrate = 96),
#       description = "Average vorbis 96-128-192 Kbps",
#       mount = "ai_radio_vorbis_avg",
#       mksafe(radio)
#)


