import cv2
import numpy as np
import tensorflow as tf
import os
from datetime import datetime

class FriendClassifier:
    def __init__(self, model_path):
        """
        Initialize the friend classifier with a saved TensorFlow model
        
        Args:
            model_path (str): Path to the saved_model.pb directory
        """
        self.model_path = model_path
        self.model = None
        self.labels = {0: "friend", 1: "not_friend"}
        self.load_model()
        
    def load_model(self):
        """Load the TensorFlow SavedModel"""
        try:
            self.model = tf.saved_model.load(self.model_path)
            print(f"Model loaded successfully from {self.model_path}")
            
            # Get the inference function
            self.infer = self.model.signatures['serving_default']
            print("Model signatures:", list(self.model.signatures.keys()))
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def preprocess_image(self, image, target_size=(224, 224)):
        """
        Preprocess the image for model input
        
        Args:
            image: OpenCV image array
            target_size: Tuple of target dimensions (width, height)
            
        Returns:
            Preprocessed image array ready for model input
        """
        # Resize image
        image_resized = cv2.resize(image, target_size)
        
        # Convert BGR to RGB (OpenCV uses BGR, most models expect RGB)
        image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values to [0, 1]
        image_normalized = image_rgb.astype(np.float32) / 255.0
        
        # Add batch dimension
        image_batch = np.expand_dims(image_normalized, axis=0)
        
        return image_batch
    
    def predict(self, image):
        """
        Make prediction on the input image
        
        Args:
            image: OpenCV image array
            
        Returns:
            Tuple of (predicted_class, confidence, label)
        """
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image)
            
            # Convert to tensor
            input_tensor = tf.constant(processed_image)
            
            # Make prediction
            # Note: You might need to adjust the input key based on your model
            # Common keys are 'input_1', 'inputs', 'x', etc.
            predictions = self.infer(input_tensor)
            
            # Get the output (adjust key based on your model's output)
            # Common keys are 'output_1', 'predictions', 'dense', etc.
            output_key = list(predictions.keys())[0]  # Get first output key
            output = predictions[output_key].numpy()
            
            # Get predicted class and confidence
            if output.shape[-1] == 1:  # Binary classification with sigmoid
                confidence = float(output[0][0])
                predicted_class = 1 if confidence > 0.5 else 0
                confidence = confidence if predicted_class == 1 else 1 - confidence
            else:  # Multi-class with softmax
                predicted_class = np.argmax(output[0])
                confidence = float(output[0][predicted_class])
            
            label = self.labels[predicted_class]
            
            return predicted_class, confidence, label
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None, None, None

def main():
    # Configuration
    MODEL_PATH = r"./converted_savedmodel/model.savedmodel/"  # Update this path
    SAVE_IMAGES = True  # Set to True if you want to save captured images
    IMAGE_SAVE_DIR = "captured_images"
    
    # Create image save directory if needed
    if SAVE_IMAGES and not os.path.exists(IMAGE_SAVE_DIR):
        os.makedirs(IMAGE_SAVE_DIR)
    
    # Initialize the classifier
    try:
        classifier = FriendClassifier(MODEL_PATH)
    except Exception as e:
        print(f"Failed to initialize classifier: {e}")
        return
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)  # Use 0 for default camera
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Webcam initialized successfully!")
    print("Controls:")
    print("- Press SPACEBAR to capture and classify image")
    print("- Press 'q' to quit")
    print("- Press 's' to save current frame without classification")
    
    frame_count = 0
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame from webcam")
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Display instructions on frame
        cv2.putText(frame, "Press SPACEBAR to classify", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show the frame
        cv2.imshow('Friend Classifier - Webcam Feed', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Spacebar pressed
            print("Capturing and classifying image...")
            
            # Make prediction
            predicted_class, confidence, label = classifier.predict(frame)
            
            if predicted_class is not None:
                # Display result
                result_text = f"Prediction: {label} (Confidence: {confidence:.2f})"
                print(result_text)
                
                # Create a copy of frame for result display
                result_frame = frame.copy()
                
                # Choose color based on prediction
                color = (0, 255, 0) if predicted_class == 0 else (0, 0, 255)  # Green for friend, Red for not_friend
                
                # Add prediction text to frame
                cv2.putText(result_frame, f"Result: {label}", (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.putText(result_frame, f"Confidence: {confidence:.2f}", (10, 160), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                
                # Show result for 3 seconds
                cv2.imshow('Friend Classifier - Result', result_frame)
                cv2.waitKey(3000)  # Wait 3 seconds
                cv2.destroyWindow('Friend Classifier - Result')
                
                # Save image if enabled
                if SAVE_IMAGES:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{IMAGE_SAVE_DIR}/capture_{timestamp}_{label}_{confidence:.2f}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"Image saved as: {filename}")
                    
            else:
                print("Failed to classify image")
        
        elif key == ord('s'):  # Save current frame
            if SAVE_IMAGES:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{IMAGE_SAVE_DIR}/manual_save_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Frame saved as: {filename}")
        
        elif key == ord('q'):  # Quit
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Application closed")

if __name__ == "__main__":
    main()