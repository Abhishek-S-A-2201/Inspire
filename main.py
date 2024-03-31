import threading
import subprocess
import time
import sys
import os


def download_models():

    def download_hugginface(url, destination_folder, original_folder):
        print(f"Downloading from {url}...")
        os.chdir(destination_folder)
        os.system(f"wget --content-disposition {url}")
        os.chdir(original_folder)

    download_hugginface(
        "https://huggingface.co/Abhishek-Anand/Inspire/resolve/main/epicrealism_naturalSinRC1VAE.safetensors?download=true",
        "./Inspire/ComfyUI/models/checkpoints/",
        "../../../../"
    )

    download_hugginface(
        "https://huggingface.co/Abhishek-Anand/Inspire/resolve/main/controlnet11Models_softedge.safetensors?download=true",
        "./Inspire/ComfyUI/models/controlnet/",
        "../../../../"
    )

    download_hugginface(
        "https://huggingface.co/Abhishek-Anand/Inspire/resolve/main/model.safetensors?download=true",
        "./Inspire/ComfyUI/models/clip_vision/",
        "../../../../"
    )
    download_hugginface(
        "https://huggingface.co/Abhishek-Anand/Inspire/resolve/main/ip-adapter-plus_sd15.safetensors?download=true",
        "./Inspire/ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus/models/",
        "../../../../../"
    )


download_models()


def start_comfyui():
    subprocess.run(["python", "Inspire/ComfyUI/main.py"])


def start_streamlit():
    subprocess.run(["streamlit", "run", "Inspire/app.py"])


t1 = threading.Thread(target=start_comfyui)
t2 = threading.Thread(target=start_streamlit)

t1.start()
time.sleep(5)
t2.start()

t2.join()
sys.exit("Execution complete...")
