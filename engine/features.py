from engine.command import speak
from playsound import playsound
from engine.config import ASSISTANT_NAME
import os
import eel
import pywhatkit
import webbrowser
import sys

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\www_assets_audio_start_sound.mp3"
    playsound(music_dir)

@eel.expose
def openCommand(query):
    query = query.strip().lower()

    if query == f"hey {ASSISTANT_NAME.lower()}":
        speak("How can I help you?")
        return

    if "search for" in query:
        search_query = query.split("search for")[-1].strip()
        if search_query:
            if "facebook" in query:
                speak(f"Searching for {search_query} on Facebook")
                webbrowser.open(f"https://www.facebook.com/search/top?q={search_query.replace(' ', '+')}")
                return

            if "instagram" in query:
                speak(f"Searching for {search_query} on Instagram")
                webbrowser.open(f"https://www.instagram.com/explore/search/keyword/?q={search_query.replace(' ', '+')}")
                return

            if "youtube" in query:
                speak(f"Searching YouTube for {search_query}")
                pywhatkit.playonyt(search_query) 
                return

    if "facebook" in query:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
        return

    if "instagram" in query:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
        return

    if "youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return

    if query.startswith("open"):
        website_name = query.replace("open", "").strip().replace(" ", "")
        if website_name:
            speak(f"Opening {website_name}")
            webbrowser.open(f"https://www.{website_name}.com")
        else:
            speak("Website not found.")
        return

    speak("Website not found.")

def process_query(query):
    """Process the query and return a response."""
    print(f"Received Query: {query}")

    if "hello" in query.lower():
        return "Hello! How can I assist you?"
    elif "time" in query.lower():
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
    else:
        return f"Processed: {query}"
