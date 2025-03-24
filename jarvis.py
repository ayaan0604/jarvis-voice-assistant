import speech_recognition as sr
import pyttsx3
import pywhatkit
from datetime import datetime
import os
import webbrowser
import threading
from keywords import *
import pyjokes

webbrowser.register("brave",None,webbrowser.BackgroundBrowser(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"))

is_listening=False      #flag for listening

voice=pyttsx3.init()
voice.setProperty("rate",200)

def speak(output):
    print(f"Jarvis: {output}")
    voice.say(output)
    voice.runAndWait()
    
def searchOnYoutube(command,keyword):
    if "search" in command:
        query=command.replace("search","")
        query=query.replace(keyword,"")

    
    else:   
        query= command.replace(keyword,"")
    
    speak(f"Okay. Searching for {query} on youtube")
    query=query.replace(" ","+")
    url=f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)

def play_song(command):
    query=command.replace("play","")
    speak(f"Alright, playing {query} on youtube")
    try:
        pywhatkit.playonyt(query)
    except Exception as e:
        print(e)

def getJoke():
    joke=pyjokes.get_joke()
    speak(joke)



def take_command():
    global is_listening
    is_listening=True
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        recognizer.pause_threshold=2
        
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source)
        

    try:
        print("recognizing audio...")
        command=recognizer.recognize_google(audio,language="en-in")
        print(f"User: {command}")

    except sr.UnknownValueError:
        print("no command found")
        return "none"
    
    except sr.RequestError:
        print("Insternet connection seems low. Please check the connection")
        return "none"
    
    finally:
        is_listening=False
    
    return command.lower()

def process_command(command):

    if "hello" in command:
        speak('Hi there! I am jarvis. What can i do for you?')

    youtubeSearch=False
    if "youtube" in command:
        for keyword in youtube_keywords:
            if keyword in command:
                youtubeSearch=True

                searchOnYoutube(command,keyword)

    

    if "search" in command and not youtubeSearch:
        query=command.replace("search","").strip()
        speak(f"Searching for {query} on google")
        pywhatkit.search(query)

    if "open brave" in command or "open browser" in command or "browser" in command:
        speak("Alright, opening brave")
        webbrowser.get("brave").open()

    if "open youtube" in command:
        speak("Alright, opening youtube")
        webbrowser.open("https://www.youtube.com")

    if "repeat after me" in command:
        query=command.replace("repeat after me","")
        speak(query)

    for keyword in date_keywords:
        if keyword in command:
            info=datetime.now()
            current_date=f"today is {info.day} of {months[info.month]} , {info.year}"
            speak(current_date)
            break

    
    for keyword in time_keywords:
        if keyword in command:
             info=datetime.now()
             time=f"the current time is {info.hour} hours {info.minute} minutes and {info.second} seconds"
             speak(time)
             break
        
    if "play" in command:
        play_song(command)


    for keyword in joke_keywords:
        if keyword in command:
            getJoke()
            break

    if "bye" in command:
        speak("Goodbye")
        exit()

    
def on_release(event):
    if event.name=="0":
        command=take_command()
        if command and command!='none':
            process_command(command)

def on_release(event):
    global is_listening
    if event.name == "0" and not is_listening:  # Prevents multiple triggers
        threading.Thread(target=listen_and_process, daemon=True).start()

def listen_and_process():
    command = take_command()
    if command and command != "none":
        process_command(command)

if __name__=="__main__":
    while True:
        command=take_command()
        process_command(command)
    



#print("Press 0 to talk")
#keyboard.on_release(on_release)
#keyboard.wait("esc")


#current issue- not able to execute the commands
#no feature to stop listening forcefully