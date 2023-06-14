import os
import threading
import pygame
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox
from functools import partial
import json
from os import path
import hashlib
from tkinter import filedialog
from PIL import Image, ImageDraw
from fpdf import FPDF
import copy
from jinja2 import Template

pygame.font.init()

LENGTH = 200
WIN_WIDTH = 8.5 * LENGTH
WIN_HEIGHT = 4.5 * LENGTH

FONT1 = pygame.font.SysFont('comicsans', 20)
FONT2 = pygame.font.SysFont('comicsans', 60)


class LoginForm:
    def __init__(self, rootLogin):
        self.rootLogin = rootLogin
        self.rootLogin.title('Login')
        self.rootLogin.geometry('400x300')
        self.rootLogin.configure(bg="white")
        self.rootLogin.resizable(False, False)

        self.frame = Frame(rootLogin, width=400, height=300, bg="white")
        self.frame.place(x=0, y=0)
        heading = Label(self.frame, text='LOGIN', fg='#717F8A', bg='white',
                        font=('Microsoft YaHei UI Light', 18, 'bold'))
        heading.place(x=155, y=10)

        usernamelabel = Label(self.frame, text='Username:', fg='black', bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        usernamelabel.place(x=45, y=80)

        passwordlabel = Label(self.frame, text='Password:', fg='black', bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        passwordlabel.place(x=50, y=120)

        self.username = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        self.username.place(x=110, y=80)

        self.password = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                              font=('Microsoft YaHei UI Light', 9), show='*')
        self.password.place(x=110, y=120)

        self.buttonLogin = Button(self.frame, width=20, pady=10, text='Log In', bg='#717F8A', fg='white', border=1,
                                  command=self.LogIn)
        self.buttonLogin.place(x=125, y=170)

        self.buttonRegister = Button(text='Don\'t have an account yet? Click here', borderwidth=0, bg='white',
                                     command=self.Register)
        self.buttonRegister.place(x=95, y=240)

    def Register(self):
        self.Register = Tk()
        self.Register.title('Register')
        self.Register.geometry('400x300')
        self.Register.resizable(False, False)
        self.Register.configure(bg="white")
        self.frame = Frame(self.Register, width=400, height=300, bg="white")
        self.frame.place(x=0, y=0)

        headingregister = Label(self.frame, text='REGISTER', fg='#717F8A', bg='white',
                                font=('Microsoft YaHei UI Light', 18, 'bold'))
        headingregister.place(x=135, y=0)

        usernamereglabel = Label(self.frame, text='Username:', fg='black', bg='white',
                                 font=('Microsoft YaHei UI Light', 9))
        usernamereglabel.place(x=45, y=70)

        passwordlabel = Label(self.frame, text='Password:', fg='black', bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        passwordlabel.place(x=50, y=120)

        confpasswordlabel = Label(self.frame, text='Confirm\npassword:', fg='black', bg='white',
                                  font=('Microsoft YaHei UI Light', 9))
        confpasswordlabel.place(x=50, y=153)

        self.usernameReg = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                                 font=('Microsoft YaHei UI Light', 9))
        self.usernameReg.place(x=110, y=70)

        self.passwordReg = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                                 font=('Microsoft YaHei UI Light', 9), show='*')
        self.passwordReg.place(x=110, y=120)

        self.confirmPasswordReg = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                                        font=('Microsoft YaHei UI Light', 9), show='*')
        self.confirmPasswordReg.place(x=110, y=170)

        self.buttonSingup = Button(self.frame, width=20, pady=10, text='Sign Up', bg='#717F8A', fg='white', border=1,
                                   command=self.SignUp)
        self.buttonSingup.place(x=125, y=220)

    def SignUp(self):
        i = 1
        with open('login.txt', 'r') as f:
            content = f.read()

            if self.usernameReg.get() not in content:
                if len(self.usernameReg.get()) > 3:
                    if self.passwordReg.get() == self.confirmPasswordReg.get():
                        if len(self.passwordReg.get()) > 5:
                            with open('login.txt', 'a') as f:
                                f.write(self.usernameReg.get() + ':' + hashlib.sha256(
                                    self.passwordReg.get().encode('utf-8')).hexdigest() + ':')

                                while path.isfile('json/' + str(i) + '.json'):  # Tworzenie pliku .json
                                    i += 1
                                
                                name = 'json/' + str(i) + '.json'
                                with open(name, 'w') as file:
                                    file.write('[]')
                                    f.write(name + '\n')

                        else:
                            messagebox.showerror('Error', 'Password must have at least 6 characters!')
                    else:
                        messagebox.showerror('Error', 'Passwords do not match!')
                else:
                    messagebox.showerror('Error', 'Username must have at least 4 characters!')
            else:
                messagebox.showerror('Error', 'Username already exists!')

    def LogIn(self):
        with open('login.txt', 'r') as f:
            content = f.read()

            for line in content.split('\n')[1:-1]:
                arr = line.split(':')

                if self.username.get() == arr[0] and hashlib.sha256(self.password.get().encode('utf-8')).hexdigest() == arr[1]:
                    root.destroy()

                    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
                    game = Game(WIN, arr[2])
                    game.loadFromJSON()
                    game.main()

            messagebox.showerror('Error', 'Invalid username or password!')


class InfoWindow:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def draw(self, win):
        pass


class ButtonLogOut:
    def __init__(self) -> None:
        self.text = FONT2.render("save", 1, (0, 0, 0))
        self.x = int(WIN_WIDTH - self.text.get_width() - 20)
        self.y = int(WIN_HEIGHT - self.text.get_height() - 10)
        self.height = int(self.text.get_width())
        self.width = int(self.text.get_width())
        self.isclicked = False

    def draw(self, win):
        x, y = pygame.mouse.get_pos()
        if x in range(self.x, self.x + self.width) and y in range(self.y, self.y + self.height):
            self.text = FONT2.render("save", 1, (200, 200, 200))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == 1:
                print("Zapisano")
                self.isclicked = True

        else:
            self.text = FONT2.render("save", 1, (0, 0, 0))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.isclicked = False

        win.blit(self.text, (self.x, self.y))


logout = ButtonLogOut()


# tworzy listę rozwijaną osoby
class PersonList:
    def __init__(self, x, y, buttons) -> None:
        self.x = x
        self.y = y
        self.buttons = buttons
        self.width = 300
        self.height = len(buttons) * 50
        self.color = (240, 240, 240)
        self.isclicked = False

    def draw(self, win):
        x, y = pygame.mouse.get_pos()
        if x in range(self.x, self.x + self.width) and y in range(self.y, self.y + self.height):
            if pygame.mouse.get_pressed()[0] == 1:
                self.isclicked = True

            if pygame.mouse.get_pressed()[2] == 1:
                self.isclicked = False

        # sprawia że wyświetlana lista jest w oknie programu
        for button in self.buttons:
            if self.x > WIN_WIDTH - self.width:
                button.x = button.x - self.width
            if self.y > WIN_HEIGHT - self.height:
                button.y = button.y - self.height
            button.draw(win)
        if self.x > WIN_WIDTH - self.width:
            self.x = self.x - self.width
        if self.y > WIN_HEIGHT - self.height:
            self.y = self.y - self.height


def do_nothing():
    pass


# klasa przycisk
class ButtonList:
    def __init__(self, x, y, text="", command=do_nothing, command2=do_nothing) -> None:
        self.x = x
        self.y = y
        self.command = command
        self.command2 = command2
        self.text = FONT1.render(str(text), 1, (0, 0, 0))
        self.width = 300
        self.height = 50
        self.costume = 0
        self.colors = [(240, 240, 240), (200, 200, 200)]
        self.isclicked = False
        self.time = 0

    def draw(self, win):

        x, y = pygame.mouse.get_pos()
        if x in range(self.x, self.x + self.width) and y in range(self.y, self.y + self.height):
            self.costume = 1
            self.time += 1
            if pygame.mouse.get_pressed()[0] == 1:
                self.isclicked = True
                self.command()
            elif pygame.mouse.get_pressed()[2] == 1:
                self.isclicked = False

            if self.time > 20:
                self.command2()
        else:
            self.costume = 0
            self.time = 0

        pygame.draw.rect(win, self.colors[self.costume], (self.x, self.y, self.width, self.height))
        win.blit(self.text, ((2 * self.x + self.width) // 2 - (self.text.get_width()) // 2,
                             (2 * self.y + self.height) // 2 - (self.text.get_height()) // 2))


class Person:
    def __init__(self, id, x=100, y=100, r=80, name="", surname="", bornYear=0, img="no-image.jpg",
                 relations={"parents": [], "childrens": [], "siblings": [], "partner": []},
                 colors=[(255, 255, 255), (255, 255, 255)], costume=0, bool=False, current=False, isclickedR=False,
                 isclickedL=False, time=0) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.name = name
        self.surname = surname
        self.bornYear = bornYear
        self.img = img
        self.relations = relations
        self.colors = colors
        self.costume = costume
        self.bool = bool
        self.current = current
        self.isclickedR = isclickedR
        self.isclickedL = isclickedL
        # self.partner = None
        self.time = time
        # self.relationsCount = 0

    def draw(self, win):
        x, y = pygame.mouse.get_pos()

        #if ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5 <= self.r:
        if all([x >= self.x - self.r, x<= self.x + self.r, y>= self.y - self.r , y<= self.y + self.r]):
            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # self.costume = 1
            self.time += 1
            if pygame.mouse.get_pressed()[2] == 1:
                self.isclickedR = True
                self.time = 0
            else:
                self.isclickedR = False

            if pygame.mouse.get_pressed()[0] == 1:
                self.isclickedL = True
                self.time = 0

            else:
                self.isclickedL = False
                self.current = False

        else:
            self.current = False
            self.time = 0
            # self.costume = 0

        if self.isclickedL and self.current:
            self.x = x
            self.y = y

        pygame.draw.circle(win, self.colors[self.costume], (self.x, self.y), self.r)  # rysuje osobę
        # for relation in list(self.relations):
        #    pygame.draw.line(win,self.color,(self.x,self.y),(relation.x,relation.y)) #rysuje relacje między osobami
        s = FONT1.render(f"{self.name} {self.surname}", 1, (0, 0, 0))
        win.blit(pygame.transform.scale(pygame.image.load(os.path.join(self.img)), (160, 160)), (self.x - self.r,self.y - self.r))
        win.blit(s, (self.x - s.get_width() // 2,
                     (self.y - s.get_height() // 2) + 1.2 * self.r))  # wyświetla imię, nazwisko i rok urodzenia

        # def toJSON(self,filename):
        #    with open(filename, 'w') as file:
        #        file.write(json.dumps(self.__dict__,indent=2))
        # return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4)

        """ 
        if self.time > 250:
            x,y = pygame.mouse.get_pos()
            pygame.draw.rect(win,(30,100,200),(x,y,4*self.r,2*self.r))
            text = FONT1.render(f"{self.name} {self.surname} {self.bornYear}", 1, (255,255,255))
            win.blit(text,(x + 2*self.r-text.get_width()//2,y + self.r-text.get_height()//2)) 
       """


class Game:
    def __init__(self, win,jsonfile="json/persons.json") -> None:
        self.jsonfile = jsonfile
        self.curId = 0
        self.win = win
        self.persons = {}
        self.form = False
        self.currentPerson = None
        self.lastCurrentPerson = None
        self.relationPerson = None
        self.personList = None
        self.list2 = None
        self.newRelation = 0
        self.changing = False

        # self.relationCount = 0
        self.lx = 0
        self.ly = 0

    def forma(self):
        # x,y = pygame.mouse.get_pos()
        self.changing = True
        root = Tk()
        root.geometry("500x500")
        firstname_text = Label(text="Firstname ", )
        firstname_text.place(x=15, y=30)
        firstname = StringVar(value=self.lastCurrentPerson.name)
        firstname_entry = Entry(textvariable=firstname, width="30")
        firstname_entry.place(x=80, y=30)

        surnname_text = Label(text="Surnname  ", )
        surnname_text.place(x=15, y=60)
        surnname = StringVar(value=self.lastCurrentPerson.surname)
        surnname_entry = Entry(textvariable=surnname, width="30")
        surnname_entry.place(x=80, y=60)

        bornyear_text = Label(text="Born Year ", )
        bornyear_text.place(x=15, y=90)
        bornyear = StringVar(value=self.lastCurrentPerson.bornYear)
        bornyear_entry = Entry(textvariable=bornyear, width="30")
        bornyear_entry.place(x=80, y=90)

        AddImg = Button(text="Add Picture", width="30", height="2", command=partial(self.addPicture))
        AddImg.place(x=140, y=180)

        save = Button(text="Save", width="30", height="2",
                      command=partial(self.changeInformation, firstname, surnname, bornyear, root))
        #save.pack()
        #save.bind("<Return>",partial(self.changeInformation, firstname, surnname, bornyear, root))
        save.place(x=140, y=230)

        root.mainloop()

    def edit(self):
        t = threading.Thread(target=self.forma)
        t.start()
        # self.form = True
        self.personList = None
        #self.changing = True

    # uaktualnia dane po edycji w formularzu
    def changeInformation(self, name, surname, bornyear, root):
        self.lastCurrentPerson.name = name.get()
        self.lastCurrentPerson.surname = surname.get()
        self.lastCurrentPerson.bornYear = bornyear.get()
        self.changing = False
        root.destroy()
        # self.form = False

    def addPerson(self):
        print("person")
        if not self.changing:
            x, y = pygame.mouse.get_pos()
            self.persons[self.curId] = Person(id=self.curId, x=x, y=y)  # dodaje osobę do listy osób
            self.lastCurrentPerson = self.persons[self.curId]
            self.edit()
            self.relationPerson = None
            self.currentPerson = None
            self.relationPerson = None
            self.newRelation = 0
            self.curId += 1

    def addParent(self):
        print("parent")
        if not self.changing:
            x, y = pygame.mouse.get_pos()
            self.persons[self.curId] = Person(id=self.curId, x=self.lastCurrentPerson.x, y=self.lastCurrentPerson.y - 200)  # dodaje osobę do listy osób
            self.lastCurrentPerson.relations["parents"].append(self.curId)
            self.persons[self.curId].relations["childrens"].append(self.lastCurrentPerson.id)
            self.lastCurrentPerson = self.persons[self.curId]
            self.edit()
            self.curId += 1
        # newPerson.relationsCount += 1
        # self.lastCurrentPerson.relationsCount += 1
        # self.relationCount += 2

    def addChild(self):
        print("child")
        if not self.changing:
            x, y = pygame.mouse.get_pos()
            self.persons[self.curId] = Person(id=self.curId, x=self.lastCurrentPerson.x, y=self.lastCurrentPerson.y + 300)  # dodaje osobę do listy osób
            self.lastCurrentPerson.relations["childrens"].append(self.curId)
            self.persons[self.curId].relations["parents"].append(self.lastCurrentPerson.id)
            self.lastCurrentPerson = self.persons[self.curId]
            self.edit()
            self.curId += 1
        # newPerson.relationsCount += 1
        # self.lastCurrentPerson.relationsCount += 1
        # self.relationCount += 2

    def addSibling(self):
        print("sibling")
        if not self.changing:
            x, y = pygame.mouse.get_pos()
            self.persons[self.curId] = Person(id=self.curId, x=self.lastCurrentPerson.x + 200, y=self.lastCurrentPerson.y)  # dodaje osobę do listy osób
            self.lastCurrentPerson.relations["siblings"].append(self.curId)
            self.persons[self.curId].relations["siblings"].append(self.lastCurrentPerson.id)
            self.lastCurrentPerson = self.persons[self.curId]
            self.edit()
            self.curId += 1

        # newPerson.relationsCount += 1
        # self.lastCurrentPerson.relationsCount += 1
        # self.relationCount += 2

    def addPartner(self):
        print("partner")
        if not self.changing:
            x, y = pygame.mouse.get_pos()
            self.persons[self.curId] = Person(id=self.curId, x=self.lastCurrentPerson.x - 200, y=self.lastCurrentPerson.y)  # dodaje osobę do listy osób
            self.lastCurrentPerson.relations["partner"].append(self.curId)
            self.persons[self.curId].relations["partner"].append(self.lastCurrentPerson.id)
            #self.lastCurrentPerson.relations["childrens"], self.persons[self.curId].relations["childrens"] = \
            #    self.lastCurrentPerson.relations["childrens"] + self.persons[self.curId].relations["childrens"], \
            #    self.lastCurrentPerson.relations["childrens"] + self.persons[self.curId].relations["childrens"]
            self.lastCurrentPerson = self.persons[self.curId]
            self.edit()
            self.curId += 1

        # newPerson.relationsCount += 1
        # self.lastCurrentPerson.relationsCount += 1
        # self.relationCount += 2

    def connectParent(self):
        self.newRelation = 1
        self.relationPerson = copy.deepcopy(self.lastCurrentPerson)

    def connectChild(self):
        self.newRelation = 2
        self.relationPerson = copy.deepcopy(self.lastCurrentPerson)

    def connectSibling(self):
        self.newRelation = 3
        self.relationPerson = copy.deepcopy(self.lastCurrentPerson)

    def connectPartner(self):
        self.newRelation = 4
        self.relationPerson = copy.deepcopy(self.lastCurrentPerson)

    def info(self):
        print(
            f"name: {self.lastCurrentPerson.name} surname: {self.lastCurrentPerson.surname} age: {self.lastCurrentPerson.bornYear}")
        self.changing = False

    def add(self):
        if self.personList.buttons[2].x + 2 * self.personList.width > WIN_WIDTH:
            xList = self.personList.buttons[2].x - self.personList.width
        else:
            xList = self.personList.buttons[2].x + self.personList.width

        yList = self.personList.buttons[2].y

        self.list2 = PersonList(xList, yList, [ButtonList(xList, yList, "Parent", self.addParent),
                                            ButtonList(xList, yList + 50, "Sibling", self.addSibling),
                                            ButtonList(xList, yList + 100, "Child", self.addChild),
                                            ButtonList(xList, yList + 150, "Partner", self.addPartner)])

    def connect(self):
        if self.personList.buttons[2].x + 2 * self.personList.width > WIN_WIDTH:
            xList = self.personList.buttons[3].x - self.personList.width
        else:
            xList = self.personList.buttons[3].x + self.personList.width

        yList = self.personList.buttons[3].y

        self.list2 = PersonList(xList, yList, [ButtonList(xList, yList, "With parent", self.connectParent),
                                               ButtonList(xList, yList + 50, "With sibling", self.connectSibling),
                                               ButtonList(xList, yList + 100, "With child", self.connectChild),
                                               ButtonList(xList, yList + 150, "With partner", self.connectPartner)])

    def backToStart(self):
        for person in list(self.persons.values()):
            person.x -= self.lx
            person.y -= self.ly

        self.lx = 0
        self.ly = 0

    def newStartingPoint(self):
        self.lx = 0
        self.ly = 0

    def something(self):
        for person in list(self.persons.values()):
            print(person.relations)

    def addPersonPDF(self,person,pdf,Ids):
    
        image = person["img"]
        name = person["name"]
        surname = person["surname"]
        bornYear = person["bornYear"]
        #relations={"parents": [], "childrens": [], "siblings": [], "partner": []}
        if person["relations"]["parents"] != []:
            parents = ""
            for x in person["relations"]["parents"]:
                parents += (Ids[x] + ", ")
            parents = parents[:-2]
        else:
            parents = "brak danych"

        if person["relations"]["childrens"] != []:
            childrens = ""
            for x in person["relations"]["childrens"]:
                childrens += (Ids[x] + ", ")
            childrens = childrens[:-2]
        else:
            childrens = "brak danych"

        if person["relations"]["siblings"] != []:
            siblings = ""
            for x in person["relations"]["siblings"]:
                siblings += (Ids[x] + ", ")
            siblings = siblings[:-2]
        else:
            siblings = "brak danych"

        if person["relations"]["partner"] != []:
            partner = ""
            for x in person["relations"]["partner"]:
                partner += (Ids[x] + ", ")
            partner = partner[:-2]
        else:
            partner = "brak danych"


        pdf.set_xy(10,130)
        pdf.image(image,50,20,w=120,h=120)
        
        pdf.set_xy(10,170)
        pdf.cell(10,20,f"Imie: {name}")
        
        pdf.set_xy(10,180)
        pdf.cell(10,20,f"Nazwisko: {surname}")
        
        pdf.set_xy(10,190)
        pdf.cell(10,20,f"Rok urodzenia: {bornYear}")
        
        pdf.set_xy(10,200)
        pdf.cell(10,20,f"Rodzice: {parents}")

        pdf.set_xy(10,210)
        pdf.cell(10,20,f"Dzieci: {childrens}")

        pdf.set_xy(10,220)
        pdf.cell(10,20,f"Rodzenstwo: {siblings}")

        pdf.set_xy(10,230)
        pdf.cell(10,20,f"Partner: {partner}")



    def exportToPDF(self):
        pdf = FPDF('P', 'mm', 'letter')
        pdf.add_page()
        pdf.set_font('times',size=40)
        pdf.set_xy(70,100)
        pdf.cell(20,30, 'Your Family')

        pdf.set_font('times',size=20)
        with open(self.jsonfile, "r") as file:
            data = json.load(file)
            ID = {}
            for person in data:
                ID[person["id"]] = (person["name"] + " " + person["surname"])

            for person in data:
                pdf.add_page()
                self.addPersonPDF(person,pdf,ID)

        pdf.output('family.pdf')

    def exportToHTML(self):
        template = Template('''
        <html>
        <head>
            <style>
                .element {
                    position: absolute;
                }
            </style>
        </head>
        <body>
            {% for item in data %}
            <div class="element" style="left: {{ item.x }}px; top: {{ item.y }}px;">
                <img src="{{ item.img }}" alt="{{ item.name }}" width = "100" height = "100">
                <p>{{ item.name }} {{ item.surname}}</p>
            </div>
            {% endfor %}
        </body>
        </html>
        ''')
        with open(self.jsonfile, "r") as file:
            data = json.load(file)
        html = template.render(data=data)

        with open("family.html", "w") as file:
            file.write(html)


    def addPicture(self):
        #image = Tk()
        #image.destroy()
        #root.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        #print(root.filename)
        #filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        filename = filedialog.askopenfilename()
        self.lastCurrentPerson.img = filename

    def deletePerson(self):
        # for person in self.lastCurrentPerson.relations.values():
        # print(person.relations)
        # if person != []:
        # list(person.relations.values()).remove(self.lastCurrentPerson)
        for person in list(self.persons.values()):
            for v in person.relations.values():
                if self.lastCurrentPerson.id in v:
                    v.remove(self.lastCurrentPerson.id)

            if person.id > self.lastCurrentPerson.id:
                person.id -= 1
        u = self.lastCurrentPerson.id
        for i in range(self.lastCurrentPerson.id,len(self.persons)-1):
            self.persons[i] = copy.copy(self.persons[i+1])
            u = i+1
        
        del self.persons[u]
        #del self.persons[self.lastCurrentPerson.id]
        self.curId -= 1

    def saveToJSON(self):
        # for person in self.persons:
        #   person.toJSON("persons.json")
        with open(self.jsonfile, 'w+') as file:
            file.write(json.dumps([person.__dict__ for person in list(self.persons.values())], indent=3))
        #file.close()


    def loadFromJSON(self):
        with open(self.jsonfile, "r") as file:
            data = json.load(file)
        self.persons = {id: Person(**person) for id, person in enumerate(data)}
        self.curId = len(self.persons)

        #file.close()

    def main(self):
        pygame.display.set_caption('Family Tree')
        # clock = pygame.time.Clock()
        run = True
        root = None  # główne okno tkintera

        while run:

            self.win.fill((238, 242, 246))
            events = pygame.event.get()
            # clock.tick(60)
            if len(self.persons) == 0:
                self.lx = 0
                self.ly = 0
            # odpowiedzialna za rysowanie osób
            if self.relationPerson:
                print(self.relationPerson.name, self.newRelation)

            for person in list((self.persons).values()):

                for indx in person.relations["siblings"]:
                    pygame.draw.line(self.win, (100, 100, 100), (self.persons[indx].x, self.persons[indx].y),
                                     (person.x, person.y), 5)

                for indx in person.relations["childrens"]:
                    #if person.relations["partner"] != []:
                    #    pygame.draw.line(self.win, (0, 0, 0), (self.persons[indx].x, self.persons[indx].y), (
                    #        (person.x + self.persons[person.relations["partner"][0]].x) // 2,
                    #        (person.y + self.persons[person.relations["partner"][0]].y) // 2), 5)
                    #else:
                        #pygame.draw.line(self.win, (0, 0, 0), (self.persons[indx].x, self.persons[indx].y),
                                         #(person.x, person.y), 5)

                    pygame.draw.line(self.win, (100, 100, 100), (self.persons[indx].x, self.persons[indx].y),
                                         (person.x, person.y), 5)

                for indx in person.relations["partner"]:
                    pygame.draw.line(self.win, (100, 100, 100), (self.persons[indx].x, self.persons[indx].y),
                                     (person.x, person.y), 5)

            for person in list((self.persons).values()):

                # person.r = 80 + (len(self.persons)*person.relationsCount - self.relationCount)

                x, y = pygame.mouse.get_pos()

                if x > 0.99 * WIN_WIDTH:
                    person.x -= 1
                    self.lx -= 1
                    #self.lx -= 1 / (2 * len(self.persons))

                elif x < 0.01 * WIN_WIDTH:
                    person.x += 1
                    #self.lx += 1 / (2 * len(self.persons))
                    self.lx += 1

                if y > 0.99 * WIN_HEIGHT:
                    person.y -= 1
                    #self.ly -= 1 / (2 * len(self.persons))
                    self.ly -= 1

                elif y < 0.01 * WIN_HEIGHT:
                    person.y += 1
                    #self.ly += 1 / (2 * len(self.persons))
                    self.ly += 1
                

                if self.newRelation == 1 and person.isclickedL:
                    self.newRelation = 0
                    print(1)
                    if person.id not in self.relationPerson.relations["parents"] and person.id not in self.relationPerson.relations["childrens"] and person.id not in self.relationPerson.relations["siblings"] and person.id not in self.relationPerson.relations["partner"]:
                        self.relationPerson.relations["parents"].append(person.id)
                        person.relations["childrens"].append(self.relationPerson.id)
                    self.relationPerson = None
                    # self.relationCount += 1
                    # person.relationsCount += 1
                    # self.relationCount += 2

                elif self.newRelation == 2 and person.isclickedL:
                    self.newRelation = 0
                    print(2)
                    if person.id not in self.relationPerson.relations["parents"] and person.id not in self.relationPerson.relations["childrens"] and person.id not in self.relationPerson.relations["siblings"] and person.id not in self.relationPerson.relations["partner"]:
                        self.relationPerson.relations["siblings"].append(person.id)
                        person.relations["siblings"].append(self.relationPerson.id)
                    self.relationPerson = None
                    # self.relationCount += 1
                    # person.relationsCount += 1
                    # self.relationCount += 2

                elif self.newRelation == 3 and person.isclickedL:
                    self.newRelation = 0
                    print(3)
                    if person.id not in self.relationPerson.relations["parents"] and person.id not in self.relationPerson.relations["childrens"] and person.id not in self.relationPerson.relations["siblings"] and person.id not in self.relationPerson.relations["partner"]:
                        self.relationPerson.relations["childrens"].append(person.id)
                        person.relations["parents"].append(self.relationPerson.id)
                    self.relationPerson = None
                    # self.relationCount += 1
                    # person.relationsCount += 1
                    # self.relationCount += 2

                elif self.newRelation == 4 and person.isclickedL:
                    self.newRelation = 0
                    print(4)
                    if person.id not in self.relationPerson.relations["parents"] and person.id not in self.relationPerson.relations["childrens"] and person.id not in self.relationPerson.relations["siblings"] and person.id not in self.relationPerson.relations["partner"]:
                        self.relationPerson.relations["partner"].append(person.id)
                        person.relations["partner"].append(self.relationPerson.id)
                        #
                        #person.relations["childrens"], self.relationPerson.relations["childrens"] = person.relations[
                        #                                                                            "childrens"] + \
                        #                                                                        self.relationPerson.relations[
                        #                                                                            "childrens"], \
                        #                                                                        person.relations[
                        #                                                                            "childrens"] + \
                        #                                                                        self.relationPerson.relations[
                        #                                                                             "childrens"]
                    self.relationPerson = None
                    # self.relationCount += 1
                    # person.relationsCount += 1
                    # self.relationCount += 2

                if person.isclickedL and self.currentPerson is None:
                    self.currentPerson = person
                    if not self.changing:
                        self.lastCurrentPerson = person
                    person.current = True

                if person is self.currentPerson and not person.current:
                    self.currentPerson = None

                if person.isclickedR:
                    self.currentPerson = person
                    if not self.changing:
                        self.lastCurrentPerson = person
                    self.personList = PersonList(x, y, [ButtonList(x, y, "Edit", self.edit),
                                                        ButtonList(x, y + 50, "Info", self.info),
                                                        ButtonList(x, y + 100, " " * 18 + "Add" + " " * 18 + ">",
                                                                   command2=self.add),
                                                        ButtonList(x, y + 150, " " * 15 + "Connect" + " " * 15 + ">",
                                                                   command2=self.connect),
                                                        ButtonList(x, y + 200, "Delete Person", self.deletePerson)])

                # stary zapis relacji
                """
                for relation in list(person.relations.values()):    
                    for human in relation:
                        pygame.draw.line(self.win,(0,0,0),(human.x,human.y),(person.x,person.y))
                """
                # nowy zapis relacji

                # for human in person.relations["parents"]:
                #    pygame.draw.line(self.win,(0,0,0),(human.x,human.y),(person.x,person.y))

                

                person.draw(self.win)

            if self.newRelation != 0:
                x, y = pygame.mouse.get_pos()
                pygame.draw.line(self.win, (0, 0, 0), (x, y), (self.relationPerson.x, self.relationPerson.y), 5)

            if self.personList != None:
                self.personList.draw(self.win)

            if self.list2 != None:
                self.list2.draw(self.win)

            for event in events:

                # odpowiada za zamknięcie aplikacji
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 3:
                        x, y = pygame.mouse.get_pos()
                        self.personList = PersonList(x, y, [ButtonList(x, y, "Add Person", self.addPerson),
                                                            ButtonList(x, y + 50, "Back to start", self.backToStart),
                                                            ButtonList(x, y + 100, "New starting point",
                                                                       self.newStartingPoint),
                                                            ButtonList(x, y + 150, "ExportToPDF", self.exportToPDF),
                                                            ButtonList(x, y + 200, "ExportToHTML", self.exportToHTML)])
                        self.list2 = None
                        self.newRelation = False

                    if event.button == 1:
                        self.personList = None
                        self.list2 = None

            # rysuje listę rozwijaną
            logout.draw(self.win)
            if logout.isclicked:
                self.saveToJSON()

            # formularz
            """
            if self.form:
                x,y = pygame.mouse.get_pos()
                root = Tk()
                root.geometry("500x500")
                firstname_text = Label(text="Firstname ", )
                firstname_text.place(x=15, y=30)
                firstname = StringVar()
                firstname_entry = Entry(textvariable=firstname, width="30")
                firstname_entry.place(x=80, y=30)
                surnname_text = Label(text="Surnname  ", )
                surnname_text.place(x=15, y=60)
                surnname = StringVar()
                surnname_entry = Entry(textvariable=surnname, width="30")
                surnname_entry.place(x=80, y=60)
                bornyear_text = Label(text="Born Year ", )
                bornyear_text.place(x=15, y=90)
                bornyear = StringVar()
                bornyear_entry = Entry(textvariable=bornyear, width="30")
                bornyear_entry.place(x=80, y=90)
                AddImg = Button(text="Add Picture", width="30", height="2", command=partial(self.addPicture))
                AddImg.place(x=140, y=180)
                save = Button(text="Save", width="30", height="2", command=partial(self.changeInformation, firstname, surnname, bornyear,root)) 
                save.place(x=140, y=230)
                """
            pygame.display.update()

            # if root:
            #    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    loginForm = LoginForm(root)
    root.mainloop()