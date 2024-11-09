import requests
from dotenv import load_dotenv
import os

from luma_video import generate_video

video_id = generate_video()

load_dotenv()
auth_token=os.environ.get("LUMAAI_API_bearer")

url = "https://api.lumalabs.ai/dream-machine/v1/generations/"+ str(video_id)

headers = {
    "accept": "application/json",
    "authorization": auth_token
}

response = requests.get(url, headers=headers)

print(response.text)