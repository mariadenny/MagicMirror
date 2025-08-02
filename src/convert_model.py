import tensorflow as tf

# Load the SavedModel from the correct path
saved_model_path = r"D:\magicmirror\src\converted_savedmodel\model.savedmodel"
model = tf.saved_model.load(saved_model_path)

# Convert the loaded model into a functional Keras model
infer = model.signatures['serving_default']

# Get input and output tensors
input_tensor = list(infer.structured_input_signature[1].values())[0]
output_tensor = list(infer.structured_outputs.values())[0]

# Wrap into a tf.keras.Model
keras_model = tf.keras.Model(inputs=input_tensor, outputs=output_tensor)

# Save as .keras
keras_model.save(r"D:\magicmirror\server\model.keras")
print("✅ Model converted and saved as model.keras")
