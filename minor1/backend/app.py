from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Load models
try:
    pneumonia_model = tf.keras.models.load_model("pneumonia_detection_model.h5")
    print("Pneumonia model loaded successfully")
except Exception as e:
    print("Error loading pneumonia model:", e)

try:
    tumor_model = tf.keras.models.load_model("brain_tumor_detector.h5")
    print("Tumor model loaded successfully")
except Exception as e:
    print("Error loading tumor model:", e)


def preprocess_image(image, target_size):
    """Preprocess the image for the model."""
    image = image.resize(target_size)
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array /= 255.0  # Normalize to [0, 1]
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


@app.route("/predict/pneumonia", methods=["POST"])
def predict_pneumonia():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        processed_image = preprocess_image(image, target_size=(150, 150))  # Ensure size matches pneumonia model

        predictions = pneumonia_model.predict(processed_image)
        predicted_class = (predictions > 0.5).astype("int32")

        class_names = ["Normal", "Pneumonia"]
        result = class_names[predicted_class[0][0]]
        return jsonify({"prediction": result})

    except Exception as e:
        print(f"Error during pneumonia prediction: {str(e)}")
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500


@app.route("/predict/tumor", methods=["POST"])
def predict_tumor():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image = Image.open(io.BytesIO(file.read()))
        processed_image = preprocess_image(image, target_size=(128, 128))  # Ensure size matches tumor model

        predictions = tumor_model.predict(processed_image)
        predicted_class = (predictions > 0.5).astype("int32")

        class_names = ["No Tumor", "Tumor"]
        result = class_names[predicted_class[0][0]]
        return jsonify({"prediction": result})

    except Exception as e:
        print(f"Error during tumor prediction: {str(e)}")
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
