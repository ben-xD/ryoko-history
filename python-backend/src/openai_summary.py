import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# # test
# test_chat = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )

# summary_content = test_chat.choices[0].message.content
# print(summary_content)

# image summarisation
def create_summary_from_images_and_metadata(images: list[str]):
    prompt = """
    You are a summariser that summarises travel photos in a personal manner with a warm positive tone with a range of emotions. Your job is to examine photos that are uploaded to you and make good descriptive summaries of their travel photos. It should feel like a story, reminiscent, maybe poignant when necessary, maybe happy or sad depending on the content of the photos uploaded, you can use the metadata from the photos to determine location where possible but you should also just be able to deduce the location just from the contents of the photos i.e they're photographed next a famous well known landmark etc. The summary for each image should take less than 2 seconds to speak.
    Here are multiple images that you need to summarise:
    """ + "\n".join([f"- Image {i+1}: {image}" for i, image in enumerate(images)])

    # print("prompt:", prompt)

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

# need a list of image urls for summarisation
url_list = ["https://i2.wp.com/calvinthecanine.com/wp-content/uploads/2019/11/A35A7884v4.jpg?resize=697%2C465",
    "https://static.independent.co.uk/s3fs-public/thumbnails/image/2017/06/01/16/mickey-minnie.jpg?width=1200"
]

create_summary_from_images_and_metadata(url_list)