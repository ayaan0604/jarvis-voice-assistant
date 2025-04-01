import sqlite3

class todo:
    def __init__(self,task):
        self.task=task
        self.status=False



def initialize_db():
    #connection open
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    


    #table for todo list
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TODO_LIST(
               SERIAL_NO INTEGER PRIMARY KEY,
               TASK VARCHAR(1024),
               STATUS BOOLEAN)

                ''')
    
    #table for email recipents
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EMAIL_RECIPENTS(
               SERIAL_NO INTEGER PRIMARY KEY,
               NAME VARCHAR(255),
               EMAIL VARCHAR(255));

                ''')
    
    #table for playlists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PLAYLISTS(
               SERIAL_NO INTEGER PRIMARY KEY,
               NAME VARCHAR(255),
               LINK VARCHAR(255))

                ''')

    #connection close
    connection.close()
    

def add_todo(task :str):
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()

    cursor.execute('''
        INSERT INTO TODO_LIST(TASK,STATUS)
                   VALUES(?,?)''',(task,False))
    connection.commit()
    connection.close()
    
def get_all_todo():
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    try:
        cursor.execute("SELECT * FROM TODO_LIST")

    except Exception as e:
        print(e)

    tasks=cursor.fetchall()

    

    for task in tasks:
        print(f"{task[0]}.   {task[1]} {"(DONE)" if int(task[2])==1 else "(Pending)"}")


def mark_as_done(number):
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    cursor.execute('''
        UPDATE TODO_LIST
                   SET STATUS=?
                   WHERE SERIAL_NO =?;
    ''',(True,number))
    print(f"marked todo at number {number} as done")
    connection.commit()
    connection.close()

def get_pending_todo():
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    cursor.execute('''
            SELECT * FROM TODO_LIST WHERE NOT STATUS=1;
        ''')
    tasks=cursor.fetchall()
    connection.commit()
    connection.close()
    print("Pending todos:")

    for task in tasks:
        print(f"{task[0]}.   {task[1]} {"(DONE)" if int(task[2])==1 else "(Pending)"}")



def delete_all_todo():
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    cursor.execute("DELETE FROM TODO_LIST")
    connection.commit()
    connection.close()


#playlist funtions
#funtion to take the name and link of a playlist and save it to the database
def save_playlist(name,link):
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    cursor.execute('''INSERT INTO PLAYLISTS(NAME,LINK)
                    VALUES(?,?)''',(name,link))
    connection.commit()
    connection.close()

#funtion to take name and return link of a saved playlist
def get_playlist(name):
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    playlist_link=None
    try:
        cursor.execute('''SELECT LINK FROM PLAYLISTS
                       WHERE NAME=?''',(name,))
        if cursor.fetchone():
            playlist_link=cursor.fetchone()[0]
        

    except Exception as e:
        print(e)
    finally:
        connection.close()
    
    if playlist_link:
        return playlist_link
    return None

#function to delete a playlist from database
def delete_playlist(name):
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    cursor.execute('''DELETE FROM PLAYLISTS WHERE NAME=?''',(name,))
    connection.commit()
    connection.close()    

#function to get all the playlist names
def view_playlists():
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    try:
        cursor.execute('''SELECT NAME FROM PLAYLISTS''')
        playlists=cursor.fetchall()
        i=1
        for title in playlists:
            print(f"{i}. {title[0]}")
            i+=1

    except Exception as e:
        print(e)
    
    connection.close()

#functions for emails
def mail_already_registered(email):
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    try:
        cursor.execute('''SELECT * FROM EMAIL_RECIPENTS WHERE EMAIL=?''',(email,))
        recipent=cursor.fetchone()
        if recipent==None:
            return False
        else:
            return True

    except Exception as e:
        print(e)

def add_email(name,email):
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    if not mail_already_registered(email):

        try:
            cursor.execute('''INSERT INTO EMAIL_RECIPENTS(NAME,EMAIL)
                           VALUES(?,?)''',(name,email))
            connection.commit()
            print(f"Successfully added mail {email} with tha name {name} into the recipent list")

        except Exception as e:
            print(e)
    
    else:
        print(f"email already registerd")
    connection.close()

def get_all_emails():
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    cursor.execute('''SELECT * FROM EMAIL_RECIPENTS''')
    recipents=cursor.fetchall()
    if not recipents:
        print("The recipent list is empty")
        return
    i=0
    print("\n")
    for recipent in recipents:
        i+=1
        print(f"{i}) Name: {recipent[1]}\tEmail: {recipent[2]}")
    print("\n")   
    connection.close()

def delete_email(email):
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    if mail_already_registered(email):
        try:
            cursor.execute('''DELETE FROM EMAIL_RECIPENTS WHERE EMAIL=?''',(email,))
            connection.commit()
            print(f"Deleted email {email}")
        
        except Exception as e:
            print(e)

    else:
        print("email does not exists")
    connection.close()

def get_mail(name):
    
    connection= sqlite3.connect("Jarvis_Database.db")
    cursor=connection.cursor()
    cursor.execute('''SELECT EMAIL FROM EMAIL_RECIPENTS WHERE NAME=?''',(name,))
    recipent=cursor.fetchone()
    if not recipent:
        
        return None
    
    return recipent[0]
    