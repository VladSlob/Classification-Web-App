import tensorflow as tf

IMAGE_SIZE = (180, 180)


def preprocess_image(image):
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)

    return img_array


def load_and_preprocess_image(path: str):
    image = tf.keras.preprocessing.image.load_img(
        path, target_size=IMAGE_SIZE
    )

    return preprocess_image(image)


def classify(model, image_path: str):
    preprocessed_image = load_and_preprocess_image(image_path)

    prediction = model.predict(preprocessed_image)
    score = prediction[0]

    label = "cat" if score <= 0.5 else "dog"
    prob = 1 - score if label == "cat" else score

    return label, prob
