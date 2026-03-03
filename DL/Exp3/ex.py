import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import reuters
from tensorflow.keras import models, layers
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# -------------------------------------------------
# 1. Load Reuters Dataset
# -------------------------------------------------
(train_data, train_labels), (test_data, test_labels) = reuters.load_data(num_words=10000)

# -------------------------------------------------
# 2. Vectorize Sequences
# -------------------------------------------------
def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

# -------------------------------------------------
# 3. One-hot Encode Labels
# -------------------------------------------------
y_train = to_categorical(train_labels)
y_test = to_categorical(test_labels)

# -------------------------------------------------
# 4. Validation Split
# -------------------------------------------------
x_val = x_train[:1000]
partial_x_train = x_train[1000:]

y_val = y_train[:1000]
partial_y_train = y_train[1000:]

# -------------------------------------------------
# 5. Build Model
# -------------------------------------------------
model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10000,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(46, activation='softmax')
])

model.compile(
    optimizer='rmsprop',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# -------------------------------------------------
# 6. Train Model
# -------------------------------------------------
history = model.fit(
    partial_x_train,
    partial_y_train,
    epochs=9,
    batch_size=512,
    validation_data=(x_val, y_val)
)

# -------------------------------------------------
# 7. Plot Training History
# -------------------------------------------------
def plot_history(history):
    epochs = range(1, len(history.history['accuracy']) + 1)

    plt.figure(figsize=(12, 5))

    # Loss
    plt.subplot(1, 2, 1)
    plt.plot(epochs, history.history['loss'], 'bo', label='Training loss')
    plt.plot(epochs, history.history['val_loss'], 'r', label='Validation loss')
    plt.title('Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    # Accuracy
    plt.subplot(1, 2, 2)
    plt.plot(epochs, history.history['accuracy'], 'bo', label='Training accuracy')
    plt.plot(epochs, history.history['val_accuracy'], 'r', label='Validation accuracy')
    plt.title('Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()

plot_history(history)

# -------------------------------------------------
# 8. Evaluate Model
# -------------------------------------------------
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

# -------------------------------------------------
# 9. Random Baseline Comparison
# -------------------------------------------------
shuffled_labels = test_labels.copy()
np.random.shuffle(shuffled_labels)
baseline_accuracy = np.mean(test_labels == shuffled_labels)
print(f"Random Baseline Accuracy: {baseline_accuracy}")

# -------------------------------------------------
# 10. Predictions
# -------------------------------------------------
predictions = model.predict(x_test)
