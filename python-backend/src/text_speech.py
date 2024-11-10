from datetime import datetime
import os
import requests
from dotenv import load_dotenv
from src.env import env
from src.local_paths import GENERATED_AUDIO_DIRECTORY

load_dotenv()

# English
# agent_id = "Xb7hH8MSUJpSbSDYk0k2"

# Japanese
# agent_id = "3JDquces8E8bkmvbh6Bc"
agent_id = "hBWDuZMNs32sP5dKzMuc"

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/"+ agent_id

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": env.ELEVENLABS_API_KEY
}

# summary = """
# Ah, Paris, the City of Love. As I scroll through these photos, I can't help but feel a sense of wonder and enchantment. From the iconic Eiffel Tower standing tall against the sky to the charming streets filled with cozy cafes and bustling markets, every corner of this city tells a unique story. 
# I can see Alice and Bob looking so happy in front of the Louvre Museum, admiring the beauty of the Mona Lisa. And then there's a shot of them playfully posing with Mickey and Minnie Mouse at Disneyland Paris, pure joy radiating from their smiles. 
# The golden sunlight reflects off the Seine River as they enjoy a romantic boat ride, taking in the breathtaking views of Notre-Dame Cathedral. And as the sun sets over the city, painting the sky in hues of orange and pink, I can feel the warmth of their memories being made in the City of Lights. Truly a trip to remember.
# """

summary = """
パリの魅力的な通りを歩きながら、焼きたてのクロワッサンの豊かな香りを吸い込むことを想像してください。これがアリスとボブの素敵なパリの冒険の背景でした。彼らの旅行は美しく捉えられ、各写真がパリ、光の都のロマンスと魅力へのポータルとなりました。
1つの大切なスナップショットで、アリスとボブは象徴的なエッフェル塔の下で見つけました。その高くそびえる鉄の格子は、人間の知恵と創造力の証です。彼らの顔は、ゴールデンなパリの夕日に照らされ、喜びを放ち、歴史的な壮大さの中で完璧な驚異と不思議の瞬間を包み込んでいました。
別の心温まる旅行シーンでは、カップルは子どもの頃の夢を思い出させる興奮とともにディズニーの魔法を抱きしめました。写真は、彼らがミッキーとミニー・マウスとポーズをとる際に彼らの嬉しそうな笑顔を披露し、愛されるキャラクターが彼らの魅惑的なパリ体験にさらなる輝きを加えました。
アリスとボブの旅行からのすべての写真は、愛、発見、そしてパリの永遠の魅力の物語を語ります。象徴的なランドマークからおとぎ話のような出会いに至るまで、彼らの旅行は訪れた場所だけでなく、一緒に作り上げた忘れられない思い出についてであり、彼らの心にパリの精神を永遠に捉えました。
"""

def generate_speech(summary:str) -> str:
  data = {
    "text": summary,
    # "model_id": "eleven_monolingual_v1",
    # "model_id": "eleven_multilingual_v2",
    "model_id": "eleven_turbo_v2_5",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
    }
  }

  response = requests.post(url, json=data, headers=headers)

  if response.status_code == 200 and response.headers.get("Content-Type") == "audio/mpeg":
      os.makedirs(GENERATED_AUDIO_DIRECTORY, exist_ok=True)
      filename = f"{datetime.now().isoformat()}_generated_audio.mp4"
      output_path = os.path.join(GENERATED_AUDIO_DIRECTORY, filename)
      with open(output_path, 'wb') as f:
          for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
              if chunk:
                  f.write(chunk)
      print("Speech generated successfully")
      return output_path
  else:
      print("Error:", response.status_code, response.text)
      return None


if __name__ == "__main__":
  generate_speech(summary)