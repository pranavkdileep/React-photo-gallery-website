import requests

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

prompt = "hellpp"
negative_prompt = "help"
height =  512
width = 512
image_id = 5744426648
image_link = "https://i.imgur.com/5Z3Z1ZP.png"
print(upload_db(image_link, image_id, prompt, negative_prompt, height, width))