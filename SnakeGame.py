import sys
import turtle
from tkinter import messagebox
import random
import time
import string
import pywhatkit as pwk
import datetime

uname = ""
password = ""

######## GAME ########
WIDTH, HEIGHT = 700, 700
delay = 0.08
score = 0
high_score = 0
segments = []

wn = turtle.Screen()
wn.setup(WIDTH, HEIGHT)
wn.title("Snake Game")
wn.bgcolor('black')
wn.tracer(0)

text = turtle.Turtle()
text.goto(-250, 280)
text.color('white')
text.hideturtle()
text.penup()

food = turtle.Turtle()
food.speed(0)
food.shape('circle')
food.shapesize(0.75,0.75)
food.color('red')
food.penup()

head = turtle.Turtle()
head.color('white')
head.shape('square')
head.speed(0)
head.penup()
head.goto(0,0)
head.direction = 'stop'


try:
    var = turtle.textinput("Color of Snake", "(Red, Blue, Green, Pink, Orange, Purple, Gray, Yellow)\nWhat color will your snake be: ")
    snakeColor = var.lower()
except:
    messagebox.showinfo("Warning", "Please Type a 'color' like above!")
    sys.exit()


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)


def goUP():
    if head.direction != 'down':
        head.direction = 'up'

def goDOWN():
    if head.direction != 'up':
        head.direction = 'down'

def goRIGHT():
    if head.direction != 'left':
        head.direction = 'right'

def goLEFT():
    if head.direction != 'right':
        head.direction = 'left'


def randFood():
    x = random.randint(-16, 14)*20
    y = random.randint(-16, 14)*20
    food.goto(x,y)

def collisions():
    global score, delay, uname
    if head.distance(food) < 20:
        randFood()
        score += 10
        delay -= 0.001
        addSegment()
    
    for index in range(len(segments)-1,0,-1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    if (head.xcor() >= WIDTH//2 or head.xcor() <= -WIDTH//2) or (head.ycor() >= HEIGHT//2 or head.ycor() <= -HEIGHT//2):
        time.sleep(0.5)
        head.direction = 'stop'
        head.goto(0,0)
        for segment in segments:
            segment.goto(1000,1000)

        with open("stats.txt", "a+") as file:
            file.write(uname + "," + str(score) + "\n")

        segments.clear()
        score = 0
        delay = 0.15

def writeScore():
    global high_score
    if score > high_score:
        high_score = score

    text.write("Score: {}\nHigh Score: {}".format(score,high_score), move=False, align='center',font=('Futura-Bold',14,'normal')) 
"""        with open("datafile.txt", "a") as file:
            users = file.readlines()
        for user in users:
            hs = user.split(",")[2]
            hs = user[:-1]
            hs = score"""

    

    
def addSegment():
    new_segment = turtle.Turtle()
    new_segment.color(snakeColor)
    new_segment.shape('square')
    new_segment.speed(0)
    new_segment.penup()
    segments.append(new_segment)


def mainRun():   
    
    wn.listen()
    wn.onkey(goUP, 'Up')
    wn.onkey(goDOWN, 'Down')
    wn.onkey(goRIGHT, 'Right')
    wn.onkey(goLEFT, 'Left')
    
    while True:
        wn.update()
        text.clear()
        writeScore()
        collisions()
        move()
        time.sleep(delay)


######## LOGIN ########
def menu(): 
    while True:    
        try:
            option = int(turtle.textinput("Login",
            """
            What do you want to do:
            1. Sign up
            2. Log in
            3. Forgot my Password
            4. Exit
            """
            ))
        except ValueError:
            messagebox.showinfo("Warning", "Please Type a number(1-3)!")
            continue
        except:
            messagebox.showinfo("Warning", "Something went wrong... Try again!")
            sys.exit()

        if option == 1:
            signUp()
        elif option == 2:
            LogIn()
        elif option == 3:
            forgotPassword()
        elif option == 4:
            sys.exit()
        else:
            messagebox.showinfo("Warning", "Please Type a number(1-3)!")
            continue


def signUp():
    while True:
        try:
            loginuname = turtle.textinput("Sign up", "Please Create a Username!")
            loginpassw = turtle.textinput("Sign up", "Please Create a new Password!")
            loginpasswrepeat = turtle.textinput("Sign up", "Please Confirm your Password!")
        except:
            messagebox.showinfo("Warning", "Something went wrong... Try again!")
            sys.exit()

        if loginpassw != loginpasswrepeat:
            messagebox.showinfo("Warning", "Your Passwords do not match... Try again!")
            continue
        else:
            while True:
                lower = string.ascii_lowercase
                upper = string.ascii_uppercase
                numbers = string.digits
                symbols = string.punctuation

                all = lower + upper + numbers + symbols
                rand = random.sample(all, 8)
                password = "".join(rand)

                with open("Activation_Code.txt", "w") as dosya:
                    dosya.write(password)

                actCheck = turtle.textinput("Activation Code", "Your Activation Code has been created.\nPlease Type Your Activation Code Here!")
                
                if actCheck == password:
                    with open("datafile.txt", "a+") as file:
                        file.write(loginuname + "," + loginpassw + "\n")
                    messagebox.showinfo("Information", "Your Account has been successfully created!")
                    mainRun()
                    
                else:
                    messagebox.showinfo("Warning", "The Activation Codes do not match... Try again!")
                    continue


def LogIn():
    global uname, password
    
    try:
        uname = turtle.textinput("Log in", "Please type your Username here!")
        password = turtle.textinput("Log in", "Please type your password here!")
    except:
        messagebox.showinfo("Warning", "Something went wrong... Try again!")
        sys.exit()
    
    with open("datafile.txt", "r") as file:
        users = file.readlines()
    
    for user in users:
        name = user.split(",")[0]
        psw = user.split(",")[1]
        psw = psw[:-1]

    if name == uname and psw == password:
        messagebox.showinfo("Information", "You successfully logged in!")
        mainRun()
    else:
        messagebox.showinfo("Warning", "Something went wrong... Try again!")
        print(psw)
        print(password)
        sys.exit()


def forgotPassword():
    global newPassword

    username = turtle.textinput("Forgot Password", "Please type your username!")
    rand = random.sample(string.digits, 8)
    password = "".join(rand)

    try:
        phoneNumber = turtle.textinput("Forgot Password", "Type Your WhatsApp Number here!\n(like: +491798947264)")
        
        now = datetime.datetime.today()
        one_min_later = now + datetime.timedelta(minutes=1)
        hour = one_min_later.hour
        minute = one_min_later.minute
        
        pwk.sendwhatmsg(str(phoneNumber), str(password), hour, minute)
        messagebox.showinfo("Information", "Your Access Code is successfully sent,\nIt can take 1-2 Minutes!")
    except:
        messagebox.showinfo("Warning", "Something went wrong... Try again!")
        sys.exit()
    
    code = turtle.textinput("Access Code", "Type your code here!")
    if int(password) == int(code):
        newPassword = turtle.textinput("Information", "Your Code is True!\nSelect your new password!")
        messagebox.showinfo("Information", "Your Password is changed\nYou can now log in!")

        with open("datafile.txt", "r") as file:
            users = file.readlines()
        
        dosya = open("datafile.txt", "w")
        counter = 0
        for user in users:
            if user.split(",")[0] == uname: # kayıtlı username ile girilen ismi aynı ise
                users[counter] = uname + "," + newPassword + "\n" # listenin ilgili satırını güncelle
                dosya.write(users[counter]) # dosyaya güncel satırı yaz
            else:
                dosya.write(user) # dosyaya satırı yaz
            counter += 1 # her seferinde counter artır
        dosya.close()

    else:
        messagebox.showinfo("Warning", "Your Code is not True... Try again!")
        sys.exit()


menu()
