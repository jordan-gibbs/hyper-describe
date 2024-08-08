import streamlit as st
import requests
import base64
from PIL import Image
import os

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to get image description from the API
def get_image_description(api_key, image_path):
    base64_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
                        Describe the image with the highest level of detail possible. Start by identifying the type of image (e.g., meme, photo, painting, social media post) and its overall theme and purpose. Then, provide details for the following categories:
                        Primary Focus: Describe the main subjects or focal points.
                        Context and Setting: Outline the general environment or background, including time and place if relevant.
                        Composition and Layout: Explain the arrangement of elements, balance, symmetry, perspective, and use of space.
                        Color and Tone: Describe the dominant colors, overall color scheme, and mood conveyed by the colors.
                        Text and Typography (if applicable): Detail the presence of text, font style, size, placement, and relationship with visual elements.
                        Actions and Interactions: Describe activities or movements depicted and interactions between subjects or elements.
                        Emotions and Expressions: Provide details on the emotional tone, facial expressions, and body language of subjects.
                        Details and Accessories: Note any notable details or accessories like clothing, objects, symbols, or icons.
                        Medium and Style: Indicate the medium used and artistic style or technique.
                        Cultural and Historical Context: Mention any cultural or historical references and their relevance.
                        Popular Media: If the image contains any sort of popular media, please try to identify it. I.e. if it is from a TV show or movie, please try to guess which media it is from. If you cannot output this, describe it generally so it could be identified by a savvy person.
                        For people within the image, describe their physical appearance without naming specific individuals:
                        Physical Appearance: Gender, age, ethnicity, height, build, posture, hair color, style, length, eye color, shape, facial features.
                        Attire and Accessories: Clothing type, style, color, footwear, accessories, unique or notable items.
                        Behavior and Actions: Specific actions or activities, interaction with other people or objects, gestures, and movements.
                        Expressions and Emotions: Facial expressions, overall demeanor, and mood.
                        Do not repeat yourself when describing these aspects. If one or more are already covered, do not spend more time writing about it.
                        Write in markdown, and be exhaustively descriptive and ultra verbose. If the sections are not relevant, simply do not output them. Never forcibly output a section if it's not entirely relevant. 
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 3000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()
    description = response_json['choices'][0]['message'][
        'content'] if 'choices' in response_json else "Description not available"

    return description





# Streamlit app
st.set_page_config(
    page_title="Hyper-Detail Image Describer",
    page_icon="🔍",  # You can choose any emoji as the icon
    layout="wide",
    initial_sidebar_state="auto",
)

with open("style.css") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

hide_streamlit_style = """
            <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("🔍Hyper-Detail Image Describer")
st.markdown("###### Upload an image to get a painstakingly detailed description.")

api_key = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and api_key:
    image = Image.open(uploaded_file)
    st.image(image, width=300)
    st.write("")

    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    with st.spinner("Generating Description..."):
        description = get_image_description(api_key, "temp_image.jpg")
        st.write(description)
