import threading
import subprocess
import time
import sys


def start_comfyui():
    subprocess.run(["python", "./ComfyUI/main.py"])


def start_streamlit():
    subprocess.run(["streamlit", "run", "app.py"])


t1 = threading.Thread(target=start_comfyui)
t2 = threading.Thread(target=start_streamlit)

t1.start()
time.sleep(5)
t2.start()

t2.join()
sys.exit("Execution complete...")
