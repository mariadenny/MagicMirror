import tensorflow as tf
print(tf.__version__)  # This checks if TensorFlow is working
from keras.models import load_model
from keras.preprocessing import image

print("✅ Imports successful!")

import numpy as np
import os

# Get model path relative to the project root
model_path = os.path.join(os.path.dirname(__file__), "..", "model", "friend_classifier.keras")
model = load_model(model_path)

# Load an image
img_path = os.path.join(os.path.dirname(__file__), "..", "images", "test_image.jpg")
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0

# Predict
prediction = model.predict(img_array)
predicted_class = np.argmax(prediction)
class_names = ["not_friend", "friend"]  # or whatever your class labels are

print("Prediction:", class_names[predicted_class])
