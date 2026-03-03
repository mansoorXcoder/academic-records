import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
import matplotlib.pyplot as plt

# Load training dataset
train_data = keras.utils.image_dataset_from_directory(
    directory=r"D:\LE03\DL\Exp6\Dataset\train",
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256, 256)
)

# Load validation dataset
validation_data = keras.utils.image_dataset_from_directory(
    directory=r"D:\LE03\DL\Exp6\Dataset\test",
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256, 256)
)

# Normalize image data
def process(image, label):
    image = tf.cast(image / 255.0, tf.float32)
    return image, label

train_data = train_data.map(process)
validation_data = validation_data.map(process)

# CNN Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.summary()

# Compile model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train model (fit_generator is deprecated → use fit)
epochs = 5

history = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=epochs,
    verbose=1
)

# Plot accuracy
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.show()
