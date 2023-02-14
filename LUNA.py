import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
from time import *
import threading
from threading import *
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from playsound import playsound
import os
import mysql.connector
from tabulate import *
import textwrap

def wrapu(txt,wid):
    return textwrap.TextWrapper(width=wid).fill(text=txt)


mydb= mysql.connector.connect(host="localhost", user="root", passwd="1234", database="python_project")
mycursor = mydb.cursor()

vName = "luna"
x = 0
a = 0
c = 0
lok = ''


lisButton = ''

root = Tk()
root.title(vName)
root.geometry("1920x1080")


main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

second_frame = Frame(my_canvas)

width=root.winfo_screenwidth()
print(width)
my_canvas.create_window((960,0), window=second_frame, anchor="n")

root.resizable(0, 0)

# do root.update_idletasks() then my_canvas.configure(scrollregion = self.my_canvas.bbox('all'))


PressImg = Image.open('PressButton1.png').resize((175, 188))
PressButton = ImageTk.PhotoImage(PressImg)

HighlightImg = Image.open('HighlightButton.png').resize((201, 201))
HighlightButton = ImageTk.PhotoImage(HighlightImg)

GreenImg = Image.open('GreenButton.png').resize((175, 175))
GreenButton = ImageTk.PhotoImage(GreenImg)


listener = sr.Recognizer()
engine = pyttsx3.init()

# female voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# speak rate
engine.setProperty('rate', 150)


class kinter(Thread):
    def run(self):
        global lok, lisButton, a, PressButton, HighlightButton, GreenButton

        print("kinter")

        def activate():
            global a, c
            if a == 0:
                lisButton.config(image=GreenButton)
                playsound("ginitial.mp3")
                a = 1
                c = 1

        def highlight(event):
            if a == 0:
                lisButton.config(image=HighlightButton)

        def unhighlight(event):
            if a == 0:
                lisButton.config(image=PressButton)



        lisButton = Button(second_frame, image=PressButton,
                           borderwidth="0", command=activate)

        lisButton.bind("<Enter>", highlight)
        lisButton.bind("<Leave>", unhighlight)
        lisButton.pack()

                # . grid(row=1,column=0)
        lok = Label(second_frame,text="", font=('Consolas',7 ))
        lok.pack()


class comp1(Thread):
    def run(self):
        print("comp1")

        def changeTxt(txt):
            global lok, lisButton, vName
            lok.config(text=txt)

        def talk(text):
            engine.say(text)
            engine.runAndWait()

        def take_command():

            try:
                with sr.Microphone() as source:
                    print('listening...')
                    voice = listener.listen(source)
                    command = listener.recognize_google(voice)
                    command = command.lower()
                    print(command)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                if a == 1:
                    playsound('gfinal.mp3')
                command = take_command()
            except sr.RequestError as e:
                print(
                    "Could not request results from Google Speech Recognition service; {0}".format(e))
                command = take_command()
            return command

        def run_alexa():
            global a, c, PressButton, HighlightButton, GreenButton
            b = 1
            command = take_command()
            print(command)

            # if we know that alexa is aloneeee in the statement
            # if we know that there is something else besides alexa
            # hi jjk alexa what is the time
            n = command.rfind(vName)+5
            comcheck = command[n:]

            if vName in command and a==0:

                lisButton.config(image=GreenButton)

                a = 1
                b = 1

                if comcheck == "" or comcheck == " " or c == 1:
                    b = 0
                    c = 0
                    playsound("ginitial.mp3")

            print(command)

            def alldb(table):
                mycursor.execute("describe "+table)
                h=[]
                for i in mycursor:
                    h.append(i[0])
                
                tempo="select * from python_project."+table

                mycursor.execute(tempo)

                a=[]
                a.append(h)
                for i in mycursor:
                    a.append(i)
                return a

            def part(table,name):
                mycursor.execute("describe "+table)
                h=[]
                for i in mycursor:
                    h.append(i[0])
                
                
                tempo = "select * from "+table +" where lower(Book_Title) like" +'"%' + name + '%"'
                print(tempo)

                mycursor.execute(tempo)

                a=[]
                a.append(h)
                for i in mycursor:
                    a.append(i)
                return a


            if a == 1 and b == 1:

                if 'top' in command and "book" in command:
                   if 'author' in command:
                        data=alldb("books_author_database")

                        lst=list(map(list,data))
                        for i in lst:
                            i[3]=wrapu(i[3],100)
                            
                        data=tabulate(lst,headers="firstrow",showindex="always",tablefmt="grid")
                        changeTxt(data)
                        my_canvas.configure(scrollregion = my_canvas.bbox('all'))
                        changeTxt(data)
                        
                   elif 'buy' in command:
                        data=alldb("books_buy_database")

                        lst=list(map(list,data))
                        for i in lst:
                            i[1]=wrapu(i[1],35)
                            i[2]=wrapu(i[2],55)
                            i[3]=wrapu(i[3],80)
                            i[4]=wrapu(i[4],55)
                            
                        data=tabulate(lst,headers="firstrow",showindex="always",tablefmt="grid")
                        changeTxt(data)
                        my_canvas.configure(scrollregion = my_canvas.bbox('all'))

                        changeTxt(data)

                   elif 'info' in command or 'information' in command:
                        data=alldb("books_info_database")

                        lst=list(map(list,data))
                        for i in lst:
                            i[1]=wrapu(i[1],30)
                            i[2]=wrapu(i[2],30)
                            i[4]=wrapu(i[4],20)
                            i[6]=wrapu(i[6],20)
                            i[10]=wrapu(i[10],20)
                            
                        data=tabulate(lst,headers="firstrow",showindex="always",tablefmt="grid")
                        changeTxt(data)
                        my_canvas.configure(scrollregion = my_canvas.bbox('all'))

                        changeTxt(data)

            

                elif "book" in command:
                   if 'author' in command:
                        n = command.rfind("book")+5
                        name = command[n:]                        

                        data=part("books_author_database",name)

                        lst=list(map(list,data))
                        for i in lst:
                            i[3]=wrapu(i[3],100)
                            
                        data=tabulate(lst,headers="firstrow",showindex="always",tablefmt="grid")
                        changeTxt(data)
                        my_canvas.configure(scrollregion = my_canvas.bbox('all'))
                        changeTxt(data)
                        
                   elif 'buy' in command:
                        n = command.rfind("book")+5
                        name = command[n:]    

                        data=part("books_buy_database",name)

                        lst=list(map(list,data))
                        for i in lst:
                            i[1]=wrapu(i[1],35)
                            i[2]=wrapu(i[2],55)
                            i[3]=wrapu(i[3],80)
                            i[4]=wrapu(i[4],55)
                            
                        data=tabulate(lst,headers="firstrow",showindex="always",tablefmt="grid")
                        print(data)
                        changeTxt(data)
                        my_canvas.configure(scrollregion = my_canvas.bbox('all'))
                        changeTxt(data)

                   elif 'info' in command or 'information' in command:
                        n = command.rfind("book")+5
                        name = command[n:]    

                        data=part("books_info_database",name)

                        lst=list(map(list,data))
                        for i in lst:
                            print(i)
                            i[1]=wrapu(i[1],30)
                            i[2]=wrapu(i[2],30)
                            i[4]=wrapu(i[4],30)

                            
                        data=tabulate(lst,headers="firstrow",showindex="always",tablefmt="grid")
                        changeTxt(data)
                        my_canvas.configure(scrollregion = my_canvas.bbox('all'))
                        changeTxt(data)
                    


                elif 'play' in command:
                    n = command.rfind("play")+4
                    song = command[n:]

                    changeTxt(str('playing ' + song))
                    talk('playing ' + song)
                    pywhatkit.playonyt(song)

                elif 'time' in command:
                    time = datetime.datetime.now().strftime('%I:%M %p')
                    changeTxt('Current time is ' + time)
                    talk('Current time is ' + time)

                elif 'who is' in command:
                    n = command.rfind("who is")+6

                    person = command[n:]
                    try:

                        info = wikipedia.summary(person, 1)
                        info1=wrapu(str(info),500)

                        changeTxt(info1)

                        changeTxt(str(info))
                        talk(info)
                    except:
                        pass

                elif 'what is' in command:
                    n = command.rfind("what is")+7
                    obj = command[n:]
                    try:
                        
                        info = wikipedia.summary(obj, 1)
                        info1=wrapu(str(info),500)

                        changeTxt(info1)
                        talk(info)
                    except:
                        pass

                elif 'joke' in command:
                    jok = pyjokes.get_joke()
                    changeTxt(jok)
                    talk(jok)

                elif 'terminate' in command:
                    changeTxt("Process Terminated")
                    talk("Yes yes, Master, I shall go away this instance, please dont get angry")
                    playsound("gfinal.mp3")
                    global x
                    x = 1
                else:
                    talk('Please say the command again.')

        while x == 0:
            run_alexa()
        os._exit(0)


t1 = kinter()
t2 = comp1()

t1.start()
t2.start()
mainloop()





#author top book
#buy top book
#information of top book
#say something else instead of "please say that command again"
# check use of global in code for necessity
# wikipedia error try except
# append read books on mysql and give output of read books
# start new line when going out of frame