import asyncio
from pathlib import Path
from typing import Optional

from src.routes import manual_test_apis
from src.file_upload import LOCAL_UPLOAD_DIRECTORY, save_files_to_disk, upload_files_to_r2
from src.luma_video import generate_video_from_1_or_2_images, download_video_from_id, luma_client
from src.luma_video import ImagePair

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

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

@app.get("/")
def read_root():
    return "OK"


class CreateTravelSummaryMetadata(BaseModel):
    names: list[str]
    description: Optional[str] = None

MINIMUM_IMAGES = 2

async def generate_and_download_video_from(image_pair: ImagePair):
    video_id = await generate_video_from_1_or_2_images(luma_client, image_pair)
    return await download_video_from_id(luma_client, video_id)


@app.post("/create-travel-summary/")
async def create_travel_summary(
    images: list[UploadFile] = File(...),
    # metadata_json_str: str = Form(...)
    ):
    # metadata_dict = json.loads(metadata_json_str)
    # metadata = CreateTravelSummaryMetadata(**metadata_dict)
    local_file_paths = await save_files_to_disk(images)
    
    remote_file_paths: list[str] = upload_files_to_r2(local_file_paths)
    # [(1,2), (3,4), (5)]
    paired_remote_file_paths: list[ImagePair] = []
    for i in range(0, len(remote_file_paths), 2):
        pair = (remote_file_paths[i], remote_file_paths[i + 1])
        paired_remote_file_paths.append(pair)
    
    tasks = [
        generate_and_download_video_from(pair) for pair in paired_remote_file_paths
    ]
    local_generated_video_paths = await asyncio.gather(*tasks)
    print(local_generated_video_paths)
    
    # TODO read exifmetadata from images
    # TODO call OpenAI API to generate summary based on images and metadata
    # summary = create_summary_from_images_and_metadata(remote_file_paths, metadata.names, metadata.description)
    # TODO use elevenlabs to generate voice over for summary, and store locally
    
    return "INCOMPLETE. "
    # voice_over = generate_voice_over(summary)

    # # TODO merge all videos and 1 audio file into final video
    # final_video_path = merge_videos_and_audio(local_generated_video_paths, voice_over)
    # # Return final video URL to browser
    # return final_video_path


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