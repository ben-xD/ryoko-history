

from fastapi import APIRouter, File, UploadFile

from src.file_upload import save_files_to_disk, upload_files_to_r2


router = APIRouter(prefix="/manual-test-apis", tags=["test"])

@router.post("/file/")
async def upload_file(
    images: list[UploadFile] = File(...)
    ):
    local_file_paths = await save_files_to_disk(images)
    remote_file_paths: list[str] = upload_files_to_r2(local_file_paths)
    print(remote_file_paths)
