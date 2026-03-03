# ===============================
# Import Required Libraries
# ===============================
from keras.models import Sequential
from keras.layers import Embedding, Dense, SimpleRNN
from keras.datasets import imdb
from keras.preprocessing import sequence
import matplotlib.pyplot as plt


# ===============================
# Dataset Configuration
# ===============================
max_word_range = 10000     # Vocabulary size
max_word_amount = 500     # Maximum review length


# ===============================
# Load IMDB Dataset
# ===============================
(input_train, output_train), (input_test, output_test) = imdb.load_data(
    num_words=max_word_range
)

print(len(input_train), "train sequences")
print(len(input_test), "test sequences")


# ===============================
# Padding Sequences
# ===============================
input_train = sequence.pad_sequences(input_train, maxlen=max_word_amount)
input_test = sequence.pad_sequences(input_test, maxlen=max_word_amount)

print("input_train shape:", input_train.shape)
print("input_test shape:", input_test.shape)


# ===============================
# Build the RNN Model
# ===============================
model = Sequential([
    Embedding(max_word_range, 32, input_length=max_word_amount),
    SimpleRNN(32),
    Dense(1, activation='sigmoid')
])

model.summary()


# ===============================
# Compile the Model
# ===============================
model.compile(
    optimizer='rmsprop',
    loss='binary_crossentropy',
    metrics=['accuracy']
)


# ===============================
# Train the Model
# ===============================
history = model.fit(
    input_train,
    output_train,
    epochs=10,
    batch_size=128,
    validation_split=0.2
)


# ===============================
# Extract Training History
# ===============================
loss = history.history['loss']
acc = history.history['accuracy']
val_loss = history.history['val_loss']
val_acc = history.history['val_accuracy']

epochs = range(1, len(loss) + 1)


# ===============================
# Plot Loss and Accuracy
# ===============================
plt.figure(figsize=(12, 5))

# Loss
plt.subplot(1, 2, 1)
plt.plot(epochs, loss, 'bo', label='Training Loss')
plt.plot(epochs, val_loss, 'b', label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()

# Accuracy
plt.subplot(1, 2, 2)
plt.plot(epochs, acc, 'bo', label='Training Accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()

plt.show()


# ===============================
# Evaluate on Test Data
# ===============================
score = model.evaluate(input_test, output_test)
print("Test Loss:", score[0])
print("Test Accuracy:", score[1])


# ===============================
# Make Predictions
# ===============================
predictions = model.predict(input_test[:5])
true_labels = output_test[:5]

print("0 = Negative review, 1 = Positive review")

for i in range(len(predictions)):
    print(
        "Prediction:",
        int(round(predictions[i][0])),
        "| True Label:",
        true_labels[i]
    )
