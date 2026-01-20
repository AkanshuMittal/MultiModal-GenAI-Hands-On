from openai import OpenAI 
from dotenv import load_dotenv
import requests

load_dotenv()

client = OpenAI()

response = client.images.generate(
    model = "dall-e-3",
    prompt="a white siamese cat",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url

img = requests.get(image_url).content

with open("dall-e-3_image.png", "wb") as f:
    f.write(img)

print("Image saved as dall-e-3_image.png")