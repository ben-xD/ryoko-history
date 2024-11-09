import asyncio
import json
import os
from pathlib import Path
from typing import Annotated, Optional, Union
from .luma_video import generate_video_from_1_or_2_images, download_video_from_id, luma_client


from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from PIL import Image
from typing import Optional
from fastapi import File, UploadFile

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIRECTORY = Path(os.path.join(os.path.dirname(__file__), "./uploads")).resolve()
print(f"Images will be uploaded to {UPLOAD_DIRECTORY}")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


image_filenames = []
image_embeddings = []
image_object_embeddings = {}
image_with_objects = []


async def save_files_to_disk(files: list[UploadFile]) -> list[Path]:
    local_file_paths: list[Path] = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        local_file_paths.append(Path(file_path))
    return local_file_paths


def process_files(local_file_paths):
    for file_path in local_file_paths:
        image = Image.open(file_path)
        print("Loaded image, of size ", image.size)


@app.get("/")
def read_root():
    return "OK"


class CreateTravelSummaryMetadata(BaseModel):
    names: list[str]
    description: Optional[str] = None

MINIMUM_IMAGES = 2

ImagePair = Union[tuple[str, str], str]

async def process_pair_of_images(image_pair: ImagePair):
    video_id = await generate_video_from_1_or_2_images(luma_client, image_pair)
    return await download_video_from_id(video_id)

@app.post("/create-travel-summary/")
async def create_travel_summary(
    images: list[UploadFile] = File(...),
    metadata_json_str: str = Form(...)):
    metadata_dict = json.loads(metadata_json_str)
    metadata = CreateTravelSummaryMetadata(**metadata_dict)
    local_file_paths = await save_files_to_disk(images)
    
    return "TODO. Not implemented."
    
    # TODO upload to R2 cloudflare
    remote_file_paths: list[str] = await upload_files_to_r2(local_file_paths)
    # [(1,2), (3,4), (5)]
    paired_remote_file_paths: list[ImagePair] = []
    for i in range(0, len(remote_file_paths), 2):
        pair = tuple(remote_file_paths[i:i + 2])
        paired_remote_file_paths.append(pair)
    
    local_generated_video_paths: list[str] = []
    for pair in paired_remote_file_paths:
        local_generated_video_paths.append(process_pair_of_images(pair))
    await asyncio.gather(*local_generated_video_paths)
    
    # TODO read exifmetadata from images
    # TODO call OpenAI API to generate summary based on images and metadata
    summary = create_summary_from_images_and_metadata(images, metadata)
    # TODO use elevenlabs to generate voice over for summary, and store locally
    voice_over = generate_voice_over(summary)

    # TODO merge all videos and 1 audio file into final video
    final_video_path = merge_videos_and_audio(local_generated_video_paths, voice_over)
    # Return final video URL to browser
    return final_video_path


@app.get("/uploads/{filename}")
async def download_file(filename: str):
    # Prevent directory traversal
    sanitized_filename = Path(filename).name
    file_path = UPLOAD_DIRECTORY / sanitized_filename

    # Resolve the full path and check it's within the upload directory
    try:
        resolved_file_path = file_path.resolve()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid filename")

    if not resolved_file_path.is_relative_to(UPLOAD_DIRECTORY):
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