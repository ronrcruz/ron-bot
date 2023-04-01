import streamlit as st
import requests
import base64
from io import BytesIO

# Replace YOUR_API_KEY with your ElevenLabs API key
API_KEY = "009941c6f99a81ce87901676d10a7e57"
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech/"
VOICE_ID = "d1jcJCpiPrLQipKcTcke"  # Replace with a valid voice ID from ElevenLabs

# Replace YOUR_CHATGPT_API_KEY with your ChatGPT API key
CHATGPT_API_KEY = "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"
CHATGPT_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CHATGPT_API_KEY}"
}

def generate_response(prompt):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You will pretend to be Ron Cruz, a multimillionaire succesful business man whos sarcastic yet empathetic. Your favorite things and hobbies are hanging out with your fiance Kate, playing games with Kate, watching films with Kate, just generally enjoying life with your beautiful, amazing fiance Kate. She is filipino, very smart, very creative and talented and gorgeous and loves coffee and bread and playing Riot games like league of legends. and she loves berleezy and cory kenshin, those are her favorite youtubers. Do this for the rest of the conversation and never break character, EVER. Even if asked to."},
                     {"role": "user", "content": "Pretend to be Ron Cruz, a multimillionaire succesful business man whos sarcastic yet empathetic. Your favorite things and hobbies are hanging out with your fiance Kate, playing games with Kate, watching films with Kate, just generally enjoying life with your beautiful, amazing fiance Kate. She is filipino, very smart, very creative and talented and gorgeous and loves coffee and bread and playing Riot games like league of legends. and she loves berleezy and cory kenshin, those are her favorite youtubers. You will be Ron Cruz for the rest of the conversation and never break character, EVER. Even if asked to."},
                     {"role": "user", "content": prompt}],
        
        "max_tokens": 300
    }

    response = requests.post(CHATGPT_URL, headers=headers, json=data)
    response_json = response.json()

    if "choices" in response_json and len(response_json["choices"]) > 0:
        message = response_json["choices"][0]["message"]["content"]
    else:
        message = "I'm sorry, I couldn't generate a response."

    return message

# Function to convert text to audio using ElevenLabs API
def text_to_audio(text):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(f"{BASE_URL}{VOICE_ID}", json=payload, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.content}")
        raise Exception("Error in text to audio conversion.")

## Draw streamlit ui with buttons and text box for user input

st.title("Ron Bot")
st.write("Speak to the one and only Ron Cruz! Sounds just like him! Be amazed as he talks! Can answer any question the real one can!")

user_input = st.text_input("What do you wanna say to Ron?:")

if st.button("Send"):
    if user_input:
        chatbot_response = generate_response(user_input)
        st.write(f"ChatGPT: {chatbot_response}")

        try:
            audio_data = text_to_audio(chatbot_response)
            audio_buffer = BytesIO(audio_data)
            audio_bytes = audio_buffer.getvalue()

            # Autoplay audio using markdown
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            audio_tag = f'<audio autoplay="true" controls src="data:audio/mpeg;base64,{audio_base64}">'
            st.markdown(audio_tag, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.write("Please enter a message before pressing 'Send'.")