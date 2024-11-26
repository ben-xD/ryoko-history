from datetime import datetime
import os
import ffmpeg

from src.languages import Language
from src.local_paths import FINAL_VIDEOS_DIRECTORY

# This function was designed to accept videos from Luma, 1168x864 or 864x1168
# Combines videos sequentially and adds audio
def merge_videos_and_audio(local_generated_video_paths: list[str], language: Language, audio_path: str) -> str:
    os.makedirs(FINAL_VIDEOS_DIRECTORY, exist_ok=True)
    
    filename = f"{datetime.now().isoformat()}_{language.value}_generated.mp4"
    output_path = os.path.join(FINAL_VIDEOS_DIRECTORY, filename)
    
    # Process videos to ensure they are in landscape format with padding if needed
    video_inputs = []
    for video in local_generated_video_paths:
        input_video = ffmpeg.input(video)
        
        # Pad the video if it is in portrait orientation (864x1168)
        video_with_padding = (
            input_video
            # scale height to 864, keep aspect ratio
            .filter('scale', -1, 864)  # Scale height to 864, keep aspect ratio
            .filter('pad', 1168, 864, '(ow-iw)/2', '(oh-ih)/2', color='black')  # Pad to 1168x864
        )
        
        video_inputs.append(video_with_padding)
    
    # Concatenate the processed video inputs
    video_concat = ffmpeg.concat(*video_inputs, v=1, a=0).node
    audio_input = ffmpeg.input(audio_path)
    
    # Combine video and audio, and save the output
    ffmpeg.output(video_concat[0], audio_input, output_path, vcodec="libx264", acodec="aac").run(overwrite_output=True)
    return output_path


if __name__ == "__main__":
    # Example usage
    audio = os.path.join(os.path.dirname(__file__), "generated_audio/2024-11-13T23:28:54.959315_JAPANESE_generated_audio.mp4")
    video_directory = os.path.join(os.path.dirname(__file__), "ai_generated_videos/")
    videos = [os.path.join(video_directory, f) for f in os.listdir(video_directory) if f.endswith(".mp4")]
    merged_video = merge_videos_and_audio(videos, Language.JAPANESE, audio)
    