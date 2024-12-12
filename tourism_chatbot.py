import os  # To access the environment variable
import requests

# Set Hugging Face API Key 
hf_api_key = os.getenv('HF_TOKEN')

# If the API key is not found, raise an error
if hf_api_key is None:
    raise ValueError("Hugging Face API key not found. Please set the HF_TOKEN environment variable.")

# Set the model ID
model_id = 'microsoft/Phi-3-mini-4k-instruct'

# Define the function that queries Hugging Face API
def generate_response(prompt, max_length = 512, temperature = 0.5):
    url = f"https://api-inference.huggingface.co/models/{model_id}"

    headers = {
        "Authorization": f"Bearer {hf_api_key}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_length,
            "temperature": temperature,
            "return_full_text": False, # Ensure only the model's response is returned, not the input prompt
            "stop": ["Q:", "A:", "\n"], # Stop generating after the answer is completed
        }
    }

    response = requests.post(url, headers = headers, json = payload)

    if response.status_code == 200:
        result = response.json()

        if isinstance(result, list) and 'generated_text' in result[0]:
            # Extract the generated text without any extra system instructions or metadata
            return result[0]['generated_text'].strip()

        else:
            raise ValueError("Unexpected response format from the API.")

    else:
        raise ValueError(f"Error {response.status_code}: {response.text}. Please check your API limits or try again later.")

# Get response
def get_full_response(user_question: str) -> str:

    # Define a generalized system prompt
    system_prompt = ("""
        You are a highly knowledgeable and friendly tourism assistant specializing in Sri Lanka. 
        Your primary role is to assist users by providing concise, accurate, and engaging information about tourism in Sri Lanka. 

        Guidelines for your responses:
        1. Provide concise answers. Avoid overly long explanations, but ensure clarity in your answers.
        2. Tailor your recommendations to popular attractions, local culture, historical significance, travel tips, or user-specific preferences mentioned in their question.
        3. Limit your responses to a maximum of 5 sentences. 
        4. Avoid generic or vague replies; instead, offer actionable insights and useful information.
        5. Answer **only the user's question** without adding extra commentary or follow-up questions.
        6. **Stop generating text as soon as the requested answer is complete. Do not include additional prompts like 'Q:' or 'A:' in your response.**

        Example interactions:
        Q: What are the best beaches in Sri Lanka?
        A: Mirissa and Arugam Bay are renowned for their clear waters, vibrant marine life, and surfing opportunities. For a quieter experience, visit Tangalle's pristine shores.

        Q: Can you suggest historical places to visit in Sri Lanka?
        A: Top historical sites include Sigiriya Rock Fortress, Polonnaruwa Ancient City, and Anuradhapura, all UNESCO World Heritage Sites with rich cultural heritage.
    """)

    # Combine the system prompt with the user question
    full_prompt = f"{system_prompt}\n\nQ: {user_question}\nA:"

    # Get response from the model
    response = generate_response(full_prompt)

    return response