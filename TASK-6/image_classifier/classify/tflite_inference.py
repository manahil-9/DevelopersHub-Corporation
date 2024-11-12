import tensorflow as tf
from tensorflow import lite as tflite
from tensorflow.lite.python.interpreter import Interpreter
import numpy as np
from PIL import Image

class ImageClassifier:
    def __init__(self, model_path):
        # Load the TFLite model
        self.interpreter = tf.lite.Interpreter(model_path=model_path)  # Use the passed model_path variable
        self.interpreter.allocate_tensors()

    def predict(self, image_path):
        # Prepare the image for prediction
        try:
            # Open the image from the provided path and resize it to match model input size
            img = Image.open(image_path).resize((224, 224))
        except Exception as e:
            raise ValueError(f"Error loading image: {e}")

        # Convert image to numpy array and preprocess
        img = np.array(img, dtype=np.float32)
        img = img / 255.0  # Normalize pixel values to [0, 1]
        img = np.expand_dims(img, axis=0)  # Add batch dimension (1, 224, 224, 3)
        
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # Ensure the input tensor is set correctly (typically float32)
        if input_details[0]['dtype'] == np.float32:
            self.interpreter.set_tensor(input_details[0]['index'], img)

        # Run inference
        self.interpreter.invoke()

        # Get the prediction result
        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        probabilities = tf.nn.softmax(output_data[0]).numpy()  # Apply softmax if logits are returned
        
        # Convert to percentages
        probabilities_percentage = probabilities * 100
        
        # Identify the index of the maximum probability
        max_index = np.argmax(probabilities_percentage)
        max_probability = probabilities_percentage[max_index]

        return max_index, max_probability

def get_prediction(image_path, model_path, classes):
    # Instantiate the ImageClassifier and make a prediction
    classifier = ImageClassifier(model_path)
    max_index, max_probability = classifier.predict(image_path)
    
    # Return the class label and prediction percentage for the highest probability
    predicted_class = classes[max_index]
    return f"{predicted_class}: {max_probability:.2f}%"

# Example usage
if __name__ == "__main__":
    model_path = "models/model_unquant.tflite"
    image_path = "original_images"
    classes = ['Everyday Objects', 'Nature and Scenery', 'Animals and Miscellaneous']  # Replace with your actual class labels
    prediction = get_prediction(image_path, model_path, classes)
    print(f"Prediction: {prediction}")
