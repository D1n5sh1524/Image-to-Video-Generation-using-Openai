# pylint: disable=unspecified-encoding

'''
This module is used to create speech file.
'''
import openai

def text_to_speech(input_text, input_file_name):
    '''
    Convert input text to speech and save the audio file.

    This function takes a string of text and converts it into speech using OpenAI's 
    text-to-speech (TTS) model. The resulting audio is saved to a specified file.

    Parameters:
    input_text (str): The text to be converted to speech.
    input_file_name (str): The name of the output audio file (excluding directory path).

    Returns:
    None
    '''
    openai.api_key = "<OpenAI KEY>"

    input1 = input_text

    input_text = input1

    response = openai.audio.speech.create(
    model="tts-1-hd",
    voice="echo",
    input=input_text
    )

    file_name = "src/audio/" + input_file_name
    response.write_to_file(file_name)

def text_speech_method():
    '''
    Convert summarized text content to speech and save the audio output to files.

    This function reads summarized text content from two files, 'university_summary_content.txt' 
    and 'course_summary_content.txt', located in the 'text' directory. It then uses the 
    'text_to_speech' function to convert the text into speech and saves the resulting audio 
    files as 'audio1.mp3' and 'audio3.mp3' in the 'audio' directory.

    This method processes two specific types of summaries: university content and course content.

    Returns:
    None
    '''

    with open('src/text/university_summary_content.txt', 'r') as file:
        uni_con = file.read()

    text_to_speech(uni_con,'audio1.mp3')

    with open('src/text/course_summary_content.txt', 'r') as file:
        uni_con = file.read()

    text_to_speech(uni_con,'audio3.mp3')
