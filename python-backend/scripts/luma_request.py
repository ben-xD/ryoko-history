import requests

from src.env import env

from ..src.luma_video import generate_video_from_1_or_2_images

video_id = generate_video_from_1_or_2_images()

url = "https://api.lumalabs.ai/dream-machine/v1/generations/"+ str(video_id)

headers = {
    "accept": "application/json",
    "authorization": f"Bearer ${env.LUMAAI_API_KEY}"
}

response = requests.get(url, headers=headers)

print(response.text)