'''
This python file is used to add music to the video created in previous step.
'''

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


def music_addition():
    '''
    Add background music to a video clip.

    This function loads a video clip ('output_video.mp4') and a new audio clip ('music.mp3').It then 
    trims the new audio to match the duration of the video, reduces its volume, fades it in, and
    overlays it with the existing audio from the video.The final composite audio is set as the audio
    of the video clip, and the video clip with the updated audio is saved as
    'output_video_with_bg.mp4'.

    Parameters:
    None

    Returns:
    None
    '''
    # Load your video clip
    video_clip = VideoFileClip("src/output_video.mp4")

    # Load your existing audio from the video clip
    existing_audio = video_clip.audio

    # Load your new audio clip
    new_audio = AudioFileClip("src/audio/music.mp3")

    # Trim the new audio to match the duration of the video
    new_audio_trimmed = new_audio.subclip(0, video_clip.duration)

    # Reduce the frequency of the trimmed new audio (optional)
    # You can use the .fx function to apply a filter to the audio
    # For example, to reduce the frequency by a factor of 0.1 (half the frequency):
    new_audio_low_vol = new_audio_trimmed.volumex(0.05)

    # Fade in the new audio
    new_audio_fadein = new_audio_low_vol.audio_fadein(1)

    # Overlay the new audio with the existing audio
    final_audio = CompositeAudioClip([existing_audio, new_audio_fadein])

    # Set the audio of the video clip to the final composite audio
    video_clip = video_clip.set_audio(final_audio)

    # Write the video clip with the updated audio
    video_clip.write_videofile(
        "src/output_video_with_bg.mp4", codec="libx264", audio_codec="aac", fps=60, bitrate='8000k')
