import requests

from src.env import env

def main():
    # video_id = generate_video_from_1_or_2_images()
    # video_id = "91a8d9f2-1cb9-44f5-86d3-c0c9f4a0ce5c"
    video_id = "e9cf3556-60f6-4f52-b72f-93745f24c513"
    
    print(env.LUMAAI_API_KEY)

    url = "https://api.lumalabs.ai/dream-machine/v1/generations/"+ str(video_id)

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {env.LUMAAI_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    print(response.text)

if __name__ == "__main__":
    main()