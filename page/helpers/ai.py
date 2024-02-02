import boto3
import openai
import os
import re
from django.conf import settings
from django.utils import timezone
from typing import List
from ..models import InstagramComment, InstagramMedia, InstagramMediaScore, JalodeiUser
from ..helpers.inst import (inst_login_client, inst_set_proxy)


def aws_analyze_image(image_path):
    client = boto3.client('rekognition')

    with open(image_path, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

        print('Detected labels in ' + image_path)
        for label in response['Labels']:
            print(label['Name'] + ' : ' + str(label['Confidence']))

    return len(response['Labels'])


def google_analyze_image(media: InstagramMedia):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f"{settings.BASE_DIR}/jalodei/google_key.json"

    client = vision_v1.ImageAnnotatorClient()
    source = {"image_uri": media.thumbnail_url}
    image = {"source": source}
    features = [
        {"type_": vision_v1.Feature.Type.FACE_DETECTION},
        {"type_": vision_v1.Feature.Type.LANDMARK_DETECTION},
        {"type_": vision_v1.Feature.Type.LABEL_DETECTION},
        {"type_": vision_v1.Feature.Type.OBJECT_LOCALIZATION}
    ]

    request = vision_v1.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request)

    return response


def decision_tree_choose(request, media_url, options: List[str]):
    request_user = JalodeiUser.objects.get(user=request.user)
    cl = inst_login_client(cl, request_user.instagram_username, request_user.instagram_password)

    media_pk = cl.media_pk_from_url(media_url)
    comments = cl.media_comments(media_pk, 200)

    openai_comments_analysis = openai_analyze_comments(comments)
    media = cl.media_info(media_pk)
    i_media = InstagramMedia.objects.get(media_id=media.pk)
    image_analysis = google_analyze_image(i_media)
