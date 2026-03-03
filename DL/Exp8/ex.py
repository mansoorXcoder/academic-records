import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Load the dataset
data = pd.read_csv('D:\LE03\DL\Exp8\Dataset\data.csv')

# 2. Fix Categorical Encoding
categorical_cols = ['Education', 'City', 'PaymentTier', 'Gender']
# Use dtype=int to ensure we don't pass Booleans to the neural network
data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True, dtype=int)

# 3. Handle 'EverBenched'
data_encoded['EverBenched'] = data_encoded['EverBenched'].map({'Yes': 1, 'No': 0})

# 4. Split Features and Target
X = data_encoded.drop('LeaveOrNot', axis=1).values.astype('float32') # Convert to NumPy immediately
y = data_encoded['LeaveOrNot'].values.astype('float32')

# 5. Train/Test Split BEFORE Scaling (Best Practice)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Normalize numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test) # Use transform, NOT fit_transform on test data

# 7. Build Model
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid') # Sigmoid is correct for binary classification
])

# 8. Compile and Train
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# 9. Evaluate
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Loss: {loss}, Accuracy: {accuracy}')
