import requests
import json
import torch
import modin.pandas as pd
from diffusers import DiffusionPipeline
from PIL import Image
import numpy as np
import random

def get_prompt():
    url = "https://orange-trout-gww74r967j62vwgr-5000.app.github.dev/getprompt"
    response = requests.get(url)
    if response.text == "No prompts in database":
        return "No prompts in database"
    else:
        response_json = response.json()
        prompt = response_json.get("prompt")
        negative_prompt = response_json.get("negative_prompt")
        height = response_json.get("height")
        width = response_json.get("width")
        image_id = response_json.get("image_id")
        return prompt, negative_prompt, height, width, image_id

def del_image(image_id):
    url = "https://orange-trout-gww74r967j62vwgr-5000.app.github.dev/del_image/" + str(image_id)
    response = requests.get(url)
    response_json = response.json()
    return response_json

def genie_and_save(prompt, negative_prompt, height, width, scale, steps, output_filename="image.png"):
    # Generate a random seed between 1 and 999999999999999999
    seed = random.randint(1, 999999999999999999)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.cuda.is_available():
        PYTORCH_CUDA_ALLOC_CONF = {'max_split_size_mb': 60000}
        torch.cuda.max_memory_allocated(device=device)
        torch.cuda.empty_cache()
        pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True)
        pipe.enable_xformers_memory_efficient_attention()
        pipe = pipe.to(device)
        torch.cuda.empty_cache()
        refiner = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0", use_safetensors=True, torch_dtype=torch.float16, variant="fp16")
        refiner.enable_xformers_memory_efficient_attention()
        refiner.enable_sequential_cpu_offload()
    else:
        pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", use_safetensors=True)
        pipe = pipe.to(device)
        refiner = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0", use_safetensors=True)
        refiner = refiner.to(device)

    generator = torch.Generator(device=device).manual_seed(seed)
    int_image = pipe(prompt, negative_prompt=negative_prompt, height=height, width=width, num_inference_steps=steps, guidance_scale=scale, num_images_per_prompt=1, generator=generator, output_type="latent").images
    image = refiner(prompt=prompt, negative_prompt=negative_prompt, image=int_image).images[0]

    image.save(output_filename)
    print("Saved")

def upload_image(output_filename):
    CLIENT_ID = "84c0409dd10cadb"
    headers = {
        'Authorization': f'Client-ID {CLIENT_ID}'
    }
    url = 'https://api.imgur.com/3/upload.json'
    data = {
        'image': open(output_filename, 'rb').read(),
    }
    response = requests.post(url, headers=headers, data=data)
    json_response = response.json()

    if response.status_code == 200 and json_response.get('data'):
        link = json_response['data']['link']
        print("Image uploaded successfully. Link:", link)
        return link
    else:
        print("Error uploading image:", json_response.get('data', {}).get('error', 'Unknown error'))
        return "Error uploading image:", json_response.get('data', {}).get('error', 'Unknown error')
    
def upload_db(image_link, image_id, prompt, negative_prompt, height, width):
    url = "https://orange-trout-gww74r967j62vwgr-5000.app.github.dev/upload_db"
    data = {
        'image_link': image_link,
        'image_id': image_id,
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'height': height,
        'width': width
    }
    response = requests.post(url, data=data)
    return response.text

while True:
    details = get_prompt()
    if details == "No prompts in database":
        print("No prompts in database")
        continue
    else:
        prompt = details[0]
        negative_prompt = details[1]
        height = details[2]
        width = details[3]
        image_id = details[4]
        output_filename = str(image_id) + ".png"
        genie_and_save(prompt, negative_prompt, height, width, scale=10, steps=25, output_filename=output_filename)
        print("Generated")
        print(del_image(image_id))
        image_link = upload_image(output_filename)
        print(image_link)
        print(upload_db(image_link, image_id, prompt, negative_prompt, height, width))

