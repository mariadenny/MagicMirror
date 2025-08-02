import tensorflow as tf
import numpy as np
import cv2

class FriendClassifier:
    def __init__(self, model_path):
        self.model = tf.saved_model.load(model_path)
        self.infer = self.model.signatures['serving_default']
        self.labels = {0: "friend", 1: "not_friend"}

    def preprocess_image(self, image, target_size=(224, 224)):
        image = cv2.resize(image, target_size)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype(np.float32) / 255.0
        image = np.expand_dims(image, axis=0)
        return image

    def predict(self, image):
        try:
            processed = self.preprocess_image(image)
            tensor = tf.constant(processed)
            output = self.infer(tensor)
            key = list(output.keys())[0]
            result = output[key].numpy()

            if result.shape[-1] == 1:  # binary
                confidence = float(result[0][0])
                predicted_class = 1 if confidence > 0.5 else 0
                confidence = confidence if predicted_class == 1 else 1 - confidence
            else:
                predicted_class = np.argmax(result[0])
                confidence = float(result[0][predicted_class])

            label = self.labels[predicted_class]
            return predicted_class, confidence, label
        except Exception as e:
            print("Prediction error:", e)
            return None, None, None

# This is the function Flask will call
model = FriendClassifier(r"D:\magicmirror\src\converted_savedmodel\model.savedmodel")
def predict_from_image(img):
    return model.predict(img)
