# pylint: disable=W1514,C0301,E0401
# pyright: reportReturnType = false
'''
This module is uses OpenAI to summarize text.
'''

from openai import OpenAI


def text_summarize_module(text) -> str:
    '''
    Summarize a given text into a single sentence using OpenAI's GPT-4 model.

    This function takes a paragraph of text as input and uses the OpenAI API to 
    generate a summarized version of the text. The summary is returned as a single 
    sentence containing between 50 to 70 words.

    Parameters:
    text (str): The input text to be summarized.

    Returns:
    str: The summarized text as a single sentence.
    '''
    client = OpenAI(
        api_key='')

    content_value = " Summarize the following paragraph into a single sentence between 50 to 70 words: " + text

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": content_value}
        ]
    )
    return response.choices[0].message.content


def text_summary():
    '''
    Summarize content from text files and save the summaries to new files.

    This function reads content from two text files, 'university_content.txt' and 
    'course_content.txt', located in the 'text' directory. It then uses the 
    'text_summarize_module' function to generate summarized versions of the content.
    The summaries are saved to 'university_summary_content.txt' and 
    'course_summary_content.txt', respectively.

    This method is called by an external method from the main.py file, which triggers 
    the summarization process.

    Returns:
    None
    '''

    with open('src/text/university_content.txt', 'r') as file:
        uni_con = file.read()

    university_summarized_content = text_summarize_module(uni_con)
    with open('src/text/university_summary_content.txt', 'w') as file:
        file.write(university_summarized_content)

    with open('src/text/course_content.txt', 'r') as file:
        cou_con = file.read()

    course_summarized_content = text_summarize_module(cou_con)
    with open('src/text/course_summary_content.txt', 'w') as file:
        file.write(course_summarized_content)
