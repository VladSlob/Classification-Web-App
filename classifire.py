from typing import Any

import tensorflow as tf

IMAGE_SIZE = (256, 256)
THRESHOLD = 0.5


def preprocess_image(image) -> Any:
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, axis=0)

    return img_array


def load_and_preprocess_image(path: str) -> Any:
    image = tf.keras.preprocessing.image.load_img(path, target_size=IMAGE_SIZE)

    return preprocess_image(image)


def classify(model: Any, image_path: str) -> tuple[str, str, float]:
    preprocessed_image = load_and_preprocess_image(image_path)

    predictions = model.predict(preprocessed_image)
    score = predictions[0]

    message = "We cannot give you a good enough advice please use an air gauge"
    probability = -1
    label = "undefined"

    if score[0] > THRESHOLD:
        label = "flat"
        message = "The tire is flat. Please don't drive before fixing it"
        probability = score[0]
    if score[1] > THRESHOLD:
        label = "OK"
        message = "The tire is OK, you can drive safely"
        probability = score[1]
    if score[2] > THRESHOLD:
        message = "The tire was not detected on the image"
        probability = score[2]

    return label, message, probability
