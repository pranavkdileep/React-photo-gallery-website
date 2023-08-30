import requests
import torch
import modin.pandas as pd
from diffusers import DiffusionPipeline
from PIL import Image
import numpy as np
import random

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

def get_prompts():
    
    return results

def delete_prompt(image_id):
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='sql.freedb.tech',
        user='freedb_pkdart',
        password='e2Q#U?#QD$2ms7v',
        database='freedb_testingkk'
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Define the SQL query to delete the prompt with the specified image_id
    query = "DELETE FROM prompts WHERE image_id = %s"

    # Execute the query with the image_id as a parameter
    cursor.execute(query, (image_id,))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()


prompts = get_prompts()
for prompt in prompts:
    image_id, prompt_text, negative_prompt, height, width = prompt
    print(f"Image ID: {image_id}")
    print(f"Prompt: {prompt_text}")
    print(f"Negative Prompt: {negative_prompt}")
    print(f"Height: {height}")
    print(f"Width: {width}")
    print()
    output_filename = f"image{image_id}.png"
    genie_and_save(prompt, negative_prompt, height, width, scale, steps, output_filename=output_filename)
    delete_prompt(image_id)
