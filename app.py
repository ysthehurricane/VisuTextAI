'''
Developer: Yash Patel
'''

from flask import Flask, render_template, request, jsonify
import requests
import os
from PIL import Image
from dotenv import load_dotenv
import base64
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_PATH", "/var/www/visutext/VisuTextAI/static/uploads")

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# "https://api-inference.huggingface.co/models/Lykon/DreamShaper"
# "https://api-inference.huggingface.co/models/stablediffusionapi/stable-diffusion-2-1",
# "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5",

HUGGINGFACE_API_URLS = [
    "https://api-inference.huggingface.co/models/stablediffusionapi/realistic-vision-51",
    "https://api-inference.huggingface.co/models/stablediffusionapi/deliberate-v2",
    "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V2.0",
    "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5",
]

HUGGINGFACE_API_CHATBOT_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"



HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")



def generate_images(text_prompt, negative_prompt):
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": text_prompt,
        "options": {"wait_for_model": True, "steps": 75, "guidance_scale": 7.5, "image_strength": 0.8}
    }

    images = []
    for url in HUGGINGFACE_API_URLS:
        try:
            response = requests.post(url, headers=headers, json=payload)
            time.sleep(3)
            if response.status_code == 200:
                images.append(response.content)
            else:
                images.append(None)
        except Exception as e:
            print(f"Error with model at {url}: {e}")
            images.append(None)
    return images

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image-generation')
def imageGen():
    return render_template('image-generation.html')

@app.route('/ai-chat-bot')
def chatGen():
    return render_template('ai-chat-bot.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    text_prompt = request.json.get('text_prompt', '')
    negative_prompt = request.json.get('negative_prompt', '')

    if not text_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    if not negative_prompt:
        return jsonify({"error": "Negative Prompt is required"}), 400

    try:
        images_data = generate_images(text_prompt, negative_prompt)
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error": "Failed to generate images"}), 500

    image_urls = []

    for idx, image_data in enumerate(images_data):
        if image_data:
            image_path = os.path.join('static', f'generated_image_{idx}.png')
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data)
            image_urls.append(image_path)
        else:
            image_urls.append(None)

    return jsonify({
        "image_urls": image_urls,
        "text_prompt": text_prompt,
        "negative_prompt": negative_prompt
    })


@app.route('/chat', methods=['GET','POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }

    # Send request to Hugging Face API
    response = requests.post(
        HUGGINGFACE_API_CHATBOT_URL,
        headers=headers,
        json={"inputs": user_input}
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch response from the chatbot"}), 500

    bot_response = response.json()[0]["generated_text"]
    
    return jsonify({"message": bot_response})
    
if __name__ == '__main__':
    app.run(debug=True)