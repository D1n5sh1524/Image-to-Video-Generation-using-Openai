# pylint: disable=C0114,C0116
'''
Add audio to the video file.
'''

import os
import numpy as np
from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.editor import AudioFileClip, concatenate_audioclips, VideoFileClip


def audio_addition(audio_path, file_name, video_path):
    '''
    Combines the video and audio file.

    This function combines the audio and video file to a single file. The main logic here is
    fixing the duration difference between the files. In case if audio is greater than video
    then we are keeping the last frame for the extended audio and in case if video is greater
    than audio then we are forming the subclip with the audio duration. The file will be
    saved as rseultant[i].mp4 in the resultant folder.

    Parameters:
    audio_path (str): The directory path where the input audio file is present.
    file_name (str): The directory path where we want my output video to be saved.
    video_path (str): The directory path where the input video file is present.

    Returns:
    None
    '''
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Load the audio clip
    audio_clip = AudioFileClip(audio_path)

    # Get the duration of the audio clip
    audio_duration = audio_clip.duration

    # Calculate the difference in duration between audio and video
    duration_difference = audio_duration - video_clip.duration

    # Write the final video to a file
    video_path = file_name

    # If the duration difference is positive, extend the video clip
    if duration_difference > 0:
        # Extend the duration of the video clip by appending black frames
        extended_video_clip = video_clip.set_duration(
            video_clip.duration + duration_difference)

        # Set the audio of the extended video clip to the audio clip
        extended_video_clip = extended_video_clip.set_audio(audio_clip)

        # Write the final video with extended duration and audio
        extended_video_clip.write_videofile(
            video_path,
            codec="libx264",
            audio_codec="aac",
            fps=60,
            bitrate='8000k'
        )
    else:
        duration_diff = abs(duration_difference)
        silent_audio = AudioArrayClip(
            np.zeros((int(duration_diff * audio_clip.fps), 2)), fps=audio_clip.fps)
        padded_audio = concatenate_audioclips([audio_clip, silent_audio])

        final_video = video_clip.set_audio(padded_audio)

        final_video.write_videofile(
            video_path,
            codec='libx264',
            audio_codec='aac',
            fps=60,
            bitrate='8000k'
        )


def audio_addition_module():
    '''
    Call the audio_addition function for each relevant video and audio file in subdirectories.

    This function defines a root directory ('subpart'), retrieves a list of all subdirectories
    within it, and then processes each subdirectory. For each subdirectory, it identifies video 
    files that start with "step2" and audio files that end with ".mp3". It then calls the 
    'audio_addition' function to combine the video and audio into a single video file. The 
    resultant video files are saved into a 'resultant' directory with filenames based on the 
    subdirectory names.

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
        video_path = [os.path.join(folder, f) for f in os.listdir(
            folder) if f.startswith("step2")]
        audio_path = [os.path.join(folder, f) for f in os.listdir(
            folder) if f.endswith(".mp3")]
        file_name = 'src/resultant/resultant'+folder[-1]+'.mp4'
        audio_addition(audio_path[0],file_name,video_path[0])
