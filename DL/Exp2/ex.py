# ====== Imports ======
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ====== Parameters ======
max_features = 10000
maxlen = 100
batch_size = 32  
epochs = 10

# ====== Load & Preprocess Data ======
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=max_features)

train_data = pad_sequences(train_data, maxlen=maxlen)
test_data = pad_sequences(test_data, maxlen=maxlen)

# ====== Model Definition ======
model = Sequential([
    Embedding(max_features, 8, input_length=maxlen),
    Flatten(),
    Dense(1, activation='sigmoid')
])

# ====== Compile Model ======
model.compile(
    optimizer='rmsprop',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ====== Train Model ======
model.fit(
    train_data,
    train_labels,
    epochs=epochs,
    batch_size=batch_size,
    validation_split=0.2
)

# ====== Evaluate Model ======
test_loss, test_acc = model.evaluate(test_data, test_labels)
print(f"Test Accuracy: {test_acc * 100:.2f}%")

# ====== Word Index ======
word_index = imdb.get_word_index()

# ====== Prediction Function ======
def predict_sentiment(review, word_index, model, maxlen):
    tokens = pad_sequences(
        [[word_index.get(word, 0) for word in review.lower().split()]],
        maxlen=maxlen
    )
    prediction = model.predict(tokens)
    return prediction[0][0]

# ====== Sample Predictions ======
positive_review = "This movie was fantastic! The acting and plot were amazing."
negative_review = "I hated this movie. The acting was terrible and the plot made no sense."

print("Positive Review Prediction:", predict_sentiment(positive_review, word_index, model, maxlen))
print("Negative Review Prediction:", predict_sentiment(negative_review, word_index, model, maxlen))
