import asyncio
import json
from pathlib import Path
from typing import Literal, Optional

from src.local_paths import LOCAL_UPLOAD_DIRECTORY
from src.openai_summary import create_summary_from_images_and_metadata
from src.routes import conversation, manual_test_apis
from src.file_upload import save_files_to_disk, upload_user_photos_to_r2_bucket
from src.luma_video import download_video_from_url, generate_video_from_1_or_2_images, luma_client
from src.luma_video import ImagePair

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from src.video_postprocessing import merge_videos_and_audio

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(manual_test_apis.router)
app.include_router(conversation.router)

@app.get("/")
def read_root():
    return "OK"


class CreateTravelSummaryMetadata(BaseModel, strict=True):
    names: list[str]
    description: Optional[str] = None
    transcript_messages: list[TranscriptMessage] = []

MINIMUM_IMAGES = 2

async def generate_and_download_video_from(image_pair: ImagePair):
    video_url = await generate_video_from_1_or_2_images(luma_client, image_pair)
    if video_url is None:
        print("Failed to generate video, skipping download")
        return None
    return await download_video_from_url(video_url)


@app.post("/create-travel-summary/")
async def create_travel_summary(
    images: list[UploadFile] = File(...),
    metadata_json_str: str = Form(...)
    ):
    metadata_dict = json.loads(metadata_json_str)
    metadata = CreateTravelSummaryMetadata(**metadata_dict)
    local_file_paths = await save_files_to_disk(images)
    
    remote_file_paths: list[str] = upload_user_photos_to_r2_bucket(local_file_paths)
    # [(1,2), (3,4), (5)]
    paired_remote_file_paths: list[ImagePair] = []
    for i in range(0, len(remote_file_paths), 2):
        if i + 1 >= len(remote_file_paths):
            # If there's an odd number of images, just use the last one
            paired_remote_file_paths.append((remote_file_paths[i],))
        else:
            pair = (remote_file_paths[i], remote_file_paths[i + 1])
            paired_remote_file_paths.append(pair)
    
    tasks = [
        generate_and_download_video_from(pair) for pair in paired_remote_file_paths
    ]
    local_generated_video_paths = await asyncio.gather(*tasks)
    print(local_generated_video_paths)
    
    # TODO read exifmetadata from images
    # TODO call OpenAI API to generate summary based on images and metadata
    summary = create_summary_from_images_and_metadata(remote_file_paths, metadata.names, metadata.description, metadata.transcript_messages)
    
    # TODO use elevenlabs to generate voice over for summary, and store locally
    # voice_over = generate_voice_over(summary)
    # Temporary audio
    voice_over_path = "/Users/zen/Downloads/holy-children-s-choir-loop_78bpm_A_major.wav"

    final_video_path = merge_videos_and_audio(local_generated_video_paths, voice_over_path)
    return final_video_path


@app.get("/uploads/{filename}")
async def download_file(filename: str):
    # Prevent directory traversal
    sanitized_filename = Path(filename).name
    file_path = LOCAL_UPLOAD_DIRECTORY / sanitized_filename

    # Resolve the full path and check it's within the upload directory
    try:
        resolved_file_path = file_path.resolve()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid filename")

    if not resolved_file_path.is_relative_to(LOCAL_UPLOAD_DIRECTORY):
        raise HTTPException(status_code=400, detail="Invalid filename")

    if resolved_file_path.exists() and resolved_file_path.is_file():
        return FileResponse(resolved_file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


def main():
    import uvicorn

    public = False
    host = "0.0.0.0" if public else "127.0.0.1"
    uvicorn.run(app, host=host, port=8000)


if __name__ == "__main__":
    main()