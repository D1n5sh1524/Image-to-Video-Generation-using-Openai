'''
This method is used to add the IDP watermark to the video.
'''

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip


def watermark_addition():
    '''
     Add a watermark to a video clip.

    This function loads a video clip ('output_video_with_bg.mp4') and an image file
    ('idp-logo-white.png') containing the watermark. The image file is set to be semi-transparent
    and resized to match the duration of the video. The watermark position is defined by the 
    'set_watermark_position' function. The watermark is then overlaid onto the video clip using
    CompositeVideoClip. The resulting video, with the watermark 
    added, is saved as 'final_video.mp4' with a higher bitrate and the H.264 codec.

    Parameters:
    None

    Returns:
    None
    '''
    video_clip = VideoFileClip("src/output_video_with_bg.mp4")

    image_clip = ImageClip(
        "image-collection/idp-logo-white.png").set_opacity(0.5).set_duration(video_clip.duration)

    def set_watermark_position(t):
        '''
        This method return the watermark position.
        '''
        return 1150, 10

    image_clip = image_clip.set_position(set_watermark_position)
    final_clip = CompositeVideoClip([video_clip, image_clip])

    bitrate = '8000k'  # Higher bitrate
    codec = 'libx264'  # H.264 codec

    final_clip.write_videofile("final_videos/final_video.mp4", bitrate=bitrate, codec=codec)
