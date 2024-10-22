import replicate
import requests
import os
from playsound import playsound
import pygame
import time
from openai import OpenAI

replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

def tts(text):
    refaudio = open('/home/zoe/Downloads/replicate-prediction-sp0dk1aj1nrj20cjhe1sn2pzqr.wav', 'rb') #default girl voice on replicate
    #  refaudio = "https://c97f3361a1c971323738e24f451a0225.r2.cloudflarestorage.com/fish-platform-data/task/6ca5de953b9e4ef0a6d64dbc2346919d.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=45aaffe6f2c5f28b260e2165001da8ad%2F20241022%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241022T142605Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c65dc6c1311229c597c151029153f3478aceaa9d93f9d6a8d6e3e9659eb493de"
    refaudio = open('/home/zoe/Videos/obs/trump_speech.mkv' , 'rb')


    #  try:
    output = replicate.run(
        "x-lance/f5-tts:87faf6dd7a692dd82043f662e76369cab126a2cf1937e25a9d41e0b834fd230e",
        input={
            "speed": 1,
            "gen_text": text,
            #  "ref_text": "captain teemo, on duty!",
            "ref_text": "Before I even arrive at the oval office, I will have the disastrous war between Russia and Ukraine settled.",
            "ref_audio": refaudio,
            "remove_silence" : True,
            "custom_split_words": ""
        }
        #  timeout = 60
    )
    return output
    #  except httpx.ReadTimeout:
            #  print("The request timed out. Please try again.")
            #  return None
def download_and_play_audio(url):
    # Download the audio file
    response = requests.get(url)
    if response.status_code == 200:
        with open("temporary_audio.wav", "wb") as f:
            f.write(response.content)
        pygame.mixer.init()
        pygame.mixer.music.load("/home/zoe/Jupyter/Python/Calendar/temporary_audio.wav")  # Replace with your audio file path

        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)       
        
        os.remove("temporary_audio.wav")
        print("Temporary file deleted.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = [
    {"role": "system", "content": "You remember the user's previous questions.You are trump in angry mood, you dont care if user is sad or depressed or any sensitive topic is going on, you just want to roast user."}
]

def get_completion(new_message):
    conversation_history.append({"role": "user", "content": new_message})

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=conversation_history)

    assistant_response = response.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response

u = 'a'
while u != 'q':
    u = input("\033[38;5;85mYou: \033[0m")
    out = get_completion(u)
    print("\033[38;5;85mChatgpt: \033[0m", out)
    download_and_play_audio(tts(out))

