import numpy as np
import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt

# --------------------------------------------------
# Set random seeds
# --------------------------------------------------
np.random.seed(0xdeadbeef)
tf.random.set_seed(0xdeadbeef)

# --------------------------------------------------
# Load IMDB dataset
# --------------------------------------------------
num_words = 20000
(train_data, train_labels), (test_data, test_labels) = keras.datasets.imdb.load_data(
    num_words=num_words
)

# --------------------------------------------------
# Prepare vocabulary
# --------------------------------------------------
vocabulary = keras.datasets.imdb.get_word_index()
vocabulary = {k: (v + 3) for k, v in vocabulary.items()}

vocabulary["<PAD>"] = 0
vocabulary["<START>"] = 1
vocabulary["<UNK>"] = 2
vocabulary["<UNUSED>"] = 3

index = {v: k for k, v in vocabulary.items()}

def decode_review(text):
    return ' '.join([index.get(i, '?') for i in text])

# --------------------------------------------------
# Pad sequences
# --------------------------------------------------
maxlen = 256
train_data = keras.preprocessing.sequence.pad_sequences(
    train_data, value=vocabulary["<PAD>"], padding='post', maxlen=maxlen
)
test_data = keras.preprocessing.sequence.pad_sequences(
    test_data, value=vocabulary["<PAD>"], padding='post', maxlen=maxlen
)

# --------------------------------------------------
# Build model
# --------------------------------------------------
model = keras.Sequential([
    keras.layers.Embedding(len(vocabulary), 2, input_length=maxlen),
    keras.layers.Flatten(),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(5, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# --------------------------------------------------
# Train model
# --------------------------------------------------
history = model.fit(
    train_data,
    train_labels,
    epochs=5,
    batch_size=100,
    validation_data=(test_data, test_labels),
    verbose=1
)

# --------------------------------------------------
# Plot accuracy
# --------------------------------------------------
def plot_accuracy(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    epochs = range(len(acc))

    plt.plot(epochs, acc, label='Train')
    plt.plot(epochs, val_acc, label='Test')
    plt.title('Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

plot_accuracy(history)

# --------------------------------------------------
# 🔥 FIXED PART: Word Embedding Visualization
# --------------------------------------------------

# Create embedding extractor model (NEW TF WAY)
embedding_model = keras.Model(
    inputs=model.inputs,
    outputs=model.layers[0].output
)

review = ['great', 'brilliant', 'crap', 'bad', 'fantastic', 'movie', 'seagal']
enc_review = tf.constant([[vocabulary[word]] for word in review])

words = embedding_model(enc_review).numpy().squeeze()

plt.scatter(words[:, 0], words[:, 1])
for i, txt in enumerate(review):
    plt.annotate(txt, (words[i, 0], words[i, 1]))

plt.title("Word Embeddings")
plt.show()
