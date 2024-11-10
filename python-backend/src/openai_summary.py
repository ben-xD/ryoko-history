import os
from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class TranscriptMessage(BaseModel):
    source: Literal["ai", "user"]
    message: str

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# image summarisation
def create_summary_from_images_and_metadata(image_urls: list[str], travellers: list[str], trip_description: str, transcript_messages: list[TranscriptMessage]) -> str:
    prompt = """
    You are a summariser that summarises travel photos in a personal manner with a warm positive tone with a range of emotions. Your job is to examine photos that are uploaded to you and make good descriptive summaries of their travel photos. It should feel like a story, reminiscent, maybe poignant when necessary, maybe happy or sad depending on the content of the photos uploaded, you can use the metadata from the photos to determine location where possible but you should also just be able to deduce the location just from the contents of the photos i.e they're photographed next a famous well known landmark etc. You should attempt to create a catchy script including the city name if possible and generate a summary of their trip in 40 seconds speech length that can be used for a narration of a travel video composed of their pictures. The narration should use traveller name or first person pronouns such as "I" or "We"  depending on the travellers but never use second person pronouns such as "They" or "She". The summary will be read by a text to speech service so should be formatted as it is pronounced.
    Here are all the images that you need to create one single summary for:
    """ + "\n".join([image_url for image_url in image_urls]) + "\n"

    if travellers is not None:
        include_travellers = "Here are the name of travellers: " + ", ".join([traveller for traveller in travellers]) + "\n"
        prompt = prompt + include_travellers
    if trip_description is not None:
        include_trip_description = "Here is the description of the trip: " + trip_description + "\n"
        prompt = prompt + include_trip_description
    if transcript_messages is not None:
        include_transcript_messages = "Here are the transcript messages: " + "\n".join([f"{transcript_message.source}: {transcript_message.message}" for transcript_message in transcript_messages]) + "\n"
        prompt = prompt + include_transcript_messages

    print("prompt:", prompt)

    summary = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    summary_content = summary.choices[0].message.content
    print(summary_content)
    return summary_content


def translate_summary(summary_content: str):
    prompt = """Translate the summary into Japansese. The translated script will be read by a text to speech service so should be formatted as it is pronounced as well as the length of the speech has to be the same as original summary when it is read. """ + summary_content + "\n"
    translation = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    translation_content = translation.choices[0].message.content
    print(translation_content)
    return translation_content


# need a list of image urls for summarisation
url_list = ["https://i2.wp.com/calvinthecanine.com/wp-content/uploads/2019/11/A35A7884v4.jpg?resize=697%2C465",
    "https://static.independent.co.uk/s3fs-public/thumbnails/image/2017/06/01/16/mickey-minnie.jpg?width=1200"
]
travellers = None
trip_description = None
transcript_messages = None

if __name__ == "__main__":
    original_summary = create_summary_from_images_and_metadata(url_list, travellers=["Alice", "Bob"], trip_description="A trip to Paris", transcript_messages = transcript_messages)
    translated_summary = translate_summary(original_summary)