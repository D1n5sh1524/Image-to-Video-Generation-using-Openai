'''
This function reads all MP4 video files from the given directory, concatenates them with 
transition effects, and saves the resulting video as 'step1.mp4' in the same directory.
'''

import os
from moviepy.editor import VideoFileClip, concatenate_videoclips


def video_concat(input_path_name):
    '''
    Concatenate multiple video files from a specified directory into a 
    single video file with transitions.

    This function reads all MP4 video files from the given directory, concatenates them with 
    transition effects, and saves the resulting video as 'step1.mp4' in the same directory.

    Parameters:
    input_path_name (str): The path to the directory containing the video files to be concatenated.

    Returns:
    None
    '''
    path_name = input_path_name
    # Load the video file
    file_paths = []
    if os.path.exists(path_name):
        file_paths = [os.path.join(path_name, f) for f in os.listdir(
            path_name) if f.endswith(".mp4")]

    # Load video clips
    video_clips = [VideoFileClip(fp) for fp in file_paths]

    # # Concatenate video clips
    # final_clip = concatenate_videoclips(video_clips)

    # Add transistion effect and concatenate the resultant video clips
    transition_duration = 1.5  # Duration of the transition effect in seconds
    final_clip = concatenate_with_transition(file_paths, transition_duration)

    # Write the final video to a file
    file_name = "step1.mp4"

    video_path = os.path.join(path_name, file_name)

    # Write the concatenated video to a file
    final_clip.write_videofile(video_path, codec='libx264',
                               audio_codec='aac')

    # Close the video clips
    for clip in video_clips:
        clip.close()


def add_transition(clip1, clip2, transition_duration):
    '''
    Add a transition effect between two video clips.

    This function adds a fade-out effect to the end of the first video clip ('clip1')
    and a fade-in effect to the beginning of the second video clip ('clip2'). The duration 
    of the transition effect is specified by `transition_duration`. The two clips are 
    then concatenated to create a seamless transition.

    Parameters:
    clip1 (VideoFileClip): The first video clip.
    clip2 (VideoFileClip): The second video clip.
    transition_duration (int or float): The duration of the transition effect in seconds.

    Returns:
    VideoFileClip: A new video clip with the transition effect applied.
    '''

    # Fade out the end of clip1
    transition_clip1 = clip1.fadeout(transition_duration)
    # Fade in the beginning of clip2
    transition_clip2 = clip2.fadein(transition_duration)
    # Combine the transition clips
    return concatenate_videoclips([transition_clip1, transition_clip2])


def concatenate_with_transition(video_files, transition_duration):
    '''
    Concatenate a list of video files with transition effects between each pair of clips.

    This function takes a list of video file paths and a specified transition duration.
    It reads each video file, applies a transition effect between each pair of video clips,
    and concatenates them into a single final video clip.

    Parameters:
    video_files (list of str): A list of file paths to the video files to be concatenated.
    transition_duration (int or float): The duration of the transition effect in seconds.

    Returns:
    VideoFileClip: A new video clip with all the input videos concatenated with transitions.
    '''
    clips = []
    for file in video_files:
        clip = VideoFileClip(file)
        clips.append(clip)
    # Apply transition effect between each pair of clips
    final_clip = clips[0]
    for i in range(1, len(clips)):
        final_clip = add_transition(final_clip, clips[i], transition_duration)
    return final_clip


def video_concat_module():
    '''
    Call the core video concatenation method on specific subdirectories.

    This function defines the root directory and retrieves a list of all subdirectories
    within it. It then calls the 'video_concat' function on each subdirectory, excluding 
    those whose names start with 'part2' or 'part4'. The 'video_concat' function is 
    expected to perform the core video concatenation tasks on the contents of each 
    specified subdirectory.

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
        if not (folder.startswith('part2') or folder.startswith('part4')):
            video_concat(folder)
