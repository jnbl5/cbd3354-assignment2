import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Fetch API key from environment variables
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise ValueError("No API_KEY found in environment variables")

# Configure the API client
genai.configure(api_key=API_KEY)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    if not request.json or 'prompt' not in request.json:
        return jsonify({'error': 'No prompt provided'}), 400

    prompt = request.json['prompt']

    try:
        # Generate text using the API
        response = genai.generate_text(prompt=prompt)

        # Log the response object for debugging
        app.logger.info(f"Response object: {response}")

        # Assuming response.text contains the generated text
        generated_text = response.text if hasattr(response, 'text') else str(response)

        # Return the generated text
        return jsonify({'response': generated_text})
    except Exception as e:
        app.logger.error(f"Error generating response: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)