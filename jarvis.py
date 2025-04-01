import speech_recognition as sr
import pyttsx3
import pywhatkit
from datetime import datetime
import webbrowser
from keywords import *
import pyjokes
from database import *
from news import get_news
from auto_email import send_email

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
        speak("Here are the todo related commands\n\n")
        i=1
        for help in todo_keywords['todo_help']:
            print(f"{i}) {help}")
            i+=1
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

def process_email_command(query):
    if "add" in query:
        speak("Do you want to add an email into the recipent list? Type yes to confirm")
        choice=input("Enter your choice: ").lower()
        if "yes" not in choice:
            speak("cancelling request")
            return
        
        
        speak("Please type in the name and email address of the recipent")
        name=input("Enter name: ")
        email=input("Enter email: ")
        
        speak("Please confirm the name and email address of the recipent")

        print(f"Name: {name}\t Email: {email}")
        choice=input("Enter yes to confirm: ")
        if "yes" not in choice:
            speak("Cancellinig request! Say add email to restart adding process")
            return
        
        try:
            add_email(name,email)
            speak("Email added successfully into the recipent list")
            return
        except Exception as e:
            print("Some error occured: ",e)

    if "delete" in query:
        speak("Enter the email of the recipent to delete")
        get_all_emails()
        speak("Enter 0 to cancel")

        email=input("Enter email: ")
        if email=='0':
            speak("Cancelling request")
            return

        if not mail_already_registered(email):
            print("Email not present in the list")
            return
        try:
            delete_email(email)
            speak("Deleted the email successfully")
            return
        except Exception as e:
            print(f"Error deleting email: {e}")

    if "view" in query:
        speak("Here is your email recipent list")
        try:
            get_all_emails()
            return
        except Exception as e:
            print(f"Error occurred: {e}")
            return        

    if "send" in query:
        
        confirmed=False

        
        speak("Enter the name of the recipent. Enter 0 to cancel")

        name=input("Enter name: ")
        if name=="0":
            print("Cancelling request")
            return
        
        #try fetching the email from database
        email=get_mail(name)
        if not email:
            speak(f'''No email found with the name {name}. You can say "send email" to restart the process ''')
            return
        
        speak(f"Do you want to send email to {name} with email {email} ")

        choice=input("Enter yes to confirm: ")
        if "yes" not in choice:
            speak("Okay! You can say send email to start the process again")               
            return
        
        speak("Okay! would you like to speak the message or write it?")
        #now the user has confirmed the recipent
        choice_confirmed=False
        global text_input_choice
        text_input_choice=False
        while(not choice_confirmed):
            
            choice=input("Enter speak or write: ")
            if "speak" in choice:
                text_input_choice=False
                break
                
            elif "write" in choice:
                text_input_choice=True
                break
            else:
                print("Please enter a valid choice")
                continue

        global subject
        global message
    


        #if user has selected text input
        if text_input_choice:

            global data_confirmed
            data_confirmed=False
            while(not data_confirmed):

                speak("Enter the Subject")
                subject=input("Subject: ")
                speak("Enter message")
                message=input("Enter message: ")

                speak("Please confirm message to proceed")
                print(f"\nSubject: {subject}\nMessage: {message}\n")
                choice=input("Enter yes to confirm")
                if "yes" not in choice:
                    continue

                else:
                    data_confirmed=True
        


        #if user has selected voice input
        else:
            global subject_confirmed, message_confirmed
            subject_confirmed=False
            message_confirmed=False
            while(not subject_confirmed):
                speak("Enter the subject")
                subject=take_command()
                speak(f"{subject}. Is that correct? Say yes to confirm")
                choice=take_command()

                if "yes" in choice:
                    subject_confirmed=True
                    break
            
                else:
                    continue

            #subject confirmed

            while(not message_confirmed):
                speak("Record the message")
                message=take_command()
                speak(f"Please confirm the message.")
                speak(message)
                speak("Say yes to confirm")
                choice=take_command()
                if "yes" in command:
                    message_confirmed=True
                    break
                else:
                    continue

        #at this point, user has confirmed all the parameters so we can try sending the mail
        final_message=message+"\nThis email was sent through a virtual assistant."
        status=send_email(email, subject, final_message)
        speak(status)
        return

    if "help" in query:
        i=1
        for line in email_help:
            print(f"{i}) {line}")
            i+=1
        return

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
            query=command.replace("to do","")
            process_todo_command(query)
            return

    for keyword in news_keywords:
        if keyword in command:
            process_news_command()
            return

    if "email" in command:
        process_email_command(command)

    if "bye" in command:
        speak("Goodbye")
        exit()


    
if __name__=="__main__":
    voice_input=False
    if voice_input:
        print("Enter 'voice input' to change to voice mode")
    else:
        print("Enter 'text input' to change to text mode")
    
    while True:
        if voice_input:
            command=take_command()
            if "text input" in command:
                speak("changing the input mode into text")
                voice_input=False
                continue
        
        if not voice_input:
            command=input("Enter command: ")
            if "voice input" in command:
                speak("Alright! now i will respond to your voice")
                voice_input=True
                continue
        
        process_command(command)
    

