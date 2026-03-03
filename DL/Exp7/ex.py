import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from PIL import Image

# Load pre-trained VGG16 model
model = VGG16(weights='imagenet')

# Function to preprocess the image for VGG16
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

# Function to make predictions
def predict(image_path):
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=3)[0]  # Get top 3 predictions
    
    print("\nTop Predictions:")
    for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
        print("{}. {}: {:.2f}%".format(i + 1, label, score * 100))
    
    # Display the image
    img = Image.open(image_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

# Allow user to select an image
if __name__ == "__main__":
    image_path = input("Enter the path of the image: ")
    predict(image_path)