import json
import os
import openai
import openpyxl
import requests

university_list = {
    "University of Plymouth":3758}


DESC_PROMT = "describe the image in 70 - 100 words."
WORKBOOK = openpyxl.load_workbook('image-collection/institution_info.xlsx')
DOMAIN = "<image_url>"


openai.api_key = "<Provide OPENAI API KEY>"

university = "University of Surrey"
sheet = WORKBOOK[university]


def save_image_json():
    """
    Save image descriptions to a JSON file for a given university.

    This function takes a university name and saves a JSON file containing
    image descriptions for all the images associated with that university.
    """
    uni_image_dict = {}

    for filename in os.listdir(f"image-collection/{university}-images"):
        filename = filename[:filename.find(".jpg")]
        row = next((row for row in sheet.iter_rows(min_row=1, values_only=False) if row[0].value == filename), None)

        if row:
            image_url = DOMAIN + str(row[1].value)
            response = requests.get(url=image_url)
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": DESC_PROMT},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url},
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )

            image_desc = response.choices[0].message.content
            uni_image_dict[filename] = image_desc

    with open(f"image-collection/Image-json/{university}_image.json", 'w') as file:
        json.dump(uni_image_dict, file, indent=4)

save_image_json()