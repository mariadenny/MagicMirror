# encode_friend.py
import face_recognition
from PIL import Image
import numpy as np
import json

# Load the image using PIL and ensure RGB format
input_path = 'friend.jpeg'
rgb_path = 'server/friend_rgb.jpg'

# Convert and save as RGB (if not already)
img = Image.open(input_path).convert('RGB')
img.save(rgb_path)
image_np = np.array(img)

# Get face encodings
encodings = face_recognition.face_encodings(image_np)

if not encodings:
    print("❌ No face detected in the image.")
else:
    # Save encoding to JSON (optional)
    data = {
        "name": "friend",
        "encoding": encodings[0].tolist()
    }
    with open("server/friend.json", "w") as f:
        json.dump(data, f)

    print("✅ Encoding successful. Saved as:")
    print("  - RGB image:", rgb_path)
    print("  - Encoding JSON: server/friend.json")
