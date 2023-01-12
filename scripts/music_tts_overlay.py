# Requires pydub (with ffmpeg) and Pillow
#
# Usage: python waveform.py <audio_file>

import sys,os

from pydub import AudioSegment
from PIL import Image, ImageDraw


class Overlay(object):

    bar_count = 400
    db_ceiling = 140

    def __init__(self, filename):
        self.filename = filename

        audio_file = AudioSegment.from_file(
            self.filename, self.filename.split('.')[-1])

        self.peaks = self._calculate_peaks(audio_file)

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

    def _generate_waveform_image(self):
        """ Returns the full waveform image """
        im = Image.new('RGB', (3200, 300), '#f5f5f5')
        min_peak= self.db_ceiling
        max_peak= -self.db_ceiling
        for index, value in enumerate(self.peaks, start=0):
            if value<min_peak and value!=0:
                min_peak=value
            if value>max_peak:
                max_peak=value
        avg_peak = (min_peak+max_peak)/2.5
        index_beg=0
        index_end=0
        longest_index_beg=0
        longest_index_end=0
        max_lowest_len=0
        prev_check=False
        for index, value in enumerate(self.peaks, start=0):
            column = index * 8 + 2
            upper_endpoint = 140 - value
            if value<avg_peak:                            
                if not prev_check:
                    index_beg = index
                prev_check = True
                index_end = index
                im.paste(self._get_bar_image((4, value * 2), '#3152c0'),
                        (column, upper_endpoint))    
            else:                
                if index_end-index_beg>max_lowest_len:
                    max_lowest_len = index_end-index_beg
                    longest_index_beg = index_beg
                    longest_index_end = index_end
                prev_check=False
                im.paste(self._get_bar_image((4, value * 2), '#424242'),
                            (column, upper_endpoint))
        if index_end-index_beg>max_lowest_len:
            max_lowest_len = index_end-index_beg
            longest_index_beg = index_beg
            longest_index_end = index_end
        for index, value in enumerate(self.peaks, start=0):
            column = index * 8 + 2
            upper_endpoint = 140 - value
            if index>=longest_index_beg and index<longest_index_end:
                im.paste(self._get_bar_image((4, value * 2), '#489e2d'),
                        (column, upper_endpoint))
        return im

    def save(self):
        """ Save the waveform as an image """
        png_filename = self.filename.replace(
            self.filename.split('.')[-1], 'png')
        with open(png_filename, 'wb') as imfile:
            self._generate_waveform_image().save(imfile, 'PNG')


if __name__ == '__main__':
    filename = os.path.join(os.path.dirname(__file__),'../parts/2.mp3')

    waveform = Overlay(filename)
    waveform.save()