# Requires pydub (with ffmpeg) and Pillow
#
# Usage: python waveform.py <audio_file>

import sys,os

from pydub import AudioSegment
from PIL import Image, ImageDraw


class Overlay(object):

    bar_count = 800
    db_ceiling = 140

    def __init__(self, filename,bar_count=800):
        self.filename = filename
        self.bar_count=bar_count
        self.audio_file = AudioSegment.from_file(
            self.filename, self.filename.split('.')[-1])
        self.peaks = self._calculate_peaks(self.audio_file)

    def _calculate_peaks(self, audio_file):
        """ Returns a list of audio level peaks """
        chunk_length = len(audio_file) / self.bar_count

        loudness_of_chunks = [
            audio_file[i * chunk_length: (i + 1) * chunk_length].rms
            for i in range(self.bar_count)]

        max_rms = max(loudness_of_chunks) * 1.00

        return [int((loudness / max_rms) * self.db_ceiling)
                for loudness in loudness_of_chunks]

    def _get_bar_image(self, size, fill):
        """ Returns an image of a bar. """
        width, height = size
        bar = Image.new('RGBA', size, fill)

        end = Image.new('RGBA', (width, 2), fill)
        draw = ImageDraw.Draw(end)
        draw.point([(0, 0), (3, 0)], fill='#3152c0')
        draw.point([(0, 1), (3, 1), (1, 0), (2, 0)], fill='#555555')

        bar.paste(end, (0, 0))
        bar.paste(end.rotate(180), (0, height - 2))
        return bar

    def _generate_waveform_image(self,avg_koev):
        """ Returns the full waveform image """
        # (255, 255, 255, 0)
        # #489e2d green
        # #4a3fe2 blue

        koef = len(self.audio_file)/self.bar_count
        im = Image.new('RGB', (self.bar_count*8, 300), '#f5f5f5')
        min_peak= self.db_ceiling
        max_peak= -self.db_ceiling
        for index, value in enumerate(self.peaks, start=0):
            if value<min_peak and value!=0:
                min_peak=value
            if value>max_peak:
                max_peak=value
        avg_peak = (min_peak+max_peak)/avg_koev
        for index, value in enumerate(self.peaks, start=0):
            column = index * 8 + 2
            upper_endpoint = 140 - value
            if value<avg_peak:
                im.paste(self._get_bar_image((4, value * 2), '#4a3fe2'),
                            (column, upper_endpoint))
            else:
                im.paste(self._get_bar_image((4, value * 2), '#424242'),
                            (column, upper_endpoint))
            

        overlay_poss=self.get_best_overlay_places(avg_koev,3,1)
        overlay_pos=overlay_poss[0]
        for tmp_pos in overlay_poss:
            if tmp_pos[4]>overlay_pos[4]:
                overlay_pos=tmp_pos
        for index, value in enumerate(self.peaks, start=0):
            column = index * 8 + 2
            upper_endpoint = 140 - value
            # fulls_ind=index*koef
            fulls_ind=index
            if fulls_ind>=overlay_pos[0] and fulls_ind<=overlay_pos[1]:
                im.paste(self._get_bar_image((4, value * 2), '#489e2d'),
                    (column, upper_endpoint))
                    
                
        return im

    def get_best_overlay_places(self,avg_koev,len_coef,dist_coef):
        min_peak= self.db_ceiling
        max_peak= -self.db_ceiling
        for index, value in enumerate(self.peaks, start=0):
            if value<min_peak and value!=0:
                min_peak=value
            if value>max_peak:
                max_peak=value
        avg_peak = (min_peak+max_peak)/avg_koev
        index_beg=0
        latest_index_beg=0
        index_end=0
        longest_index_beg=0
        longest_index_end=0
        max_lowest_len=0
        half = int(len(self.peaks)/2)
        prev_check=False
        overlay_places=[]
        overlay_places.append((index_beg,index_end,
                                (index_end-index_beg),
                                (half-abs(half-index_beg)),
                                (index_end-index_beg)*len_coef+(half-abs(half-index_beg))*dist_coef))  
        for index, value in enumerate(self.peaks, start=0):
            column = index * 8 + 2
            upper_endpoint = 140 - value
            if value<avg_peak:                            
                if not prev_check:
                    index_beg = index
                prev_check = True 
                index_end = index
            else:   
                if latest_index_beg!=index_beg:
                    overlay_places.append((index_beg,index_end,
                                            (index_end-index_beg),
                                            (half-abs(half-index_beg)),
                                            (index_end-index_beg)*len_coef+(half-abs(half-index_beg))*dist_coef))             
                    latest_index_beg = index_beg
                if index_end-index_beg>max_lowest_len:
                    max_lowest_len = index_end-index_beg
                    longest_index_beg = index_beg
                    longest_index_end = index_end
                prev_check=False
        overlay_places.append((index_beg,index_end,
                        (index_end-index_beg),
                        (half-abs(half-index_beg)),
                        (index_end-index_beg)*len_coef+(half-abs(half-index_beg))*dist_coef))  

        
        # begin_overlay = int(longest_index_beg*koef)
        return overlay_places

    def add_overlay(self,overlay_filename,avg_koev,fade_len):
        self.overlay_filename = overlay_filename
        self.overlay_file = AudioSegment.from_file(
            self.overlay_filename, self.overlay_filename.split('.')[-1])
        overlay_poss=self.get_best_overlay_places(avg_koev,3,1)
        overlay_pos=overlay_poss[0]
        for tmp_pos in overlay_poss:
            if tmp_pos[4]>overlay_pos[4]:
                overlay_pos=tmp_pos
        koef = len(self.audio_file)/self.bar_count
        overlay_pos = int(overlay_pos[0]*koef)
        orig_len=len(self.audio_file)
        new_len=overlay_pos+len(self.overlay_file)
        if new_len>orig_len:
            self.audio_with_overlay = self.audio_file.append(self.overlay_file,crossfade=new_len-orig_len)    
        else:
            self.overlay_file = self.overlay_file.fade_in(duration=fade_len)
            self.audio_with_overlay = self.audio_file.overlay(self.overlay_file,position=overlay_pos)

    def save_waveform(self,avg_koev):
        """ Save the new audio as mp3 """
        png_filename = self.filename.replace(
            self.filename.split('.')[-1], 'png')
        with open(png_filename, 'wb') as imfile:
            self._generate_waveform_image(avg_koev).save(imfile, 'PNG')

    def seve_audio_with_overlay(self,new_filename):
        """ Save the waveform as an image """
        # new_filename = self.filename+".mp3"
        with open(new_filename, 'wb') as out_f:
            self.audio_with_overlay.export(out_f, format='mp3',bitrate="192k")


if __name__ == '__main__':
    # filename = os.path.join(os.path.dirname(__file__),'../parts/2023-01-09_21_26_33.mp3')
    # overlay_filename = os.path.join(os.path.dirname(__file__),'../parts/1.mp3')
    
    avg_koef=1.8
    filename = sys.argv[1]
    overlay_filename = sys.argv[2]
    new_filename = sys.argv[3]

    # parsed_wave = Overlay(filename,600)
    # parsed_wave.save_waveform(avg_koef)
    # exit(0)

    parsed_wave = Overlay(filename)
    parsed_wave.add_overlay(overlay_filename,avg_koef,2000)
    parsed_wave.seve_audio_with_overlay(new_filename)
    if len(sys.argv)>4 and sys.argv[4]=='-w':
        parsed_wave = Overlay(filename)
        parsed_wave.save_waveform(avg_koef)
        parsed_wave = Overlay(overlay_filename)
        parsed_wave.save_waveform(avg_koef)
        parsed_wave = Overlay(new_filename)
        parsed_wave.save_waveform(avg_koef)