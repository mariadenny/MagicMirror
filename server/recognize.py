import face_recognition
import cv2

# Load your friend's image and encode it
known_image = face_recognition.load_image_file(r"C:\Users\maria\OneDrive\Desktop\useless\server\friend.jpeg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Start webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Camera error")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces and get encodings
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        match = face_recognition.compare_faces([known_encoding], face_encoding)[0]

        if match:
            print("✅ Match found - Your Friend 👯‍♀️")
            video_capture.release()
            cv2.destroyAllWindows()
            exit()
        else:
            print("❌ Not your friend")

    cv2.imshow('Face Recognition', frame)

    # Press 'q' to quit manually
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
