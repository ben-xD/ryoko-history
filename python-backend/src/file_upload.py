from datetime import datetime
import os
import boto3
from fastapi import UploadFile
from pathlib import Path
from botocore.config import Config
import uuid

from src.local_paths import LOCAL_UPLOAD_DIRECTORY

from .env import env


# R2 is like S3, but with Cloudflare. It's a storage service.
endpoint_url = f"https://{env.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com"

# Sync API
# For more code, see https://developers.cloudflare.com/r2/examples/aws/boto3/

s3 = boto3.client(service_name='s3',
  endpoint_url = endpoint_url,
  aws_access_key_id = env.CLOUDFLARE_R2_ACCESS_KEY_ID,
  aws_secret_access_key = env.CLOUDFLARE_R2_ACCESS_KEY_SECRET,
  # To avoid generating the presigned URLs with v2 by default, which is not supported by R2 (it rejects with `Unauthorized: SigV2 authorization is not supported. Please use SigV4 instead.`)
  config=Config(signature_version='v4')
)

# Async API. Not a nice way of managing the lifetime of a client. Unsure how long it will last, and if it will reauthenticate, etc.
# def create_r2_client():
#     return aioboto3.Session(
#             aws_access_key_id=os.environ.get("CLOUDFLARE_R2_ACCESS_KEY_ID"),
#             aws_secret_access_key=os.environ.get("CLOUDFLARE_R2_ACCESS_KEY_SECRET"),
#             #   # Must be one of: wnam, enam, weur, eeur, apac, auto
#     ).client("s3", endpoint_url=endpoint_url)
# r2 = await create_r2_client()

def upload_object_to_r2(file_path: Path, bucket_name: str, key_name: str):
    # TODO secure to uploads folder only
    s3.upload_file(str(file_path), bucket_name, key_name)

def delete_object_from_r2(bucket_name: str, key_name: str):
    s3.delete_object(Bucket=bucket_name, Key=key_name)
    
def get_object_info_from_r2(bucket_name: str, key_name: str):
    s3.head_object(Bucket=bucket_name, Key=key_name)
    

def get_download_url(bucket_name: str, key_name: str, expiration=3600):
    try:
        url = s3.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name,
                                                        'Key': key_name},
                                                ExpiresIn=expiration)
        print(f"Download URL: {url}")
        return url
    except Exception as e:
        print(f"An error occurred when generating presigned url (bucket_name=${bucket_name}, key_name=${key_name}). {e}")
        return None    

    
user_photos_bucket_name = "ryoko-history-user-photos"
def upload_user_photos_to_r2_bucket(local_file_paths: list[Path]) -> list[str]:
    download_urls = []
    for file_path in local_file_paths:
        key_name = os.path.basename(file_path)
        upload_object_to_r2(file_path, user_photos_bucket_name, key_name)
        download_urls.append(get_download_url(bucket_name=user_photos_bucket_name, key_name=key_name))
    return download_urls
    
        
async def save_files_to_disk(files: list[UploadFile]) -> list[Path]:
    local_file_paths: list[Path] = []
    for file in files:
        unique_id = uuid.uuid4()
        filename = f"{datetime.now().isoformat()}-{unique_id}-{file.filename}"
        if file.filename is None:
            # Get current date and time
            filename = f"{datetime.now().isoformat()}-unnamed"
            print("File has no name, saving as {filename}.")
        file_path = os.path.join(LOCAL_UPLOAD_DIRECTORY, filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        local_file_paths.append(Path(file_path))
    return local_file_paths
