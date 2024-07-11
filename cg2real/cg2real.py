import os
import replicate
from PIL import Image
import tempfile
import urllib.request

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
if REPLICATE_API_TOKEN is None:
    raise Exception("REPLICATE_API_TOKEN must be set")

base_params = {
    "seed": 1337,
    "prompt": "photograph, professional photography, Nikon D850, 50mm, f/2.8, masterpiece, best quality, highres, <lora:more_details:0.5> <lora:SDXLrender_v2.0:1>",
    "dynamic": 3.00,
    "handfix": "disabled",
    "pattern": False,
    "sharpen": 0,
    "sd_model": "juggernaut_reborn.safetensors [338b85bc4f]",
    "scheduler": "DPM++ 3M SDE Karras",
    "creativity": 0.3,
    "downscaling": False,
    "resemblance": 0.7,
    "scale_factor": 2,
    "tiling_width": 80,
    "output_format": "png",
    "tiling_height": 80,
    "custom_sd_model": "",
    "negative_prompt": "(worst quality, low quality, normal quality, cgi, video game, artificial, painting, drawing:2) JuggernautNegative-neg",
    "num_inference_steps": 18,
    "downscaling_resolution": 768
}


def call_runway_api(image_path, width, height):
    with open(image_path, "rb") as image:
        params = dict(image=image, **base_params)
        output = replicate.run(
            "philz1337x/clarity-upscaler:dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e",
            input=params
        )
    
    res_url = output[0]
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_path = tmp_file.name + ".png"
    tmp_file.close()
    urllib.request.urlretrieve(res_url, tmp_path)
    res = Image.open(tmp_path).resize((width, height))
    res.save(tmp_path)
    return res

def call_with_retry(image_path, width, height):
    for i in range(3):
        try:
            return call_runway_api(image_path, width, height)
        except Exception as e:
            if i < 2:
                print("Runway API failed , retrying")
                print(e)
            else:
                print("Failed after max retries")
                raise
    raise Exception("Failed after max retries")

def upscale(image_path, image_path_out):
    image = Image.open(image_path)
    width = image.width
    height = image.height
    image = call_with_retry(image_path, width, height)
    image.save(image_path_out)
