import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
newsapi = os.getenv("NEWS_API_KEY")


recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_gemini(command)

    
    genai.configure(api_key=API_KEY)

    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(command)
    return(response.text)


def processcommand(c):
    c = c.lower()
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musiclibrary.music.get(song)
        webbrowser.open(link)

    elif 'news' in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        data = r.json()
        print(data)
        
        if r.status_code == 200 and data['status'] == 'ok':
         articles = data.get("articles", [])[:5]
         
         for article in articles:
          speak(article['title'])  

    else:
        output = ask_gemini(c)       
        speak(output)

if __name__ == "__main__":   
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)

            word = recognizer.recognize_google(audio).lower()
            print("You said:", word)

            # Wake word detection
            if "Jarvis" in word:   # trigger word
                speak("Yes, I'm listening. What should I do?")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                processcommand(command)

        except sr.UnknownValueError:
            # Ignore if speech wasn’t clear
            pass
        except sr.RequestError as e:
            print("Speech recognition service error:", e)
        except Exception as e:
            print("Error:", e)
