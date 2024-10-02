'''
This method is used to call part1 to part3 method. The main focus here is to automate the stuff.
'''
import os
import shutil
import time

from part1 import course_cloud_call
from part2 import text_summary
from part3 import text_speech_method
from part4 import generate_motion_videos_and_card
from main1 import video_processor
from delete_file import delete_files

delete_files()

t1 = time.time()
course_cloud_call('PRG-AU-00330698')
print("Part-01 completed.")
text_summary()
print("Part-02 completed.")
text_speech_method()
print("Part-03 completed.")


# Need to create the root folder.

CORE_FOLDER = 'src/subpart'
os.makedirs(CORE_FOLDER)
for i in range(1, 5):
    PART_NAME = 'part'+str(i)
    FOLDER_NAME = CORE_FOLDER + '/' + PART_NAME
    os.makedirs(FOLDER_NAME, exist_ok= True)
    AUDIO_FOLDER = 'src/audio/'+'audio'+str(i)+'.mp3'

    # Define the destination file path
    destination_file = os.path.join(
        FOLDER_NAME, os.path.basename(AUDIO_FOLDER))

    # Copy the file
    shutil.copy2(AUDIO_FOLDER, destination_file)

print('Folder creation part completed.')

generate_motion_videos_and_card()
print("Part-04 completed.")

video_processor()

print(time.time()-t1)
