# Local upload
import os
from pathlib import Path


LOCAL_UPLOAD_DIRECTORY = Path(os.path.join(os.path.dirname(__file__), "./uploads")).resolve()
print(f"Images will be saved locally to {LOCAL_UPLOAD_DIRECTORY}")
os.makedirs(LOCAL_UPLOAD_DIRECTORY, exist_ok=True)


GENERATED_VIDEOS_DIRECTORY = Path(os.path.join(os.path.dirname(__file__), "./ai_generated_videos")).resolve()
print(f"Generated videos will be downloaded to {GENERATED_VIDEOS_DIRECTORY}")
os.makedirs(GENERATED_VIDEOS_DIRECTORY, exist_ok=True)

# New for post processed video
FINAL_VIDEOS_DIRECTORY = Path(os.path.join(os.path.dirname(__file__), "./final_videos")).resolve()
os.makedirs(FINAL_VIDEOS_DIRECTORY, exist_ok=True)

# New generated audio
GENERATED_AUDIO_DIRECTORY = Path(os.path.join(os.path.dirname(__file__), "./generated_audio")).resolve()
os.makedirs(GENERATED_AUDIO_DIRECTORY, exist_ok=True)