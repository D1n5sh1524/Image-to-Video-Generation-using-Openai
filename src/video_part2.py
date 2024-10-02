'''
This is used to fix the size of the video to the constant value.
'''

import os
from moviepy.editor import VideoFileClip


def size_fixer(file_name, path):
    '''
    Set the frame rate and resize the frames of a video file.

    This function adjusts the frame rate and frame size of a given video file. The video is set
    to a fixed frame rate of 60 frames per second and resized to a resolution of 1280x720 pixels.
    The processed video is then saved to a specified path with the filename 'step2.mp4'.

    Parameters:
    file_name (str): The name of the input video file.
    path (str): The directory path where the processed video will be saved.

    Returns:
    None
    '''
    video_file = VideoFileClip(file_name)

    # Sync issue fix.
    fixed_fps = 60
    fixed_size = (1280, 720)

    # Setting it to a fixed size.
    video_file = video_file.set_fps(fixed_fps)
    video_file = video_file.resize(newsize=fixed_size)

    resultant_path = path + '/step2.mp4'
    video_file.write_videofile(resultant_path, codec='libx264',
                               audio_codec='aac')


def size_fixer_module():
    '''
    Call the size_fixer function for each relevant video file in subdirectories.

    This function defines a root directory ('subpart'), retrieves a list of all subdirectories
    within it, and then processes each subdirectory.For each subdirectory, it identifies video files
    that start with "step1" and calls the `size_fixer` function on these files to set the frame rate 
    and resize the frames. The processed videos are saved back into their respective subdirectories.

    Parameters:
    None

    Returns:
    None
    '''
    # Define the root directory
    root_directory = 'src/subpart'

    # Get a list of all subdirectories in the root directory with full paths
    subfolders = [os.path.join(root_directory, name) for name in os.listdir(
        root_directory) if os.path.isdir(os.path.join(root_directory, name))]

    for folder in subfolders:
        file_paths = [os.path.join(folder, f) for f in os.listdir(
            folder) if f.startswith("step1")]
        size_fixer(file_paths[0], folder)
