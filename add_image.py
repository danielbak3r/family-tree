import os
import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageDraw

pygame.font.init()

LENGTH = 200
WIN_WIDTH = 8.5 * LENGTH
WIN_HEIGHT = 4.5 * LENGTH
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

FONT1 = pygame.font.SysFont('comicsans', 14)


class MainMenu:
    def __init__(self) -> None:
        self.x = 50
        self.y = 50
        self.width = 500
        self.heigth = 100
        self.color = (100, 60, 50)
        self.button = 50
        self.buttonColor = (12, 124, 20)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.heigth))  # rysuje główne menu
        pygame.draw.rect(win, self.buttonColor, (
        self.x + self.button, self.y + (self.heigth - self.button) // 2, self.button,
        self.button))  # rysuje pierwszy przycisk
        pygame.draw.rect(win, self.buttonColor, (
        self.x + 3 * self.button, self.y + (self.heigth - self.button) // 2, self.button,
        self.button))  # rysuje drugi przycisk
        pygame.draw.rect(win, self.buttonColor, (
        self.x + 5 * self.button, self.y + (self.heigth - self.button) // 2, self.button,
        self.button))  # rysuje trzeci przycisk


menu = MainMenu()  # tworzy obiekt klasy MainMenu


# tworzy listę rozwijaną osoby

class PersonList:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.length = 300
        self.height = 400
        self.color = (240, 240, 240)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.length, self.height))


# klasa przycisk

"""
class Button:
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))
		return action
"""


class Person:
    def __init__(self, x=300, y=300, r=100, name="Adam", surname="Kowalski", bornYear=2000, img=pygame.image.load(os.path.join("C:/Users/t33lx/PycharmProjects/pythonProject/venv/images/invisible-png.png"))) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.color = (7, 56, 99)
        #self.color = "C:/Users/t33lx/OneDrive/Desktop/img2 - moon.jpg"
        self.bool = False
        self.relations = set()
        self.name = name
        self.surname = surname
        self.bornYear = bornYear
        self.img = pygame.transform.scale(img, (300, 300))
        self.parents = []
        self.children = []
        self.siblings = []
        self.partner = None

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)  # rysuje osobę
        for relation in list(self.relations):
            pygame.draw.line(win, self.color, (self.x, self.y),
                             (relation.x, relation.y))  # rysuje relacje między osobami
        s = FONT1.render(str(self.name) + " " + str(self.surname) + " " + "(" + str(self.bornYear) + ")", 1,
                         (0, 255, 255))


        #x = self.r
        #img_cropped = self.img.crop((x, 0, x + 300, 300))

        DEFAULT_IMAGE_SIZE = (300, 300)
        self.img = pygame.transform.scale(self.img, DEFAULT_IMAGE_SIZE)
        win.blit(self.img, (self.x - self.r,self.y - self.r))
        win.blit(s, (
        self.x - s.get_width() // 2, (self.y - s.get_height() // 2) + 50))  # wyświetla imię, nazwisko i rok urodzenia

    def options(self, win):  # w planie będzie tworzyło listę rozwijaną
        pass




# embed = tk.Frame(root, width = 500, height = 500) #creates embed frame for pygame window
# embed.grid(columnspan = (600), rowspan = 500) # Adds grid
# embed.pack(side = LEFT) #packs window to the left
# buttonwin = tk.Frame(root, width = 75, height = 500)
# buttonwin.pack(side = LEFT)
# os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
# os.environ['SDL_VIDEODRIVER'] = 'windib'

class Game:
    def __init__(self) -> None:
        self.persons = []
        self.button3 = False
        self.currentPerson = None

    def changeInformation(self, name, surname, bornyear):
        self.currentPerson.name = name.get()  # zmienia imie po edycji w formularzu
        self.currentPerson.surname = surname.get()
        self.currentPerson.bornYear = bornyear.get()

    def addPerson(self, name="Adam", surname="Kowalski", bornYear=2000):
        self.persons.append(Person(name=name, surname=surname, bornYear=bornYear))  # dodaje osobę do listy osób

    def AddParents(self, MothersName, FathersName, surname, FatherBornYear, MothersBornYear):
        print("X")

    def AddChild(self, name, surname, bornYear):
        print("X")

    def AddPicture(self):
        image = Tk()
        image.destroy()
        image.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        print(image.filename)
        imgloaded = pygame.image.load(image.filename)

        self.currentPerson.img = imgloaded
        #pygame.display.update()

    def main(self, win):
        clock = pygame.time.Clock()
        run = True
        root = None  # główne okno tkintera
        relationBool = False  # służy przy dodawaniu relacji (button 2)
        tempSet = set()  # do niego dodawane są osoby tymczasowo osoby które są w relacji
        personList = None
        while run:

            win.fill((255, 255, 200))
            events = pygame.event.get()
            clock.tick(30)
            self.button3 = False
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    run = False
                    pygame.quit()
                    quit()
                # odpowiada za zamknięcie aplikacji

                if event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()
                    p = False
                    for person in self.persons:
                        if ((x - person.x) ** 2 + (y - person.y) ** 2) ** 0.5 <= person.r:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            p = True

                    if not p:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                # zmienia kursor po najechaniu na osobę

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for person in self.persons:
                        if ((x - person.x) ** 2 + (y - person.y) ** 2) ** 0.5 <= person.r and not relationBool:
                            if event.button == 1:
                                person.bool = True
                                self.currentPerson = person
                            elif event.button == 3:
                                personList = PersonList(x, y)
                            # tworzy listę dla osoby


                        # po kliknięciu na osobę zmienia ją na obecną i tworzy listę rozwijaną

                        elif ((x - person.x) ** 2 + (y - person.y) ** 2) ** 0.5 <= person.r and relationBool:
                            tempSet.add(person)
                        # służy do dodawania relacji między osobami
                        if event.button == 1 and personList != None:
                            personList = None
                    # usuwa listę dla osoby

                if event.type == pygame.MOUSEBUTTONUP:
                    for person in self.persons:
                        person.bool = False

                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if x in range(menu.x, menu.x + menu.width) and y in range(menu.y, menu.y + menu.heigth):
                        if x in range(menu.x + menu.button, menu.x + 2 * menu.button) and y in range(
                                menu.y + (menu.heigth - menu.button) // 2,
                                menu.y + (menu.heigth - menu.button) // 2 + menu.button):
                            self.addPerson()
                        # pierwszy przycisk tworzy nową osobę
                        elif x in range(menu.x + 3 * menu.button, menu.x + 4 * menu.button) and y in range(
                                menu.y + (menu.heigth - menu.button) // 2,
                                menu.y + (menu.heigth - menu.button) // 2 + menu.button):
                            relationBool = True
                        # drugi przycisk odpowiedzialny za robienie relacji

                        elif x in range(menu.x + 5 * menu.button, menu.x + 6 * menu.button) and y in range(
                                menu.y + (menu.heigth - menu.button) // 2,
                                menu.y + (menu.heigth - menu.button) // 2 + menu.button):
                            self.button3 = True
                            if root:
                                root.quit()
                        # trzeci przycisk uruchamia formularz

                if event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()
                    if x in range(menu.x, menu.x + menu.width) and y in range(menu.y, menu.y + menu.heigth):
                        if any([x in range(menu.x + menu.button, menu.x + 2 * menu.button),
                                x in range(menu.x + 3 * menu.button, menu.x + 4 * menu.button),
                                x in range(menu.x + 5 * menu.button, menu.x + 6 * menu.button)]) and y in range(
                                menu.y + (menu.heigth - menu.button) // 2,
                                menu.y + (menu.heigth - menu.button) // 2 + menu.button):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                # zmienia kursor myszy po najechaniu na obiekt klasy MainMenu

            menu.draw(win)
            if len(list(tempSet)) >= 2:
                list(tempSet)[0].relations.add(list(tempSet)[1])
                list(tempSet)[1].relations.add(list(tempSet)[0])
                tempSet.clear()
                relationBool = False
            # tworzy relacje między osobami

            for person in self.persons:
                x, y = pygame.mouse.get_pos()
                if person.bool:
                    person.x = x
                    person.y = y
                if person is self.currentPerson:
                    person.color = (107, 56, 99)
                else:
                    person.color = (7, 56, 99)
                person.draw(win)
            # odpowiedzialna za rysowanie osób

            if self.currentPerson == None and len(self.persons) == 1:
                self.currentPerson = self.persons[0]
            # ustawia pierwszą osobę jako obecną

            if personList != None:
                personList.draw(win)
            # rysuje listę rozwijaną

            if self.button3:
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

                AddParents = Button(text="Add Parents", width="30", height="2", command=partial(self.AddParents))
                AddParents.place(x=15, y=120)

                AddChild = Button(text="Add Child", width="30", height="2", command=partial(self.AddParents))
                AddChild.place(x=260, y=120)

                AddImg = Button(text="Add Picture", width="30", height="2", command=partial(self.AddPicture))
                AddImg.place(x=140, y=180)

                register = Button(text="Register", width="30", height="2", command=partial(self.changeInformation, firstname, surnname, bornyear))
                register.place(x=140, y=230)


            # formularz
            pygame.display.update()

            if root:
                root.mainloop()


if __name__ == "__main__":
    game = Game()
    game.main(WIN)
