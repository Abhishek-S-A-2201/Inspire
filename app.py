import streamlit as st
import random
import threading
import os
import psutil
from utils import *

st.set_page_config(page_title='Inspire', page_icon="🎨" ,layout="wide")

cols = st.columns(5)
cols[0].title('🎨 Inspire')
quit_button = cols[-1].button("Quit", key="quit_button")
st.subheader('Get inspiration from AI generated images.')

# Accept text prompt
style = st.text_input("Enter a style:", key='3')

col = st.columns(2)
colors = col[0].text_input("Enter the colors:", key='4')
num_images = col[1].number_input(
    "Number of images:", key="number_input", step=1, value=4)

prompt_strength = st.slider(
    "Set prompt strength:", min_value=0.0, max_value=20.0, step=0.5, key='1', value=9.0)

# Create two columns with image uploaders
col1, col2 = st.columns(2)
main = col1.file_uploader("Upload main image", type=["jpg", "jpeg", "png"])
background = col2.file_uploader(
    "Upload background image", type=["jpg", "jpeg", "png"], key="Prompt Strength")


# Create a slider with specified range and step
main_strength = col1.slider(
    "Set image strength:", min_value=0.0, max_value=1.0, step=0.1, key='54', value=0.5)
background_strength = col2.slider(
    "Set background image strength:", min_value=0.0, max_value=1.0, step=0.1, key='2', value=0.5)

button_clicked = st.button("Generate Images", key="process_button")

if quit_button:
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()


# Process images if uploaded
if button_clicked and main is not None and background is not None:
    client_id = random.randint(10**14, 10**15-1)

    upload_image(main, "main", client_id)
    upload_image(background, "bg", client_id)
    workflow = "./workflow.json"
    prompt = get_prompt(workflow, client_id, style, colors,
                        num_images, main_strength, background_strength, prompt_strength)
    queue_prompt(prompt, client_id)

    t1 = threading.Thread(target=get_queue)
    t1.start()
    with st.spinner('Generating Images...'):
        t1.join()

    images = get_outputs(client_id)
    cols = st.columns(len(images))
    for idx, img in enumerate(images):
        if img:
            cols[idx].image(img)
else:
    if main is None or background is None:
        warning_text = ''
        if main is None and background is None:
            warning_text = 'Please upload the MAIN image and BACKGROUND image'
        elif main is None:
            warning_text = 'Please upload the MAIN image'
        else:
            warning_text = 'Please upload the BACKGROUND image'
        st.warning(warning_text)
