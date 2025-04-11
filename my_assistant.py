import pvporcupine
import pyaudio
import numpy as np
import wave
import os
import time
import sounddevice as sd
import webrtcvad  
import whisper  
import pyttsx3  
import google.generativeai as genai 
import atexit
import signal
import sys
from dotenv import load_dotenv

load_dotenv()  

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ACCESS_KEY = os.getenv("ACCESS_KEY")
WAKE_WORD_PATH = os.getenv("WAKE_WORD_PATH")

stop_speaking = False


ASSISTANT_RULES = """
You are an AI assistant. Follow these rules at all times:
1. Always be polite and respectful.
2. Never give harmful or misleading information.
3. Do not respond with asterisks or special formatting.
4. If you don't know something, say 'I'm not sure' instead of guessing.
"""






# Initialize Porcupine for wake word detection
porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[WAKE_WORD_PATH])

SHUTDOWN_COMMANDS = {"shut down", "exit", "stop listening", "quit", "turn off","bye","please shut down","goodbye"}

def cleanup():
    # Ensure Porcupine resources are freed before exit.
    print("Cleaning up resources...")
    porcupine.delete()
    print("Porcupine deleted.")

# Register cleanup function 
atexit.register(cleanup)

def handle_exit(signum, frame):
    print(f"Received signal {signum}. Exiting gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)  #
signal.signal(signal.SIGTERM, handle_exit)

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=512)

vad = webrtcvad.Vad(2)
engine = pyttsx3.init()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')  

def is_speech(frame):
    return vad.is_speech(frame, 16000)

def record_audio(filename="command.wav"):
    print("Recording... Speak now!")
    buffer = []
    last_speech_time = time.time()

    with sd.InputStream(samplerate=16000, channels=1, dtype=np.int16) as stream:
        while True:
            audio_chunk, _ = stream.read(320)
            buffer.append(audio_chunk)

            if is_speech(audio_chunk):
                last_speech_time = time.time()

            if time.time() - last_speech_time > 1.5:
                print("Silence detected. Stopping recording.")
                break

    audio_data = np.concatenate(buffer, axis=0)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio_data.tobytes())

    print(f"Recording saved as {filename}")
    return filename

def transcribe_audio(filename="command.wav"):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"].strip()

def get_response(prompt):
    if not prompt:
        return "Sorry, I didn't hear what you were saying."
    try:
        full_prompt = f"{ASSISTANT_RULES}\nUser: {prompt}\nAssistant:"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response with Gemini: {e}")
        return "Sorry, I encountered an error."

def speak(text):
    engine.setProperty('rate', 175) 
    engine.say(text)
    engine.runAndWait()

def wake_word_loop():
    print("Listening for wake word...")

    try:
        while True:
            pcm = stream.read(512)
            pcm = np.frombuffer(pcm, dtype=np.int16)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Wake word detected! Activating assistant...")

                filename = record_audio()
                query = transcribe_audio(filename).lower()

                if not query:
                    print("No speech detected.")
                    response = "Sorry, I didn't hear what you were saying."
                elif any(cmd in query for cmd in SHUTDOWN_COMMANDS):
                    print("Shutdown command detected. Exiting...")
                    speak("Goodbye!")
                    cleanup()
                    sys.exit(0)
                else:
                    print("You said:", query)
                    response = get_response(query)

                print("Assistant:", response)
                speak(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup()  

if __name__ == "__main__":
    wake_word_loop()