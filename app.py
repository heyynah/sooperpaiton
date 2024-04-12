from flask import Flask, request, send_file, render_template, jsonify
from werkzeug.utils import secure_filename
import subprocess
import os

app = Flask(__name__)

# Define the directory to store uploaded images
UPLOAD_FOLDER = 'ESRGAN/LR/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

        # Call the Python script with subprocess
        script_path = 'ESRGAN/test.py'
        python_process = subprocess.Popen(['python', script_path, file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = python_process.communicate()

        # Check for errors
        if stderr:
            print('Error:', stderr)
            return jsonify({'error': 'Internal server error'}), 500

        # Assuming stdout contains the path to the processed image
        processed_image_path = stdout.decode().strip()
        print('Processed image path:', processed_image_path)

        # Return the path to the processed image
        return jsonify({'processed_image_path': processed_image_path}), 200

@app.route('/processed_images/<path:image_name>')
def get_processed_image(image_name):
    print('Getting processed image...')
    image_path = os.path.join('ESRGAN', 'results', image_name)
    print('Image path:', image_path)
    
    return send_file(image_path)
    
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=3000)
