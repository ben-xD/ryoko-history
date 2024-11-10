# generate a video from two images using luma api
import datetime
import os
from typing import Union
import uuid
from lumaai import NOT_GIVEN, AsyncLumaAI, NotGiven
from lumaai.types.generation_create_params import Keyframes

import aiohttp
import asyncio

from src.env import env
from src.local_paths import GENERATED_VIDEOS_DIRECTORY

luma_client = AsyncLumaAI(auth_token=env.LUMAAI_API_KEY)

# need a list of two image urls per video
example_urls = ("https://i2.wp.com/calvinthecanine.com/wp-content/uploads/2019/11/A35A7884v4.jpg?resize=697%2C465",
    "https://static.independent.co.uk/s3fs-public/thumbnails/image/2017/06/01/16/mickey-minnie.jpg?width=1200"
)

ImagePair = Union[tuple[str, str], tuple[str]]

async def generate_video_from_1_or_2_images(client: AsyncLumaAI, urls: ImagePair, prompt: str | NotGiven = NOT_GIVEN) -> str | None:
    if len(urls) > 2:
        raise ValueError("Only 1 or 2 images are supported")
    
    keyframes: Keyframes = {
        "frame0": {
            "type": "image",
            "url": urls[0]
        }
        }
    
    if len(urls) > 1:
        keyframes["frame1"] = {
            "type": "image",
            "url": urls[1]
        }
    
    check_video_generated_interval_seconds = 5
    
    # the await is just for the request to succeed, not for the video to be generated
    generation = await client.generations.create(
        # We can still get 9:16 and 16:9
        aspect_ratio="16:9",
        # loop=False,
        prompt=prompt,
        keyframes=keyframes,
    )
    video_id = generation.id
    if video_id is None:
        print("Video generation failed")
        return None
    while generation.state == "queued" or generation.state == "dreaming":
        print("Checking video generation status (id: ", video_id, ")")
        await asyncio.sleep(check_video_generated_interval_seconds)
        try:
            generation = await client.generations.get(video_id)
        except Exception as e:
            print(f"Failed to get generation (id={video_id})", e)
    
    if generation.state == "failed":
        print(f"Video generation failed (id={video_id})")
        return None
    
    print("Video generated! video ID:", generation.id)
    
    # "assets" is only 1 video url
    if generation.assets is None:
        print("No video asset found")
        return None
    url = generation.assets.video
    if url is None:
        print("No video url found")
        return None
    return url


async def download_video_from_url(url: str):
    os.makedirs(GENERATED_VIDEOS_DIRECTORY, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            unique_id = uuid.uuid4()
            response_content = await response.read()
            # Current time formatted compactly: luma_video_20210930_123456.mp4
            file_name = f"{GENERATED_VIDEOS_DIRECTORY}/luma_video_{unique_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            with open(file_name, 'wb') as f:
                f.write(response_content)
                print(f"Video downloaded to {file_name}")
    return file_name


async def download_video_from_id(client: AsyncLumaAI, video_id: str):
    generation = await client.generations.get(id=video_id)
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
    video_url = await generate_video_from_1_or_2_images(luma_client, example_urls)
    await download_video_from_url(luma_client, video_url)


if __name__ == "__main__":
    asyncio.run(main())
