'''
This method is used to call video_part1 to video_part7 method. 
The main focus here is to automate the stuff.
'''

import time

from video_part1 import video_concat_module
from video_part2 import size_fixer_module
from video_part3 import audio_addition_module
from video_part4 import video_concat
from video_part5 import cc_addition
from video_part6 import music_addition
from video_part7 import watermark_addition



def video_processor():
    video_concat_module()
    print("Initial video concat process completed.")

    size_fixer_module()
    print("Video frame size fix part completed.")

    audio_addition_module()
    print("Speech to the video addition part completed and files created in resultant folder.")

    video_concat()
    print("Overall video concatenation part completed.")

    cc_addition()
    print("Caption addition part completed.")

    music_addition()
    print("Background addition music part completed.")

    watermark_addition()
    print("Watermark addition completed. Final video is ready.")