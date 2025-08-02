# server/recognize.py
import face_recognition

def recognize_face(known_image_path, unknown_image_path):
    try:
        # Load and convert both images to RGB
        known_image = face_recognition.load_image_file(known_image_path)
        unknown_image = face_recognition.load_image_file(unknown_image_path)

        known_encodings = face_recognition.face_encodings(known_image)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        if not known_encodings or not unknown_encodings:
            return "unknown"

        known_encoding = known_encodings[0]
        unknown_encoding = unknown_encodings[0]

        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        return "friend" if results[0] else "unknown"
    except Exception as e:
        print("Recognition error:", e)
        return "error"
