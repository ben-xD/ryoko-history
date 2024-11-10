from typing import Literal, Optional
from openai import OpenAI
from pydantic import BaseModel
from src.env import env
from src.languages import Language


openaiModel = "gpt-4-turbo"

class TranscriptMessage(BaseModel):
    source: Literal["ai", "user"]
    message: str

    def __str__(self):
        return f"{self.source} said {self.message}"

openai_client = OpenAI(api_key=env.OPENAI_API_KEY)


def create_summary_from_images_and_metadata(image_urls: list[str], travellers: list[str], trip_description: Optional[str], transcript_messages: list[TranscriptMessage]) -> Optional[str]:
    # prompt_with_images = """
    # You are a summariser that summarises travel photos in a personal manner with a warm positive tone with a range of emotions. Your job is to examine photos that are uploaded to you and make good descriptive summaries of their travel photos. It should feel like a story, reminiscent, maybe poignant when necessary, maybe happy or sad depending on the content of the photos uploaded, you can use the metadata from the photos to determine location where possible but you should also just be able to deduce the location just from the contents of the photos i.e they're photographed next a famous well known landmark etc. You should attempt to create a catchy script including the city name if possible, and generate a summary of their trip totally in 30 seconds speech length that can be used for a narration of a travel video composed of their pictures. The narration should use traveller name or first person pronouns such as "I" or "We"  depending on the travellers but do not use third person pronouns such as "They" or "She" in the narration. The summary will be read by a text to speech service so should be formatted as it is pronounced. Do not include any captions, e.g. [Opening music plays].
    # Here are all the images that you need to create one single summary for:
    # """ + "\n".join([image_url for image_url in image_urls]) + "\n"

    prompt = """
    You are a summariser that summarises the chat agent and user conversation to create a video script for a travel photo video. You should attempt to create a script that explain the user's travel experiences including the city name if possible, and generate a summary of their trip totally in 30 seconds long that can be used for a narration of a travel video composed of their pictures. The narration should use traveller name or first person pronouns such as "I" or "We"  depending on the travellers but do not use third person pronouns such as "They" or "She" in the narration. The summary will be read by a text to speech service so should be formatted as it is pronounced. Do not include any captions, e.g. [Opening music plays].
    Here is the conversation between a traveller and an AI assistant: """ + ". ".join([str(message) for message in transcript_messages])

    if travellers is not None and len(travellers) > 0:
        include_travellers = "Here are the name of travellers: " + ", ".join([traveller for traveller in travellers]) + "\n"
        prompt = prompt + include_travellers
    if trip_description is not None:
        include_trip_description = "Here is the description of the trip: " + trip_description + "\n"
        prompt = prompt + include_trip_description
    # if transcript_messages is not None:
    #     include_transcript_messages = "Here is the conversation between a traveller and an AI assistant: " + ". ".join([str(message) for message in transcript_messages]) + "\n\n"
    #     prompt = prompt + include_transcript_messages

    print("prompt:", prompt)

    summary = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=openaiModel,
    )

    summary_content = summary.choices[0].message.content
    print(summary_content)
    return summary_content


def translate_summary(summary_content: str, language: Language):
    prompt = f"""Translate the text into {language.value}. It should sound like travellers are the narrators of the story.""" + summary_content + "\n"
    translation = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=openaiModel,
    )

    translation_content = translation.choices[0].message.content
    print(translation_content)
    return translation_content


# need a list of image urls for summarisation
example_urls = ["https://i2.wp.com/calvinthecanine.com/wp-content/uploads/2019/11/A35A7884v4.jpg?resize=697%2C465",
    "https://static.independent.co.uk/s3fs-public/thumbnails/image/2017/06/01/16/mickey-minnie.jpg?width=1200"
]
travellers = None
trip_description = None

# example 3 messages in the conversation: 
example_transcript = [
    TranscriptMessage(source="ai", message="Ah, Paris, the City of Love. As I scroll through these photos, I can't help but feel a sense of wonder and enchantment. From the iconic Eiffel Tower standing tall against the sky to the charming streets filled with cozy cafes and bustling markets, every corner of this city tells a unique story."),
    TranscriptMessage(source="user", message="I can see Alice and Bob looking so happy in front of the Louvre Museum, admiring the beauty of the Mona Lisa. And then there's a shot of them playfully posing with Mickey and Minnie Mouse at Disneyland Paris, pure joy radiating from their smiles."),
    TranscriptMessage(source="ai", message="The golden sunlight reflects off the Seine River as they enjoy a romantic boat ride, taking in the breathtaking views of Notre-Dame Cathedral. And as the sun sets over the city, painting the sky in hues of orange and pink, I can feel the warmth of their memories being made in the City of Lights. Truly a trip to remember.")
]

if __name__ == "__main__":
    original_summary = create_summary_from_images_and_metadata(example_urls, travellers=["Alice", "Bob"], trip_description="A trip to Paris", transcript_messages = example_transcript)
    if original_summary is None:
        print("Failed to generate summary")
    else:
        translated_summary = translate_summary(original_summary, Language.JAPANESE)