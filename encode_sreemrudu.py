import face_recognition
import json

# Load the known image of Sreemrudu
image = face_recognition.load_image_file("server/real.jpg")
encodings = face_recognition.face_encodings(image)

if encodings:
    # Convert NumPy array to list and save as JSON
    data = encodings[0].tolist()
    with open("server/sreemrudu.json", "w") as f:
        json.dump(data, f)
    print("Encoding saved to sreemrudu.json")
else:
    print("No face found in the image!")

