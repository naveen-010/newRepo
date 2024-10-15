import os
from fish_audio_sdk import Session, TTSRequest

def speak_text(text: str, output_filename: str = "outputnew.mp3"):
    session = Session("e92f5a56dee44cc9b4cd40d67ce386a2")
        # Generate audio file
    with open(output_filename, "wb") as f:
        for chunk in session.tts(TTSRequest(
            reference_id="e58b0d7efca34eb38d5c4985e378abcb",
            text=text
        )):
            f.write(chunk)

    # Play the generated audio file

# Example usage
t = "Ha! I love the toddler analogy! Let’s get back on track. Do you want to add, edit, view, or remove an event? I'm here to help!"
speak_text(t, 'toddler.mp3') 
# playsound("outputnew.mp3")

