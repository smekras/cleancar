import subprocess

from google.cloud import vision
from google.cloud.vision import types

from logic.utils import *

client = vision.ImageAnnotatorClient()


def grab_image():
    subprocess.call('/home/pi/scripts/webcam.sh')
    picture = 'images/capture.jpg'
    with open(picture, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    return image


def get_response(image):
    response = client.text_detection(image=image)
    annotations = response.text_annotations
    text = []
    for _ in annotations:
        text.append(_.description)
    raw = list_to_string(text)
    return raw
