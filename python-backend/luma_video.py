# generate a video from two images using luma api
import datetime
from lumaai import AsyncLumaAI
from dotenv import load_dotenv
import os

import requests
import aiohttp
import asyncio

load_dotenv()

auth_token=os.environ.get("LUMAAI_API_KEY")
# print(auth_token)

client = AsyncLumaAI(auth_token=os.environ.get("LUMAAI_API_KEY"))

# need a list of two image urls
async def generate_video(client: AsyncLumaAI):
    generation = await client.generations.create(
        # aspect_ratio="16:9",
        # loop=False,
        # prompt="my travel vlog in paris 2024",
        keyframes={
        "frame0": {
            "type": "image",
            "url": "https://i2.wp.com/calvinthecanine.com/wp-content/uploads/2019/11/A35A7884v4.jpg?resize=697%2C465"
        },
        "frame1": {
            "type": "image",
            "url": "https://static.independent.co.uk/s3fs-public/thumbnails/image/2017/06/01/16/mickey-minnie.jpg?width=1200"
        }
        }
    )
    video_id = generation.id
    print("Video generated! video ID:", generation.id)
    return video_id


video_downloads_folder = "video_downloads"

async def download_video_from_url(url: str):
    os.makedirs(video_downloads_folder, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_content = await response.read()
            # Current time formatted compactly: luma_video_20210930_123456.mp4
            file_name = f"{video_downloads_folder}/luma_video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            with open(file_name, 'wb') as f:
                f.write(response_content)


async def get_video(client: AsyncLumaAI, video_id):
    generation = await client.generations.get(id=video_id)
    # Optional[Literal["queued", "dreaming", "completed", "failed"]]
    # TODO: Check if the video is completed before downloading
    if generation.state == 'failed':
        print("Video generation failed")
        return

    # "assets" is only 1 video url
    if generation.assets is None:
        print("No video asset found")
        return
    url = generation.assets.video
    if url is None:
        print("No video url found")
        return
    await download_video_from_url(url)


async def main():
    video_id = await generate_video(client)
    await get_video(client, video_id)

if __name__ == "__main__":
    asyncio.run(main())
