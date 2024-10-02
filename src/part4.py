
import json
import random
import re

import cv2
from Constants import OPENAI_API_KEY
from moviepy.editor import *
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

client = OpenAI(api_key=OPENAI_API_KEY)
university_list = {
    "University of Plymouth":3758

}


def generate_course_card(course_details):
    """
    Generate a course card with the given course details.

    Parameters:
        course_details (dict): A dictionary containing the course details.
    """
    course_card_temp = "image-collection/course_card_temp.png"
    course_card = "image-collection/course_card.png"

    image = Image.open(course_card_temp)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 55)
    color = (0, 0, 0)

    university = course_details["university_name"]
    course_name = course_details["course_name"]

    university_pos = (620, 715)
    course_name_pos = (520, 850)

    draw.text(university_pos, university, fill=color, font=font)
    draw.text(course_name_pos, course_name, fill=color, font=font)

    image.save(course_card)

    image_clip = ImageClip(course_card)
    video_clip = image_clip.set_duration(5)
    video_clip.write_videofile("src/subpart/part2/step1.mp4", fps=60)


def generate_course_details_card(course_details):
    """
    Generate a course details card from the given course details.

    This function takes a dictionary of course details and generates a course
    details card from it. The generated card is saved as a PNG image at
    image-collection/course_details.png.

    Parameters:
    course_details (dict): Course details dictionary.
    """
    image = Image.open("image-collection/course_details_temp.png")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("arial.ttf", 28)

    text_1 = course_details["duration"]
    text_2 = course_details["location"]
    text_3 = course_details["annual_fee"]
    text_4 = course_details["is_scholarship_available"]
    text_5 = course_details["is_internship_available"]
    text_6 = course_details["ielts_score"]

    positions = [
        (163, 100),
        (445, 100),
        (716, 100),
        (163, 277),
        (445, 277),
        (716, 277),
    ]

    for text, position in zip([text_1, text_2, text_3, text_4, text_5, text_6], positions):
        draw.text(position, text, fill=(0, 0, 0), font=font)

    image.save("image-collection/course_details.png")

    background = Image.open("image-collection/course_details_bg.png")
    overlay = Image.open("image-collection/course_details.png")
    overlay = overlay.resize((1100, 460))
    position = (100, 200)
    background.paste(overlay, position, overlay)
    background.save("image-collection/course_details.png")

    image_clip = ImageClip("image-collection/course_details.png")
    video_clip = image_clip.set_duration(5)
    video_clip.write_videofile("src/subpart/part4/step1.mp4", fps=60)


def suggest_images(institution_name, institution_content, course_content):
    """
    Suggest image ids based on content for a given institution and course.

    Args:
        institution_name (str): Name of the institution.
        institution_content (str): Content of the institution.
        course_content (str): Content of the course.

    Returns:
        tuple: A tuple of two lists of image ids, one for the institution and one for the course.
    """
    file_id = None

    with open(
            f"image-collection/Image-json/{institution_name}_image.json", "rb") as file:
        file_id = client.files.create(
            file=file, purpose='assistants').id


    assistant = client.beta.assistants.create(
        name="Data visualizer",
        description="You are an expert in analysing images with image description in the json file and recommending  appropriate image ids based the content provided for creation.",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
        tool_resources={
            "code_interpreter": {
                "file_ids": [file_id]
            }
        }
    )

    # for university content
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"Suggest 5 image ids based on the below content - {institution_content}",
                "attachments": [
                    {
                        "file_id": file_id,
                        "tools": [{"type": "file_search"}]
                    }
                ]
            }
        ]
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(
        thread_id=thread.id, run_id=run.id))
    institution_image_ids = re.findall(
        r'\d+-\d+', messages[0].content[0].text.value)

    # for course content
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"Suggest 5 image ids  for below content - {course_content} .And do not include these image ids {institution_image_ids} .",
                "attachments": [
                    {
                        "file_id": file_id,
                        "tools": [{"type": "file_search"}]
                    }
                ]
            }
        ]
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    course_messages = list(client.beta.threads.messages.list(
        thread_id=thread.id, run_id=run.id))
    course_image_ids = re.findall(
        r'\d+-\d+', course_messages[0].content[0].text.value)

    return institution_image_ids, course_image_ids


def create_institution_video(institution_name, image_ids):
    """
    Create a video with images for an institution.

    Args:
        institution_name (str): The name of the institution.
        image_ids (list): A list of image ids to use for the video.
    """
    audio = AudioFileClip(f"src/subpart/part1/audio1.mp3")
    frame_width, frame_height = 1280, 720
    image_duration = audio.duration / len(image_ids)
    institution_path = f"image-collection/{institution_name}"
    blur_images = False

    try:
        os.makedirs(institution_path)
    except FileExistsError:
        pass

    for i, image_id in enumerate(image_ids, start=1):
        image_path = f"{institution_path}-images/{image_id}.jpg"
        initial_image = ImageClip(image_path)
        image_size = initial_image.size

        if image_size[0] == 720:
            pad_with_blurred_edges(image_path)
            blur_images = True

        process_image(image_id=image_id, image_path=image_path,
                      save_path=institution_path)

        processed_image = ImageClip(f"{institution_path}/{image_id}.jpg")

        if image_duration < 4.5:
            motion_speed = 18
        else:
            motion_speed = 10

        def simple_motion(t, start_x, start_y):
            """
            A simple motion function to move the image.
            """
            x = start_x + t * motion_speed
            y = start_y + t * motion_speed
            return x, y

        def right_to_left(t):
            """
            Move the image from right to left.
            """
            start_x = frame_width - processed_image.w + 100
            start_y = (frame_height - processed_image.h) / 2
            return simple_motion(t, start_x, start_y)

        def down_to_up(t):
            """
            Move the image from down to up.
            """
            start_x = (frame_width - processed_image.w) / 2
            start_y = frame_height - processed_image.h + 80
            return simple_motion(t, start_x, start_y)

        motion_functions = [right_to_left, down_to_up]
        selected_function = random.choice(motion_functions) if blur_images else down_to_up

        image_clip = processed_image.set_position(selected_function)

        final_clip = CompositeVideoClip(
            [image_clip], size=(frame_width, frame_height)
        ).set_duration(image_duration)

        final_clip.write_videofile(
            f"src/subpart/part1/{i}-{image_id}-ANI.mp4", fps=60
        )


def create_course_motion_videos(institution_name, course_image_ids):
    """
    This function takes an institution name and a list of image ids, and creates
    a separate video for each image. The video is created by adding a motion
    to the image and then setting the duration of the video to be
    proportional to the duration of the audio.

    Args:
        institution_name (str): The name of the institution.
        course_image_ids (list): A list of image ids for the course.

    Returns:
        None
    """
    course_audio = AudioFileClip("src/subpart/part3/audio3.mp4")
    image_duration = course_audio.duration / 5
    institution_path = f"image-collection/{institution_name}"
    blur_images = False

    try:
        os.makedirs(institution_path)
    except FileExistsError:
        pass

    for i, image_id in enumerate(course_image_ids, start=1):
        image_path = f"{institution_path}-images/{image_id}.jpg"
        initial_image = ImageClip(image_path)
        frame_width, frame_height = 1280, 720
        image_size = initial_image.size

        if image_size[0] == 720:
            pad_with_blurred_edges(image_path)
            blur_images = True

        process_image(image_id=image_id, image_path=image_path,
                      save_path=institution_path)

        processed_image = ImageClip(f"{institution_path}/{image_id}.jpg")

        if image_duration < 4.5:
            motion_speed = 18
        else:
            motion_speed = 10

        def top_down_motion(t):
            return 0, t * motion_speed

        def left_right_motion(t):
            return t * motion_speed, 0

        def down_top_motion(t):
            return 0, frame_height - processed_image.h - t * motion_speed

        def right_left_motion(t):
            return frame_width - processed_image.w - t * motion_speed, 0

        motion_functions = [
            top_down_motion, left_right_motion, down_top_motion, right_left_motion
        ]
        selected_function = random.choice(motion_functions) if blur_images else down_top_motion

        image_clip = processed_image.set_position(selected_function)

        final_clip = CompositeVideoClip(
            [image_clip], size=(frame_width, frame_height)
        ).set_duration(image_duration)

        final_clip.write_videofile(
            f"src/subpart/part3/{i}-{image_id}-ANI.mp4", fps=60, bitrate="8000k", codec="libx264"
        )


def resize_image(image_path, target_size=(1400, 800)):
    try:
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, target_size)

        return resized_image
    except Exception as e:
        print(f"Error: {e}")
        return None


def process_image(image_id, image_path, save_path):

    resized_image = resize_image(image_path)
    if resized_image is not None:
        output_path = f"{save_path}/{image_id}.jpg"
        cv2.imwrite(output_path, resized_image)
        print("Image processed and saved")


def pad_with_blurred_edges(image_path, target_size=(720, 1280)):
    # Get the original image size
    image = cv2.imread(image_path)
    original_height, original_width = image.shape[:2]

    # Determine padding sizes
    pad_vertical = (target_size[0] - original_height) // 2
    pad_horizontal = (target_size[1] - original_width) // 2

    # Pad the image with replicated edges
    padded_image = cv2.copyMakeBorder(
        image,
        pad_vertical, pad_vertical, pad_horizontal, pad_horizontal,
        cv2.BORDER_REPLICATE
    )

    # Create a blurred version of the padded image
    blurred_image = cv2.GaussianBlur(padded_image, (21, 21), 0)

    # Blend the original image into the blurred image
    blended_image = blurred_image.copy()
    blended_image[pad_vertical:pad_vertical + original_height,
                  pad_horizontal:pad_horizontal + original_width] = image

    cv2.imwrite(image_path, blended_image)


def generate_motion_videos_and_card():
    """
    Generate motion videos and a course card from text files and image collections.
    """
    with open("src/text/course_details.json") as file:
        course_details = json.load(file)
    with open("src/text/university_summary_content.txt") as file:
        institution_content = file.read()
    with open("src/text/course_summary_content.txt") as file:
        course_content = file.read()

    institution_name = course_details["university_name"]

    generate_course_card(course_details)
    generate_course_details_card(course_details)
    institution_images, course_images = suggest_images(
        institution_name, institution_content, course_content)

    create_institution_video(institution_name, institution_images)
    create_course_motion_videos(institution_name, course_images)
