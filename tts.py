import replicate
import requests
import os
import time
from openai import OpenAI
from pydub import AudioSegment
import threading
import pygame
from pydub.playback import play
import httpx
replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
#  client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"), transport=httpx.AsyncHTTPTransport(verify=False))

def print_text_slowly(text, audio_duration):
    words = text.split()  # Split text into words
    time_per_word = audio_duration / len(words)  # Calculate time per word

    for word in words:
        print(word, end=' ', flush=True)  # Print each word with a space
        time.sleep(time_per_word)  # Wait for the calculated time

def play_audio(file):
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load(file)  # Load the audio file
    pygame.mixer.music.play()  # Play the audio



def playtts(text):

    #  refaudio = open('/home/zoe/Videos/obs/2024-10-22_23-41-59.mkv' , 'rb')
    refaudio = open('/home/zoe/Videos/obs/trump_speech_trimmed.mkv', 'rb')

    output = replicate.run(
        "x-lance/f5-tts:87faf6dd7a692dd82043f662e76369cab126a2cf1937e25a9d41e0b834fd230e",
        input={
            "speed": 1,
            "gen_text": text,
            #  "ref_text": "captain teemo, on duty!",
            "ref_text": "Before I even arrive at the oval office, I will have the disastrous war between Russia and Ukrain settled.",
            "ref_audio": refaudio,
        }
    )
    response = requests.get(output)
    if response.status_code == 200:
        with open("temporary_audio.wav", "wb") as f:
            f.write(response.content)
        play_audio("/home/zoe/Jupyter/Python/Calendar/temporary_audio.wav")
        print('\033[38;5;85mChatgpt: \033[0m', end = '')
        audio = AudioSegment.from_file("/home/zoe/Jupyter/Python/Calendar/temporary_audio.wav")
        audio_duration = len(audio)/1000
        print_text_slowly(text, audio_duration)
        print()
        print()
       
        os.remove("temporary_audio.wav")
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
    playtts(out)

