# pylint: disable=all
import math
import ffmpeg
import subprocess

from faster_whisper import WhisperModel


def cc_addition():
    '''
    This method is used to add the caption to the video we have created.
    '''
    input_video = "src/final1.mp4"
    input_video_name = input_video.replace(".mp4", "")

    def extract_audio():
        ffmpeg_executable = "ffmpeg/ffmpeg.exe"
        extracted_audio = f"src/audio_generated.wav"
        stream = ffmpeg.input(input_video)
        stream = ffmpeg.output(stream, extracted_audio)

        result = subprocess.run([ffmpeg_executable, '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())

        ffmpeg.run(stream, cmd=ffmpeg_executable, overwrite_output=True)
        return extracted_audio

    def transcribe(audio):
        model = WhisperModel("small")
        segments, info = model.transcribe(audio)
        language = info[0]
        print("Transcription language", info[0])
        segments = list(segments)
        return language, segments

    def format_time(seconds):

        hours = math.floor(seconds / 3600)
        seconds %= 3600
        minutes = math.floor(seconds / 60)
        seconds %= 60
        milliseconds = round((seconds - math.floor(seconds)) * 1000)
        seconds = math.floor(seconds)
        formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

        return formatted_time

    def generate_subtitle_file(language, segments):

        subtitle_file = f"src/sub_tittle_{language}.srt"
        text = ""
        for index, segment in enumerate(segments):
            segment_start = format_time(segment.start)
            segment_end = format_time(segment.end)
            text += f"{str(index+1)} \n"
            text += f"{segment_start} --> {segment_end} \n"
            text += f"{segment.text} \n"
            text += "\n"

        f = open(subtitle_file, "w")
        f.write(text)
        f.close()

        return subtitle_file

    def add_subtitle_to_video(soft_subtitle, subtitle_file,  subtitle_language):

        ffmpeg_executable = "ffmpeg/ffmpeg.exe"
        video_input_stream = ffmpeg.input(input_video)
        subtitle_input_stream = ffmpeg.input(subtitle_file)
        output_video = "src/output_video.mp4"
        subtitle_track_title = subtitle_file.replace(".srt", "")

        if soft_subtitle:
            stream = ffmpeg.output(
                video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
                **{"metadata:s:s:0": f"language={subtitle_language}",
                   "metadata:s:s:0": f"title={subtitle_track_title}"}
            )
            ffmpeg.run(stream, cmd=ffmpeg_executable, overwrite_output=True)

        else:
            stream = ffmpeg.output(video_input_stream, output_video,

                                   vf=f"subtitles={subtitle_file}")

            ffmpeg.run(stream, cmd=ffmpeg_executable, overwrite_output=True)

    def run():

        extracted_audio = extract_audio()
        language, segments = transcribe(audio=extracted_audio)
        subtitle_file = generate_subtitle_file(
            language=language,
            segments=segments
        )
        add_subtitle_to_video(
            soft_subtitle=False,
            subtitle_file=subtitle_file,
            subtitle_language=language
        )

    run()
