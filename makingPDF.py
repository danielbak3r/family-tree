from fpdf import FPDF
import json

def addPersonPDF(person,pdf):
    
    image = person["img"]
    name = person["name"]
    surname = person["surname"]
    bornYear = person["bornYear"]

    pdf.set_xy(10,150)
    pdf.image(image,60,20,w=100,h=100)
    pdf.set_xy(10,210)
    pdf.cell(10,20,f"Imie: {name}")
    pdf.set_xy(10,220)
    pdf.cell(10,20,f"Nazwisko: {surname}")
    pdf.set_xy(10,230)
    pdf.cell(10,20,f"Rok urodzenia: {bornYear}")

def exportToPDF():
    pdf = FPDF('P', 'mm', 'letter')


    pdf.add_page()
    pdf.set_font('times',size=40)
    pdf.set_xy(70,100)
    pdf.cell(20,30, 'Your Family')

    pdf.set_font('times',size=20)
    with open("persons.json", "r") as file:
        data = json.load(file)
        for person in data:
            pdf.add_page()
            addPersonPDF(person,pdf)

    pdf.output('pdf_1.pdf')

exportToPDF()
