# Abhishek's Assistant - Command Engine

import pyttsx3
import speech_recognition as sr
import eel
import threading
import re
import ctypes
from engine.gpt import ask_gpt

speech_done_event = threading.Event()
stop_requested = False
speak_thread = None 
def speak(text):
    global speak_thread

    def run():
        try:
            engine = pyttsx3.init('sapi5')
            engine.setProperty('rate', 150)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(" TTS error:", e)
        finally:
            speech_done_event.set()

    speech_done_event.clear()
    speak_thread = threading.Thread(target=run)
    speak_thread.start()

def stop_speaking_now():
    global speak_thread
    try:
        if speak_thread and speak_thread.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(speak_thread.ident),
                ctypes.py_object(SystemExit)
            )
            print(" Speech thread killed")
    except Exception as e:
        print(" Error stopping speech thread:", e)
    finally:
        speech_done_event.set()

# 👋 On load
@eel.expose
def welcome():
    speak("Welcome Abhishek, how can I help you today?")
    speech_done_event.wait()

# 🎧 Mic input
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        eel.DisplayMessage("Listening...")
        print("🎤 Listening...")

        r.pause_threshold = 0.8

        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=8)
            eel.DisplayMessage("Recognizing...")
            print(" Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(" You said:", query)
            return query.lower()
        except sr.WaitTimeoutError:
            eel.DisplayMessage("Timeout: No speech detected.")
            print(" Timeout")
        except sr.UnknownValueError:
            eel.DisplayMessage("Could not understand.")
            print(" Unknown input")
        except sr.RequestError as e:
            eel.DisplayMessage("Speech API error.")
            print(" Speech API error:", e)
        except Exception as e:
            eel.DisplayMessage("Mic error.")
            print(" Mic error:", e)

        return ""

@eel.expose
def startListening():
    global stop_requested
    stop_requested = False

    while not stop_requested:
        query = takecommand()
        if not query:
            continue

        if "thank you" in query:
            eel.DisplayConversation(query, "My pleasure.")
            speak("My pleasure.")
            speech_done_event.wait()
            eel.ShowHood()
            break

        elif "stop" in query:
            eel.DisplayConversation(query, "Stopping now.")
            speak("Alright, stopping now.")
            speech_done_event.wait()
            eel.ShowHood()
            break

        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
            eel.DisplayConversation(query, "Opening...")
            speak("Opening...")
            speech_done_event.wait()
            eel.ShowHood()
            break

        else:
            eel.DisplayConversation(query, "Thinking...")
            eel.DisplayMessage("Thinking...")

            try:
                response = ask_gpt(query)
            except Exception as e:
                print(" GPT error:", e)
                response = "An error occurred while connecting to Marte."

            response = re.sub(r'[^\w\s.,!?;:()\'\"-]', '', response)
            eel.DisplayConversation(query, response)
            speak(response)
            speech_done_event.wait()

@eel.expose
def stopSpeaking():
    global stop_requested
    stop_requested = True
    stop_speaking_now()
    eel.ShowHood()
