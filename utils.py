import requests
import json
import requests
import time
import glob
import io
from PIL import Image
import random


def get_generate_image_prompt(workflow, client_id, positive, colors, no_of_images, main_strength, prompt_strength):
    f = open(workflow, 'r')
    prompt = json.loads(f.read())

    id_to_class_type = {id: details['class_type']
                        for id, details in prompt.items()}

    main = [key for key, value in id_to_class_type.items()
              if value == 'IPAdapterAdvanced'][0]
    prompt.get(main)['inputs']['weight'] = main_strength

    load_main_image = [
        key for key, value in id_to_class_type.items() if value == 'LoadImage'][0]
    prompt.get(load_main_image)['inputs']['image'] = f'{client_id}_main.jpg'

    save_image = [key for key, value in id_to_class_type.items()
                  if value == 'SaveImage'][0]
    prompt.get(save_image)['inputs']['filename_prefix'] = str(client_id)

    positive_prompt = [
        key for key, value in id_to_class_type.items() if value == 'CLIPTextEncode'][-1]
    positive = f"{positive}\n({colors}): 1.5"
    prompt.get(positive_prompt)['inputs']['text'] = positive

    k_sampler = [key for key, value in id_to_class_type.items()
                 if value == 'KSampler'][0]
    prompt.get(k_sampler)['inputs']['seed'] = random.randint(10**14, 10**15-1)
    prompt.get(k_sampler)['inputs']['cfg'] = prompt_strength

    return prompt

def generate_imageless_workflow(workflow, client_id, positive, colors, no_of_images, prompt_strength):
    f = open(workflow, 'r')
    prompt = json.loads(f.read())

    id_to_class_type = {id: details['class_type']
                        for id, details in prompt.items()}

    empty_image = [key for key, value in id_to_class_type.items()
                   if value == 'EmptyLatentImage'][0]
    prompt.get(empty_image)['inputs']['batch_size'] = no_of_images

    save_image = [key for key, value in id_to_class_type.items()
                  if value == 'SaveImage'][0]
    prompt.get(save_image)['inputs']['filename_prefix'] = str(client_id)

    positive_prompt = [
        key for key, value in id_to_class_type.items() if value == 'CLIPTextEncode'][-1]
    positive = f"{positive}\n({colors}): 1.5"
    prompt.get(positive_prompt)['inputs']['text'] = positive

    k_sampler = [key for key, value in id_to_class_type.items()
                 if value == 'KSampler'][0]
    prompt.get(k_sampler)['inputs']['seed'] = random.randint(10**14, 10**15-1)
    prompt.get(k_sampler)['inputs']['cfg'] = prompt_strength

    return prompt

def image_processing(workflow, client_id):
    f = open(workflow, 'r')
    prompt = json.loads(f.read())

    id_to_class_type = {id: details['class_type']
                        for id, details in prompt.items()}

    load_main_image = [
        key for key, value in id_to_class_type.items() if value == 'LoadImage'][0]
    prompt.get(load_main_image)['inputs']['image'] = f'{client_id}_main.jpg'

    save_image = [key for key, value in id_to_class_type.items()
                  if value == 'SaveImage'][0]
    prompt.get(save_image)['inputs']['filename_prefix'] = str(client_id)

    return prompt


def queue_prompt(prompt, client_id, server_address: str = "http://127.0.0.1:8188"):
    p = {"prompt": prompt, "client_id": client_id}
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(p).encode('utf-8')
    req = requests.post("{}/prompt".format(server_address),
                        data=data, headers=headers)
    return req.json()


def upload_image(image, type: str, clientID: str):
    image = Image.open(io.BytesIO(image.getvalue()))
    destination = f'./Inspire/ComfyUI/input/{clientID}_{type}.jpg'
    image = image.convert("RGB")
    image.save(destination)
    print("File uploaded...")


def get_queue(server_address: str = "http://127.0.0.1:8188", ttl: int = 10):
    time.sleep(5)
    try:
        headers = {'Content-Type': 'application/json'}
        while True:
            time.sleep(ttl)
            req = requests.get(
                "{}/queue".format(server_address), headers=headers)
            req = req.json()
            if req['queue_running'] or req['queue_pending']:
                print(
                    f"\n\n{len(req['queue_pending'])+len(req['queue_running'])} prompt in queue...\n\n")
            else:
                print('All prompts completed executing...')
                break
    except Exception as e:
        print(e)


def get_outputs(client_id):
    time.sleep(10)
    images = [""]*4
    for idx, image in enumerate(glob.glob(f"./Inspire/ComfyUI/output/{client_id}*")):
            images[idx] = image
    if not images:
        images = ['./Inspiretest_images/Toonyou.jpeg', './Inspire/test_images/pixelart.jpeg',
                  './Inspiretest_images/painting.png', './Inspiretest_images/seekyou.png']
    return images
