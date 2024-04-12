import streamlit as st
import random
import threading
import os
import psutil
from utils import *
import uuid

st.set_page_config(page_title='Inspire', page_icon="🎨" ,layout="wide")

st.title('🎨 Inspire')

st.subheader('Get inspiration from AI generated images.')
st.text("")
st.text("")
st.text("")

options = st.sidebar.selectbox('How would you like to be contacted?',('Generate Images', 'Combine Images', 'Upscale Image', 'Remove Background'))
quit_button = st.sidebar.button("Quit", key="quit_button")

if quit_button:
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()


if options == "Generate Images":

    st.header("Generate Images")
    # Accept text prompt
    style = st.text_input("Enter a style:", key='3')

    col = st.columns(2)
    colors = col[0].text_input("Enter the colors:", key='4')
    num_images = col[1].number_input(
        "Number of images:", key="number_input", step=1, value=2, max_value=4, min_value=1)

    prompt_strength = st.slider(
        "Set prompt strength:", min_value=0.0, max_value=20.0, step=0.5, key='1', value=6.0)

    # Create two columns with image uploaders
    main = st.file_uploader("Upload inspiration image", type=["jpg", "jpeg", "png"])

    # Create a slider with specified range and step
    main_strength = st.slider(
        "Set image strength:", min_value=0.0, max_value=1.0, step=0.1, key='54', value=0.8)

    button_clicked = st.button("Generate Images", key="process_button")

    # Process images if uploaded
    if button_clicked:
        if main is not None:
            client_id = str(uuid.uuid4())

            upload_image(main, "main", client_id)
            workflow = "Inspire/workflows/generate_image_workflow.json"
            prompt = get_generate_image_prompt(workflow, client_id, style, colors,
                                num_images, main_strength, prompt_strength)
            queue_prompt(prompt, client_id)

            t1 = threading.Thread(target=get_queue, args=(10,))
            t1.start()
            with st.spinner('Generating Images...'):
                t1.join()
                images = get_outputs(client_id, 4)

            cols = st.columns(len(images))
            for idx, img in enumerate(images):
                if img:
                    cols[idx].image(img)
        else:
            client_id = str(uuid.uuid4())

            workflow = "Inspire/workflows/generate_imageless_workflow.json"
            prompt = generate_imageless_workflow(workflow, client_id, style, colors,
                                num_images, prompt_strength)
            queue_prompt(prompt, client_id)

            t1 = threading.Thread(target=get_queue)
            t1.start()
            with st.spinner('Generating Images...'):
                t1.join()
                images = get_outputs(client_id, 4)

            cols = st.columns(len(images))
            for idx, img in enumerate(images):
                if img:
                    cols[idx].image(img)
    else:
        if main is None:
            warning_text = 'Please upload the Inspiration image'
            st.warning(warning_text)
elif options == "Combine Images":
    st.info("New features coming soon.Stay tuned...")

elif options == "Upscale Image":
    st.header("Upscale Image")

    # Create two columns with image uploaders
    main = st.file_uploader("Upload Upscale image", type=["jpg", "jpeg", "png"])

    button_clicked = st.button("Upscale Image", key="process_button")

    # Process images if uploaded
    if button_clicked and main is not None:
        client_id = str(uuid.uuid4())

        upload_image(main, "main", client_id)
        workflow = "Inspire/workflows/upscale_image.json"
        prompt = image_processing(workflow, client_id)
        queue_prompt(prompt, client_id)

        t1 = threading.Thread(target=get_queue, args=(5,))
        t1.start()
        with st.spinner('Upscaling Images...'):
            t1.join()
            images = get_outputs(client_id, 1)

        cols = st.columns(len(images))
        for idx, img in enumerate(images):
            if img:
                cols[idx].image(img)
    else:
        if main is None:
            warning_text = 'Please upload the Upscale image'
            st.warning(warning_text)

elif options == "Remove Background":
    st.header("Remove Background")

    # Create two columns with image uploaders
    main = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

    button_clicked = st.button("Remove Background", key="process_button")

    # Process images if uploaded
    if button_clicked and main is not None:
        client_id = str(uuid.uuid4())

        upload_image(main, "main", client_id)
        workflow = "Inspire/workflows/remove_image_background.json"
        prompt = image_processing(workflow, client_id)
        queue_prompt(prompt, client_id)

        t1 = threading.Thread(target=get_queue, args=(5,))
        t1.start()
        with st.spinner('Removing image background...'):
            t1.join()
            images = get_outputs(client_id, 1)

        cols = st.columns(len(images))
        for idx, img in enumerate(images):
            if img:
                cols[idx].image(img)
    else:
        if main is None:
            warning_text = 'Please upload the Upsacle image'
            st.warning(warning_text)
