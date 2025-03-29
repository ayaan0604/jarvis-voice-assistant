import speech_recognition as sr
import pyttsx3
import pywhatkit
from datetime import datetime
import webbrowser
from keywords import *
import pyjokes
from database import *
from news import get_news

#registering the webbrowser
webbrowser.register("brave",None,webbrowser.BackgroundBrowser(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"))

#initializing the database
initialize_db()


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

def process_todo_command(query):
    todo_executed=False
    for keyword in todo_keywords["add_todo"]:
        if keyword in query:
            todo=query.replace(keyword,"").strip()
            try:
                add_todo(todo)
                speak(f"Added task {todo} into the todo list successfully")
                todo_executed=True
            except Exception as e:
                print(e)
            
            break

    for keyword in todo_keywords["view_todo"]:
        if keyword in query:
            speak("Here is a list of all the pending todos")

            try:
                get_pending_todo()
                todo_executed=True
            except Exception as e:
                speak("some error occured")
                print(e)
            
            break

    for keyword in todo_keywords["done_todo"]:
        if keyword in query:
            speak("please enter the todo number from the list of todos\n")
            get_pending_todo()
            num=int(input("\nEnter todo number (enter 0 to cancel): "))

            if num == 0:
                print("request cancelled")
                todo_executed=True

            else:
                try:
                    mark_as_done(num)
                    speak("marked the todo as done")
                    todo_executed=True
                except Exception as e:
                    speak("please enter a valid number")
                    print(e)

            
            break

    for keyword in todo_keywords['delete_todo']:
        if keyword in query:
            speak("Do you really want to delete the todo list?")
            choice=input("Enter yes to confirm").lower()
            if choice=='yes':
                    
                try:
                    
                    delete_all_todo()
                    speak("deleted all tasks from the todo list")
                    
                except Exception as e:
                    speak("some error occured")
                    print(e)
                
                finally:
                    todo_executed=True


                break

            else:
                speak("cancelled deletion")
                
                break

            

    if "help" in query:
        speak("Here are the todo related commands")
        for help in todo_keywords['todo_help']:
            print(help)
            todo_executed=True

    if not todo_executed:
        speak("Say todo help for todo related commands")

def process_news_command():
    articles=get_news()
    speak("Okay, here are the top headlines from BBC News:")
    i=1
    for news in articles:
        speak(f'Headline number {i}: {news[0]}')
        print("Description:")
        speak(news[1])
        i+=1

        print(f"source: {news[2]}\n\n")
    
    speak("Hmmm. The world seems doomed")


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
        return
    youtubeSearch=False
    if "youtube" in command:
        for keyword in youtube_keywords:
            if keyword in command:
                youtubeSearch=True

                searchOnYoutube(command,keyword)
        return   
    

    if "search" in command and not youtubeSearch:
        query=command.replace("search","").strip()
        speak(f"Searching for {query} on google")
        pywhatkit.search(query)
        return

    if "open brave" in command or "open browser" in command or "browser" in command:
        speak("Alright, opening brave")
        webbrowser.get("brave").open()
        return

    if "open youtube" in command:
        speak("Alright, opening youtube")
        webbrowser.open("https://www.youtube.com")
        return

    if "repeat after me" in command:
        query=command.replace("repeat after me","")
        speak(query)
        return

    for keyword in date_keywords:
        if keyword in command:
            info=datetime.now()
            current_date=f"today is {info.day} of {months[info.month]} , {info.year}"
            speak(current_date)
            
            
            return

    
    for keyword in time_keywords:
        if keyword in command:
            info=datetime.now()
            time=f"the current time is {info.hour} hours {info.minute} minutes and {info.second} seconds"
            speak(time)
            return
        
    if "play" in command:
        play_song(command)
        return


    for keyword in joke_keywords:
        if keyword in command:
            getJoke()
            return

    for keyword in todo_keywords["identifiers"]:
        if keyword in command:
            query=command.replace("todo","")
            process_todo_command(query)
            return

    for keyword in news_keywords:
        if keyword in command:
            process_news_command()
            return

    if "bye" in command:
        speak("Goodbye")
        exit()


    
if __name__=="__main__":
    while True:
        #command=take_command()
        command=input("Enter command: ")
        process_command(command)
    

