from openai import OpenAI
import streamlit as st
import numpy as np
from io import BytesIO
from PIL import Image
import requests
openai_api_key = st.secrets["openai_key"]
client=OpenAI(api_key=openai_api_key)

st.markdown(
"""
<style>
    [data-testid="stSidebarNavItems"] li:nth-child(1) {
        display: none;
    }
</style>
""",
    unsafe_allow_html=True,
)

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://lh3.googleusercontent.com/a/ACg8ocK_OgY-g9V-VG07tj59v_RE9qBRNxWFmSjTk7DbIViw5IA=s260-c-no);
                background-repeat: no-repeat;
                background-size: 100px 100px;
                padding-top: 60px;
                background-position: 120px 50px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "AI, ML, & Prompt Engineering";
                padding-bottom: 30px;
                font-size: 18px;
                display: flex;
                justify-content: center;
                position: relative;
                top: 100px;
            }[data-testid="stSidebarNav"]::after {
                content: "© 2023-2024 J. Davis";
                width: 100%;
                font-size: 14px;
                justify-content: center;
                display: flex;
                position: relative;
                top: 100px;
            }
            [data-testid="stSidebarNavLink"] span {
                font-size: 11px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()

st.title("🎆 OpenAI DALL-E Text To Image Generation") 
st.caption("Prompted artwork powered by OpenAI DALL-E Model")

# ----------------------------------------------
# CTA BUTTON
if "messages" in st.session_state:
    url = "/OpenAI%20Text%20To%20Image%20Generation"
    st.markdown(
        f'<div><a href="{url}" target="_self" style="justify-content:center; padding: 10px 10px; background-color: #2D2D2D; color: #efefef; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px;">Clear History</a></div><br /><br />',
            unsafe_allow_html=True
        )



if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "I am feeling creative today! What would you like to generate an image of?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # ----------------------------------------------
    # GENERATE IMAGE
    response = client.images.generate(
        model="dall-e-3",
        #prompt="a photorealistic AKC Alaskan Malamute puppy on a black background",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    st.image(image_url)


        
    with st.expander("View Image URL"):
        # ----------------------------------------------
        # DOWNLOAD BUTTON
        img = Image.open(requests.get(image_url, stream=True).raw)
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_image = buf.getvalue()

        btn = st.download_button(
            label="Download Image",
            data=byte_image,
            file_name="sweater.png",
            mime="image/png",
            )
        st.markdown(image_url)
        