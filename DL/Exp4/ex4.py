# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load dataset
data = pd.read_csv(r"D:\LE03\DL\Exp4\Dataset\data.csv")

# Separate features and target (UPDATED: medv is lowercase)
X = data.drop('medv', axis=1).values
y = data['medv'].values

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Define ANN model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dense(1)   # Output layer for regression
])

# Compile model
model.compile(
    optimizer='adam',
    loss='mean_squared_error'
)

# Train model
model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.1
)

# Evaluate model
test_loss = model.evaluate(X_test, y_test)
print("Test Loss:", test_loss)

# Predict house prices
y_pred = model.predict(X_test)

# Visualize results
plt.scatter(y_test, y_pred)
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Actual vs Predicted House Prices")
plt.show()
