from flask import Flask, request, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
import subprocess
import os
from ESRGAN.test import test_esrgan

app = Flask(__name__)

# Define the directory to store uploaded images
UPLOAD_FOLDER = 'ESRGAN/LR/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the directory to store processed images
RESULTS_FOLDER = 'ESRGAN/results/'
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

# Define the route to process the image
@app.route('/process_image', methods=['POST'])
def process_image():
    print('Processing image...')
    # Check if the POST request has a file part
    if 'image' not in request.files:
        print('No file part')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        print('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    # If the file is valid, save it to the UPLOAD_FOLDER
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print('File saved to:', file_path)

        # Call the ESRGAN testing function
        processed_image_path = test_esrgan(file_path)

        # Return the path to the processed image
        return jsonify({'processed_image_path': processed_image_path}), 200

@app.route('/processed_images/<path:image_name>')
def get_processed_image(image_name):
    print('Getting processed image...')
    return send_from_directory(app.config['RESULTS_FOLDER'], image_name)
    
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=3000)
