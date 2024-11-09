import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
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


def individual_similarity(embedding1, embedding2):
    similarity = torch.matmul(embedding1, embedding2.T)
    norm1 = embedding1.norm(dim=1, keepdim=True)
    norm2 = embedding2.norm(dim=1, keepdim=True)
    similarity = similarity / (norm1 * norm2.T)
    assert similarity.shape == (1, 1), f"Expected shape (1, 1), got {similarity.shape}"
    return similarity.item()


async def upload_files(files: list[UploadFile]) -> list[Path]:
    local_file_paths: list[Path] = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        local_file_paths.append(Path(file_path))
    return local_file_paths


class Position2D(BaseModel):
    lat_deg: int
    lon_deg: int


class SearchResult(BaseModel):
    image_url: str
    score: float

    # name: str
    # description: Optional[str] = None
    # position: Optional[Position2D] = None
    # exif: Exif # position? camera data?
    # embedding: bytes


def process_files(local_file_paths):
    for file_path in local_file_paths:
        image = Image.open(file_path)
        print("Loaded image, of size ", image.size)


@app.get("/")
def read_root():
    return "OK"


@app.post("/uploadfiles/")
async def upload_and_process_files(files: list[UploadFile] = File(...)):
    local_file_paths = await upload_files(files)
    image_filenames.extend([file.filename for file in files])
    process_files(local_file_paths)


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)