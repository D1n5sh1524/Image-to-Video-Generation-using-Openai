# pylint: disable=C0301, C0103, E1121, W1514
'''
This python file consists of all the codes related to calling Course Cloud and creating the
txt file for university and course summary.
'''
import json
import re
from datetime import datetime

import requests


def remove_html_tags_and_escape_sequences(text):
    """
    Remove HTML tags and escape sequences from a given text.

    This function removes all HTML tags from the input text using a regular expression.
    It also removes newline ('\n') and tab ('\t') escape sequences. The cleaned text
    is then stripped of any leading or trailing whitespace.

    Parameters:
    text (str): The input text containing HTML tags and escape sequences.

    Returns:
    str: The cleaned text with HTML tags and escape sequences removed.
    """
    clean = re.compile('<.*?>')
    text_without_tags = re.sub(clean, '', text)
    text_without_escape_sequences = text_without_tags.replace(
        '\n', '').replace('\t', '')
    return text_without_escape_sequences.strip()


def date_sorter(input_dates):
    '''
    Sort a list of dates in the format "dd.mm.yyyy" and return the earliest date.

    This function takes a list of date strings, converts them to datetime objects,
    sorts them in ascending order, and then returns the earliest date as a string
    in the original format.

    Parameters:
    input_dates (list of str): A list of date strings in the format "dd.mm.yyyy".

    Returns:
    str: The earliest date in the list, formatted as "dd.mm.yyyy".
    '''
    # Convert string dates to datetime objects
    date_format = "%d.%m.%Y"
    dates = [datetime.strptime(date, date_format) for date in input_dates]

    # Sort the dates
    dates.sort()

    # Convert datetime objects back to string format
    sorted_next_intake_list = [datetime.strftime(
        date, date_format) for date in dates]
    return sorted_next_intake_list[0]


def course_cloud_call(program_id):
    '''
    This method calls the Course Cloud API and creates the respective text files.

    This function takes program_id as input and calls the Course Cloud get courses
    end point and fetches the details from there and creates a university_content.txt
    file and course_content file under text folder and also creates a course_details.json
    file which has the necessary course specific details.

    Parameters:
    program_id (str): Input program id.

    Returns:
    None: This function does it's function and will not return anything.
    '''

    PRE_URL = "https://qpbm7v1pv6.execute-api.ap-southeast-1.amazonaws.com/prd/v1/courses?courseId="
    URL = PRE_URL + program_id

    headers = {'x-api-key': 'lTwecE3FGk1XDIAqxX9AV7scyP2lpP7e17uK6HjT'}

    response = requests.get(url=URL, headers=headers, timeout=None)
    uni_response = response.json()
    uni_content = remove_html_tags_and_escape_sequences(
        uni_response['institution']['attributes'][0].get('idpProfile', ''))

    with open('src/text/university_content.txt', 'w', encoding='utf-8') as f:
        f.write(uni_content)

    # For getting the Course details from CC.
    course_details = {}

    cou_response = response.json()
    cou_content = remove_html_tags_and_escape_sequences(
        cou_response['attributes'][0].get('courseSummary', ''))
    if not cou_content:
        cou_content = remove_html_tags_and_escape_sequences(
            cou_response['attributes'][0].get('programDescription', ''))

    with open('src/text/course_content.txt', 'w', encoding='utf-8') as f:
        f.write(cou_content)

    course_details['university_name'] = cou_response['institution']['attributes'][0]['displayName']
    course_details['location'] = cou_response['institution']['attributes'][0]['countryName']
    course_details['location'] = 'UK' if course_details['location'] == 'United Kingdom' else course_details['location']
    course_details['course_name'] = cou_response['idpCourseTitle']
    course_details['ielts_score'] = cou_response['attributes'][0]['ieltsScore']+' IELTS'
    course_details['is_scholarship_avilable'] = 'Available' if cou_response['attributes'][0]['scholarshipAvailable'] is True else 'N/A'
    course_details['is_internship_avilable'] = 'Available' if cou_response['attributes'][0]['internshipAvailable'] is True else 'N/A'

    # For finding the annual fee, Duration for the upcoming course. I am going to iterate through the course availabilty key.
    next_intake_list = []
    course_availability = cou_response['courseAvailability']
    for ind_availabilty in course_availability:
        commencement_date = ind_availabilty['attributes'][0].get(
            'commencementDate', '')
        if commencement_date not in ('', '', 'NA'):
            next_intake_list.append(commencement_date)

    next_intake_date = ''
    if next_intake_list:
        next_intake_date = date_sorter(next_intake_list)

    if next_intake_date:
        for ind_availabilty in course_availability:
            if ind_availabilty['attributes'][0].get('commencementDate', '') == next_intake_date:
                fee = int(ind_availabilty['attributes'][0].get('annualFee', 0))
                currency = ind_availabilty['attributes'][0].get('currency', 0)
                annual_fee = currency + ' ' + "{:,}".format(fee)
                course_details['annual_fee'] = annual_fee
                course_details['duration'] = ind_availabilty['attributes'][0].get(
                    'durationOfStudy', '')

    with open('src/text/course_details.json', 'w') as fx:
        json.dump(course_details, fx, indent=2)
