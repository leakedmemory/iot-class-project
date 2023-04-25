import os
import random
import urllib
import tarfile
import shutil

import keras
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, Dense, MaxPooling2D, Input, Flatten
from tensorflow.keras.metrics import Precision, Recall
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from custom_objects import L1Dist

MODEL_PATH = "model.h5"

RESIZED_WIDTH = 105
RESIZED_HEIGHT = 105

EPOCHS = 50

CHECKPOINT_DIR = "training_checkpoints"
CHECKPOINT_PREFIX = os.path.join(CHECKPOINT_DIR, "ckpt")

EVALUATION_IMAGES_PATH = "evaluation_images"


def main():
    load_dotenv()

    custom_objects = {"L1Dist": L1Dist}

    locate_gpus_and_config_if_found()
    create_directories_if_needed()
    donwload_negatives_if_needed()

    preprocessed_data = preprocess_data()
    data_to_train, data_for_tests = take_data_sample(preprocessed_data)

    embedding = make_embedding()
    model = load_or_make_model(custom_objects, embedding)
    optimizer = keras.optimizers.Adam(1e-4)

    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    checkpoint = tf.train.Checkpoint(opt=optimizer, model=model)

    train_data(data_to_train, model, optimizer, checkpoint)
    evaluate_model(model, data_for_tests, save_evaluation_imgs=False)
    save_model(model, custom_objects, optimizer)


def locate_gpus_and_config_if_found():
    gpus = tf.config.experimental.list_physical_devices("GPU")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)


def create_directories_if_needed():
    anc_path = os.getenv("ANC_PATH")
    pos_path = os.getenv("POS_PATH")
    neg_path = os.getenv("NEG_PATH")

    if not (os.path.isdir(anc_path) and os.path.isdir(pos_path) and os.path.isdir(neg_path)):
        print("\nSOME DATA STORAGE WAS NOT FOUND: creating missing directories...")
        os.makedirs(anc_path, exist_ok=True)
        os.makedirs(pos_path, exist_ok=True)
        os.makedirs(neg_path, exist_ok=True)
    else:
        print("\nDATA STORAGE FOUND: skipping directories creation...")


def donwload_negatives_if_needed():
    if len(os.listdir(os.getenv("NEG_PATH"))) > 0:
        print("\nNEGATIVE DATASET FOUND: loading it...")
        return

    print("\nNEGATIVE DATASET NOT FOUND: starting download...")
    ds_compressed_path = "lfw.tgz"
    ds_directory_path = "lfw"

    # download and extract Labelled Faces in the Wild dataset
    urllib.request.urlretrieve("http://vis-www.cs.umass.edu/lfw/lfw.tgz", ds_compressed_path)

    with tarfile.open(ds_compressed_path) as file:
        file.extractall()

    # move dataset images to the `NEG_PATH` directory
    for directory in os.listdir(ds_directory_path):
        for file in os.listdir(os.path.join(ds_directory_path, directory)):
            ex_path = os.path.join(ds_directory_path, directory, file)
            new_path = os.path.join(os.getenv("NEG_PATH"), file)
            os.replace(ex_path, new_path)

    # remove dataset compressed file and directory
    shutil.rmtree(ds_directory_path)
    os.remove(ds_compressed_path)


def load_or_make_model(custom_objects, embedding):
    if os.path.isfile(MODEL_PATH):
        print("\nMODEL FOUND: loading it...")
        return load_model(custom_objects)

    print("\nMODEL NOT FOUND: making a new one...")
    input_image = Input(name="input_image", shape=(RESIZED_HEIGHT, RESIZED_WIDTH, 3))
    validation_image = Input(name="validation_image", shape=(RESIZED_HEIGHT, RESIZED_WIDTH, 3))

    layer = L1Dist()
    layer._name = "distance"
    distances = layer(embedding(input_image), embedding(validation_image))

    classifier = Dense(1, activation="sigmoid")(distances)

    return Model(inputs=[input_image, validation_image], outputs=classifier, name="SiameseNetwork")


def load_model(custom_objects=None):
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects
    )

    return model


def make_embedding():
    filters = 64
    inp = Input(shape=(RESIZED_HEIGHT, RESIZED_WIDTH, 3), name="input_image")

    convolution1 = Conv2D(filters, (10, 10), activation="relu")(inp)
    max_pooling1 = MaxPooling2D(filters, (2, 2), padding="same")(convolution1)

    convolution2 = Conv2D(filters * 2, (7, 7), activation="relu")(max_pooling1)
    max_pooling2 = MaxPooling2D(filters, (2, 2), padding="same")(convolution2)

    convolution3 = Conv2D(filters * 2, (4, 4), activation="relu")(max_pooling2)
    max_pooling3 = MaxPooling2D(filters, (2, 2), padding="same")(convolution3)

    convolution4 = Conv2D(filters * 4, (4, 4), activation="relu")(max_pooling3)
    flatten1 = Flatten()(convolution4)
    dense1 = Dense(4096, activation="sigmoid")(flatten1)

    return Model(inputs=[inp], outputs=[dense1], name="embedding")


def preprocess_data():
    print("\nPreprocessing data...")
    anchor = tf.data.Dataset.list_files(os.path.join(os.getenv("ANC_PATH"), "*.jpg")).take(400)
    positive = tf.data.Dataset.list_files(os.path.join(os.getenv("POS_PATH"), "*.jpg")).take(400)
    negative = tf.data.Dataset.list_files(os.path.join(os.getenv("NEG_PATH"), "*.jpg")).take(400)

    positives = tf.data.Dataset.zip((anchor, positive, tf.data.Dataset.from_tensor_slices(tf.ones(len(anchor)))))
    negatives = tf.data.Dataset.zip((anchor, negative, tf.data.Dataset.from_tensor_slices(tf.zeros(len(anchor)))))
    data = positives.concatenate(negatives)

    data = data.map(preprocess)
    data = data.cache()
    data = data.shuffle(buffer_size=1024)

    return data


def preprocess(input_image, validation_image, label):
    return (preprocess_aux(input_image), preprocess_aux(validation_image), label)


def preprocess_aux(file_path):
    byte_image = tf.io.read_file(file_path)
    image = tf.io.decode_jpeg(byte_image)
    image = tf.image.resize(image, (RESIZED_HEIGHT, RESIZED_WIDTH))
    image = image / 255.0

    return image


def take_data_sample(data, percentage_taken=0.7):
    percentage_not_taken = 1.0 - percentage_taken

    train_data = data.take(round(len(data) * percentage_taken))
    train_data = train_data.batch(16)
    train_data = train_data.prefetch(8)

    test_data = data.skip(round(len(data) * percentage_taken))
    test_data = test_data.take(round(len(data) * percentage_not_taken))
    test_data = test_data.batch(16)
    test_data = test_data.prefetch(8)

    return train_data, test_data


def train_data(data, model, optimizer, checkpoint):
    print("\nStarting data training...")
    for epoch in range(1, EPOCHS+1):
        print(f"\nEpoch {epoch}/{EPOCHS}")
        progbar = tf.keras.utils.Progbar(len(data))

        for idx, batch in enumerate(data):
            train_step(model, batch, optimizer)
            progbar.update(idx+1)

        if epoch % 10 == 0:
            checkpoint.save(file_prefix=CHECKPOINT_PREFIX)


@tf.function
def train_step(model, batch, opt):
    binary_cross_loss = tf.losses.BinaryCrossentropy()

    with tf.GradientTape() as tape:
        images = batch[:2]
        label = batch[2]

        yhat = model(images, training=True)
        loss = binary_cross_loss(label, yhat)

        # calculate gradients
        grad = tape.gradient(loss, model.trainable_variables)
        # calculate updated weights and apply to model
        opt.apply_gradients(zip(grad, model.trainable_variables))


def evaluate_model(model, test_data, save_evaluation_imgs=False):
    print("\nEvaluating model...")
    for i, (test_input, test_val, y_true) in enumerate(test_data.as_numpy_iterator()):
        batch = f"{i + 1:03d}"
        y_hat = model.predict([test_input, test_val])
        filtered_y_hat = [1 if prediction > 0.5 else 0 for prediction in y_hat]
        print(f"Batch: {batch}")
        print(f"Prediction: {filtered_y_hat}")

        mp = Precision()
        mp.update_state(y_true, y_hat)
        print(f"Precision: {mp.result().numpy()}")

        mr = Recall()
        mr.update_state(y_true, y_hat)
        print(f"Recall: {mr.result().numpy()}\n")

        if save_evaluation_imgs:
            batch_dir = os.path.join(EVALUATION_IMAGES_PATH, f"batch{batch}")
            os.makedirs(batch_dir, exist_ok=True)

            for j in range(len(test_input)):
                plt.figure(figsize=(16, 8))
                plt.subplot(1, 2, 1)
                plt.imshow(test_input[j])
                plt.subplot(1, 2, 2)
                plt.imshow(test_val[j])
                plt.savefig(os.path.join(batch_dir, f"prediction{j+1:03d}_result{filtered_y_hat[j]:03d}.jpg"))
                plt.close()


def save_model(model, custom_objects, optimizer):
    print("\nSaving model...")
    config = model.get_config()
    with keras.utils.custom_object_scope(custom_objects):
        custom_model = keras.Model.from_config(config)

        custom_model.compile(
            optimizer=optimizer,
            loss="binary_crossentropy",
            metrics=[keras.metrics.Precision(), keras.metrics.Recall()]
        )

        custom_model.save(MODEL_PATH)


if __name__ == "__main__":
    main()
