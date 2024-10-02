'''
This will be used when concatenating movies.
'''

import os
from moviepy.editor import VideoFileClip, concatenate_videoclips


def video_concat():
    '''
    Concatenate multiple video files from a resultant directory into a 
    single video file with transitions.

    This function reads all MP4 video files from the resultant directory, concatenates them with 
    transition effects, and saves the resulting video as 'resultant.mp4' in the main directory.

    Returns:
    None
    '''
    # Load the video file
    path_name = "src/resultant"
    file_paths = []
    if os.path.exists(path_name):
        file_paths = [os.path.join(path_name, f) for f in os.listdir(
            path_name) if f.endswith(".mp4")]

    # Load video clips
    video_clips = [VideoFileClip(fp) for fp in file_paths]

    # Add transistion effect and concatenate the resultant video clips
    transition_duration = 1  # Duration of the transition effect in seconds
    final_clip = concatenate_with_transition(file_paths, transition_duration)

    # Write the final video to a file
    video_path = "src/final1.mp4"

    # Write the concatenated video to a file
    final_clip.write_videofile(video_path,
                               codec="libx264",
                               audio_codec="aac",
                               fps=60,
                               bitrate='8000k'
                               )

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
