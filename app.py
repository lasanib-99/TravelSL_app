import streamlit as st
from tourism_chatbot import get_full_response

st.set_page_config(page_title = "Travel SL - Chatbot", layout = "wide")

st.title("Tourism Chatbot for Sri Lanka")

st.write("Ask me anything about travelling in Sri Lanka!")

# Input form for the user's question
user_input = st.text_input("Your Question:", placeholder = "Ex: What are the best beaches in Sri Lanka?")

# Button to submit the question
if st.button("Ask"):

    if user_input.strip():  # Check if the input is not empty

        # Get the chatbot response based on user input
        response = get_full_response(user_input)

        # Display the response in a text area with a fixed height of 400px
        st.text_area("Response:", value = response, height = 150)

    else:
        st.write("Please enter a valid question.")
