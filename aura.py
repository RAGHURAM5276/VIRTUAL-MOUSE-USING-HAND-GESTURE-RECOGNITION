import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import os
from os import listdir
from os.path import isfile, join
import app
from threading import Thread

# Initialize text-to-speech
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[0].id)

# Initialize recognizer
r = sr.Recognizer()

# Globals
today = date.today()
keyboard = Controller()
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status

def aura_chat():
    def reply(audio):
        """Respond via text-to-speech and chatbot interface."""
        app.ChatBot.addAppMsg(audio)
        print(audio)
        engine.say(audio)
        engine.runAndWait()

    def wish():
        """Greet the user based on the current time."""
        hour = datetime.datetime.now().hour
        if hour < 12:
            reply("Good Morning!")
        elif hour < 18:
            reply("Good Afternoon!")
        else:
            reply("Good Evening!")
        reply("I am Aura. How may I help you?")

    # Configure microphone and audio input
    def record_audio():
        """Capture audio and convert it to text."""
        with sr.Microphone() as source:
            print("Listening...")
            r.energy_threshold = 300
            r.pause_threshold = 0.8
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                voice_data = r.recognize_google(audio)
                print(f"Recognized: {voice_data}")
                return voice_data.lower()
            except sr.RequestError:
                reply("Sorry, my service is down. Please check your internet connection.")
            except sr.UnknownValueError:
                reply("I didn't catch that. Could you please repeat?")
            return ""

    # Command processing
    def respond(voice_data):
        global file_exp_status, files, is_awake, path

        if 'wake up' in voice_data and not is_awake:
            is_awake = True
            wish()
            return

        if not is_awake:
            return

        if 'hello' in voice_data:
            wish()
        elif 'what is your name' in voice_data:
            reply('My name is Aura!')
        elif 'date' in voice_data:
            reply(today.strftime("%B %d, %Y"))
        elif 'time' in voice_data:
            reply(datetime.datetime.now().strftime("%H:%M:%S"))
        elif 'search' in voice_data:
            query = voice_data.split('search', 1)[-1].strip()
            reply(f'Searching for {query}')
            url = f'https://google.com/search?q={query}'
            try:
                webbrowser.open(url)
                reply("Here's what I found.")
            except:
                reply("Please check your internet connection.")
        elif 'location' in voice_data:
            reply('Which place are you looking for?')
            location = record_audio()
            if location:
                reply(f"Locating {location}...")
                url = f'https://google.nl/maps/place/{location}/&amp;'
                try:
                    webbrowser.open(url)
                    reply("Here's the location.")
                except:
                    reply("Please check your internet connection.")
        elif 'bye' in voice_data:
            reply("Goodbye! Have a great day.")
            is_awake = False
        elif 'exit' in voice_data:
            reply("Exiting. Goodbye!")
            sys.exit()
        else:
            reply("I am not programmed to do that yet!")

    # Main loop
    t1 = Thread(target=app.ChatBot.start)
    t1.start()

    while not app.ChatBot.started:
        time.sleep(0.5)

    wish()
    while True:
        voice_data = app.ChatBot.popUserInput() if app.ChatBot.isUserInput() else record_audio()
        try:
            respond(voice_data)
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    aura_chat()
