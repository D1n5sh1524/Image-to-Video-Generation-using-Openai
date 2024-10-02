import json
import os
import time
import urllib.request

import openai
import openpyxl
import requests
from PIL import Image
university_list = ['UCW']

DESC_PROMT = "describe the image in 70 - 100 words."
WORKBOOK = openpyxl.load_workbook('image-collection/IDPC-image-data.xlsx')
DOMAIN = "https://mytest.stage.aws.idp-connect.com"
PRD_DOMAIN = "https://images-intl.prod.aws.idp-connect.com"


openai.api_key = "<Openai KEY>"


def load_and_save_images_and_json(university_list: list) -> None:
    """
    Given a list of university names, download the images from the excel sheet (IDPC-image-data.xlsx),
    save them in the respective folders, check if the images are resizable, if not delete them.
    Once the images are resized, use the openai api to generate a description of the image,
    create a json file for each university and save the image id and description in the json file.

    Args:
        university_list (list): A list of university names

    Returns:
        None
    """
    for university in university_list:
        images_folder = f"image-collection/{university}-images"
        try:
            os.makedirs(images_folder)
        except FileExistsError:
            pass

        sheet = WORKBOOK[university]
        image_dict = {}

        for row in sheet.iter_rows(min_row=2, values_only=False):
            image_id = str(row[0].value)
            image_url = DOMAIN + str(row[1].value)
            image_path = f"{images_folder}/{image_id}.jpg"

            try:
                response = requests.get(url=image_url)
                if response.status_code != 404:
                    urllib.request.urlretrieve(image_url, image_path)
                else:
                    image_url = PRD_DOMAIN + str(row[1].value)
                    urllib.request.urlretrieve(image_url, image_path)

                meets_requirement, size = check_image_resizable(image_path)
                if size[1] == 720:
                    new_file_name = f"{images_folder}/{image_id}-pd.jpg"
                    os.rename(image_path, new_file_name)

                if meets_requirement:
                    response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                        {"type": "text", "text": DESC_PROMT},
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": image_url,
                                            },
                                        },
                                ],
                            }
                        ],
                        max_tokens=300,
                    )
                    time.sleep(1)
                    image_dict[image_id] = response.choices[0].message.content
                    pass
                else:
                    os.remove(image_path)
            except:
                pass

        with open(f"image-collection/Image-json/{university}_image.json", 'w') as file:
            json.dump(image_dict, file, indent=4)


def is_image_resizable(image_path: str, target_width: int = 1280, target_height: int = 720) -> tuple[bool, tuple[int, int]]:
    """Check if image is compatible and resize to required width and height."""

    with Image.open(image_path) as img:
        width, height = img.size
        if width >= target_width and height >= target_height:
            return True, (width, height)
        elif width >= 720 and height >= 600:
            return True, (width, height)
        else:
            return False, (width, height)


load_and_save_images_and_json(university_list)
print('Completed')
