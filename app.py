import streamlit as st
import joblib
import json
import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.models import load_model, save_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np

import h5py

with h5py.File('best_model.h5', 'r') as file:
    print(file.attrs['keras_version'])  # Check Keras version
    print(file.attrs['backend'])  # Check backend

# Load the trained model and tokenizer
@st.cache_resource
def load_resources():
    model = tf.keras.models.load_model('best_model.h5')
    tokenizer = joblib.load('tokenizer.joblib')
    print(tokenizer)
    return model, tokenizer


model, tokenizer = load_resources()

# Define constants
MAX_SEQUENCE_LENGTH = 30

# Title
st.title("Sarcasm Detection Model")

# Input form
input_text = st.text_input("Enter a sentence to check for sarcasm:", "")

if st.button("Predict"):
    if input_text.strip():
        # Preprocess the input text
        sequences = tokenizer.texts_to_sequences([input_text])
        padded_seq = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
        
        # Predict using the model
        prediction = model.predict(padded_seq)[0][0]
        
        
        # Output prediction
        st.subheader("Prediction:")
        if prediction > 0.5:
            st.write(f"**Sarcastic** with a probability of {prediction:.2f}")
        else:
            st.write(f"**Not Sarcastic** with a probability of {1 - prediction:.2f}")
    else:
        st.warning("Please enter a valid sentence.")

st.markdown("This app uses an LSTM model trained on sarcasm detection data.")