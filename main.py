import threading
import subprocess
import time
import sys
import os


def download_models():

    os.makedirs("./Inspire/ComfyUI/models/ipadapter")

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
        "https://huggingface.co/Abhishek-Anand/Inspire/resolve/main/model.safetensors?download=true",
        "./Inspire/ComfyUI/models/clip_vision/",
        "../../../../"
    )

    download_hugginface(
        "https://huggingface.co/Abhishek-Anand/Inspire/resolve/main/4xUltrasharp_4xUltrasharpV10.pt?download=true",
        "./Inspire/ComfyUI/models/upscale_models/",
        "../../../../"
    )

    download_hugginface(
        "https://huggingface.co/Abhishek-Anand/Inspire/resolve/main/ip-adapter-plus_sd15.safetensors?download=true",
        "./Inspire/ComfyUI/models/ipadapter/",
        "../../../../"
    )


if not os.path.exists("./Inspire/ComfyUI/models/checkpoints/epicrealism_naturalSinRC1VAE.safetensors"):
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
