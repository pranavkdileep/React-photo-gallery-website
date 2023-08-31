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

details = get_prompt()
prompt = details[0]
negative_prompt = details[1]
height = details[2]
width = details[3]
image_id =details[4]
print("Prompt: " + prompt)
print("Negative Prompt: " + negative_prompt)
print("Height: " + str(height))
print("Width: " + str(width))
print("image id: " + str(image_id))

del_image(image_id)

