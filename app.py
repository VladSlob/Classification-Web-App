import os

import tensorflow as tf
from flask import Flask, request, render_template
from classifier import classify


app = Flask(__name__, template_folder="templates")

STATIC_FOLDER = "static"
UPLOAD_FOLDER = "static/images"

cnn_model = tf.keras.models.load_model(
    STATIC_FOLDER + "/models/" + "tires_model_light.keras"
)


def save_uploaded_file(file) -> str:
    uploaded_img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(uploaded_img_path)
    return uploaded_img_path


def determine_result_classes(label: str) -> tuple[str, str]:
    background_class = "road-bg"
    message_class = ""

    if "flat" in label.lower():
        background_class = "flat-tire-bg"
        message_class = "advice-message--danger"

    elif "OK" in label:
        background_class = "ok-tire-bg"
        message_class = "advice-message--success"

    return background_class, message_class


def prepare_response(
    message: str, probability: float, background_class: str, message_class: str
) -> str:
    return render_template(
        "result.html",
        message=message,
        probability=probability,
        background_class=background_class,
        message_class=message_class,
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/classify")
def classify_image():
    file = request.files["image"]
    uploaded_img_path = save_uploaded_file(file)
    label, message, prob = classify(cnn_model, uploaded_img_path)
    probability = round(prob * 100, 0)

    background_class, message_class = determine_result_classes(label)

    return prepare_response(message, probability, background_class, message_class)


if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
