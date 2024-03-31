import requests
import json
import requests
import time
import glob
import io
from PIL import Image


def get_prompt(workflow, client_id, positive, colors, no_of_images, main_strength, bg_strength, prompt_strength):
    f = open(workflow, 'r')
    prompt = json.loads(f.read())

    id_to_class_type = {id: details['class_type']
                        for id, details in prompt.items()}

    empty_image = [key for key, value in id_to_class_type.items()
                   if value == 'EmptyLatentImage'][0]
    prompt.get(empty_image)['inputs']['batch_size'] = no_of_images

    bg_net = [key for key, value in id_to_class_type.items()
              if value == 'ACN_AdvancedControlNetApply'][0]
    prompt.get(bg_net)['inputs']['strength'] = bg_strength

    fg_net = [key for key, value in id_to_class_type.items()
              if value == 'ACN_AdvancedControlNetApply'][1]
    prompt.get(fg_net)['inputs']['strength'] = main_strength

    load_main_image = [
        key for key, value in id_to_class_type.items() if value == 'LoadImage'][0]
    prompt.get(load_main_image)['inputs']['image'] = f'{client_id}_main.jpg'

    load_bg_image = [
        key for key, value in id_to_class_type.items() if value == 'LoadImage'][1]
    prompt.get(load_bg_image)['inputs']['image'] = f'{client_id}_bg.jpg'

    save_image = [key for key, value in id_to_class_type.items()
                  if value == 'SaveImage'][0]
    prompt.get(save_image)['inputs']['filename_prefix'] = str(client_id)

    positive_prompt = [
        key for key, value in id_to_class_type.items() if value == 'CLIPTextEncode'][-1]
    positive = f"{positive}\n({colors}): 1.5"
    prompt.get(positive_prompt)['inputs']['text'] = positive

    k_sampler = [key for key, value in id_to_class_type.items()
                 if value == 'KSampler'][0]
    prompt.get(save_image)['inputs']['cfg'] = prompt_strength

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
    destination = f'./ComfyUI/input/{clientID}_{type}.jpg'
    image = image.convert("RGB")
    image.save(destination)
    print("File uploaded...")


def get_queue(server_address: str = "http://127.0.0.1:8188"):
    time.sleep(10)
    try:
        headers = {'Content-Type': 'application/json'}
        while True:
            time.sleep(30)
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
    for idx, image in enumerate(glob.glob(f"./ComfyUI/output/{client_id}*")):
            images[idx] = image
    if not images:
        images = ['.test_images/Toonyou.jpeg', '.test_images/pixelart.jpeg',
                  '.test_images/painting.png', '.test_images/seekyou.png']
    return images
