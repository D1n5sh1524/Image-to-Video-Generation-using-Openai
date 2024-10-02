'''
This method is used to delete all the files which was created for the
next iteration to start.
'''

import os
import shutil

def delete_files():

    file_paths = ['src/audio_generated.wav', 'src/final_video.mp4', 'src/final1.mp4',
                'src/output_video_with_bg.mp4', 'src/output_video.mp4', 'src/sub_tittle_en.srt',
                'src/audio/audio1.mp3','src/audio/audio3.mp3']

    for files in file_paths:
        if os.path.exists(files):
            os.remove(files)
            print(f"File '{files}' deleted successfully.")

    # Deleting the subpart folder.
    DELETE_FOLDER = 'src/subpart'
    if os.path.exists(DELETE_FOLDER):
        shutil.rmtree(DELETE_FOLDER)

    # Deleting all the files from resultant folder.
    DELETE_FOLDER2 = ['src/resultant', 'src/text']
    for folder in DELETE_FOLDER2:
        for filename in os.listdir(folder):
            if folder=='src/resultant' and filename not in ['resultant.mp4','resultant5.mp4']:
                file_path = os.path.join(folder,filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            elif folder=='src/text':
                file_path = os.path.join(folder,filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
