import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Load and preprocess MNIST dataset
# -------------------------------------------------
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Normalize
train_images = train_images / 255.0
test_images = test_images / 255.0

# Flatten images to 784-dim vectors
train_images = train_images.reshape((60000, 28 * 28))
test_images = test_images.reshape((10000, 28 * 28))

# One-hot encode labels
train_labels = tf.keras.utils.to_categorical(train_labels)
test_labels = tf.keras.utils.to_categorical(test_labels)

# -------------------------------------------------
# Build MLP model
# -------------------------------------------------
model = models.Sequential([
    layers.Dense(128, activation='relu', input_shape=(784,)),
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')
])

# Compile
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# -------------------------------------------------
# Train
# -------------------------------------------------
model.fit(
    train_images, train_labels,
    epochs=5,
    batch_size=64,
    validation_split=0.2
)

# -------------------------------------------------
# Evaluate
# -------------------------------------------------
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"Test Accuracy: {test_acc:.4f}")

# -------------------------------------------------
# Predictions
# -------------------------------------------------
num_samples = 5
sample_indices = np.random.choice(test_images.shape[0], num_samples, replace=False)
samples_to_predict = test_images[sample_indices]

predictions = model.predict(samples_to_predict)

# -------------------------------------------------
# Display predictions with images
# -------------------------------------------------
plt.figure(figsize=(12, 3))
for i in range(num_samples):
    predicted_label = np.argmax(predictions[i])
    true_label = np.argmax(test_labels[sample_indices[i]])

    img = samples_to_predict[i].reshape(28, 28)

    plt.subplot(1, num_samples, i + 1)
    plt.imshow(img, cmap='gray')
    plt.title(f"T: {true_label}\nP: {predicted_label}")
    plt.axis("off")

plt.show()
