from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from predict_model import predict_from_image

# Use root as template folder
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')  # index.html in root folder

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    if file.filename == '':
        return 'No file selected', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Load image and run prediction
    image = cv2.imread(filepath)
    predicted_class, confidence, label = predict_from_image(image)

    if label == 'friend':
        return redirect('/sreemrudu.html')
    else:
        return redirect('/non_sreemrudu.html')

@app.route('/<path:filename>')
def serve_static_file(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
