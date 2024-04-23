import openai
from openai import OpenAI
import re
from django.conf import settings
from django.utils import timezone
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from typing import List
from ..models import InstagramComment, InstagramMedia, InstagramMediaScore


def openai_analyze_comments(comments: List[InstagramComment], instagram_account_type: str = 'brand'):
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    prompt = (f"Analyze these comments given that they relate to a post from an instagram account for a "
              f" {instagram_account_type}: {[str(comment) for comment in comments]}")

    openai_response = client.chat.completions.create(
        model=settings.OPENAI_IMAGE_ENGINE,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                ]
            }
        ],
        max_tokens=256,
    )

    analysis = openai_response.choices[0].message.content
    return analysis


def hume_analyze_image(image_url):
    client = HumeBatchClient(settings.HUME_KEY)
    urls = [image_url]
    config = FaceConfig()
    job = client.submit_job(urls, [config])

    details = job.await_complete()
    print(details)

    predictions = job.get_predictions()

    return predictions


def analyze_face(hume_response):
    hume_results = hume_response[0]['results']
    hume_predictions = hume_results['predictions'][0]
    hume_models = hume_predictions['models']
    hume_face = hume_models['face']
    hume_grouped_predictions = hume_face['grouped_predictions']

    if len(hume_grouped_predictions) < 1:
        # no face detected
        facial_analysis = ''
    else:
        facial_analysis = hume_face['grouped_predictions'][0]['predictions'][0]['emotions']

    return facial_analysis


def rate_image(media: InstagramMedia, comment_list):
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    with open(f"{settings.BASE_DIR}/post_prompt.txt") as post_prompt:
        post_prompt = post_prompt.read().replace('\n', '')
        prompt = (f"Taking into account the image at the given url for an Instagram post, "
                  f"the post text accompanying the image {media.caption_text},"
                  f"and the list of comments: {[str(comment) for comment in comment_list]}"
                  f"{post_prompt}")

        openai_response = client.chat.completions.create(
            model=settings.OPENAI_IMAGE_ENGINE,
            messages=[
                {
                    "role":"user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": media.thumbnail_url
                            }
                        }
                    ]
                }
            ],
            max_tokens=256,
        )

        analysis = openai_response.choices[0].message.content
        return analysis
