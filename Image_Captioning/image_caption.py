import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

## Image URLs
image_url = [
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/5uo16pKhdB1f2Vz7H8Utkg/image-1.png",
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/fsuegY1q_OxKIxNhf6zeYg/image-2.png",
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/KCh_pM9BVWq_ZdzIBIA9Fw/image-3.png",
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/VaaYLw52RaykwrE3jpFv7g/image-4.png"
]

## Encode images to base64

def encode_images_to_base64(image_url):
    """
    Downloads and encodes a list of image URLs to base64 strings.

    Parameters:
    - image_urls (list): A list of image URLs.

    Returns:
    - list: A list of base64-encoded image strings.
    """
    encoded_images = []

    for url in image_url:
        response = requests.get(url)

        if response.status_code ==200:
            encoded = base64.b64encode(response.content).decode("utf-8")
            encoded_images.append(encoded)
        else:
            print(f"Failed to fetch image: {url}")
            encoded_images.append(None)

    return encoded_images


def generate_model_response(encoded_images, user_query, assistant_prompt="You are a helpful assistant. Answer the following user query in 1 or 2 sentences: "):
    """
    Sends an image and a query to the model and retrieves the description or answer.

    Parameters:
    - encoded_image (str): Base64-encoded image string.
    - user_query (str): The user's question about the image.
    - assistant_prompt (str): Optional prompt to guide the model's response.

    Returns:
    - str: The model's response for the given image and query.
    """
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_images}"}}
                ]
            }
        ], 
        max_tokens=200
    )

    return response.choices[0].message.content

encoded_images = encode_images_to_base64(image_url)

for i, image in enumerate(encoded_images):
    if image:
        user_query = "Describe the image in one sentence."
        model_response = generate_model_response(image, user_query)
        print(f"Image {i+1} Description: {model_response}\n")
    else:
        print(f"Image {i+1} could not be processed due to download failure.\n")

image = encoded_images[0]
print("Q: How many cars are in this image?")
print("A:", generate_model_response(image, "How many cars are in this image?"))

image = encoded_images[2]
print("Q: How severe is the damage in this image?")
print("A:", generate_model_response(image, "How severe is the damage in this image?"))

image = encoded_images[3]
print("Q: How much sodium is in this product?")
print("A:", generate_model_response(image, "How much sodium is in this product?"))

print("Q: How much cholesterol is in this product?")
print("A:", generate_model_response(image, "How much cholesterol is in this product?"))


image = encoded_images[1]
print("Q: What is the color of the woman's jacket?")
print("A:", generate_model_response(image, "What is the color of the woman's jacket?"))


