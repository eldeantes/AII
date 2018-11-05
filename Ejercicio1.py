from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3


def ventana_principal():
    top = Tk()
    buscarGoles = Button(top, text="Buscar Goles", command = buscar_goles)
    buscarGoles.pack(side = TOP)
    top.mainloop()
    
def buscar_goles():
    def listar_busqueda():
        conn = sqlite3.connect('as.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        s2 = "%"+en2.get()+"%" 
        s3 = "%"+en3.get()+"%" 
        cursor = conn.execute("""SELECT LINK FROM JORNADAS WHERE JORNADA LIKE ? AND LOCAL LIKE ? AND VISITANTE LIKE ?""",(s,s2,s3)) # al ser de tipo string, el ? le pone comillas simples
        extraer_goles(cursor)
        conn.close()
    
    
    v = Toplevel()
    lb = Label(v, text="Introduzca la jornada: ")
    lb.pack(side = TOP)
    en = Entry(v)
    en.pack(side = TOP)
    
    lb2 = Label(v, text="Introduzca equipo local: ")
    lb2.pack(side = TOP)
    en2 = Entry(v)
    en2.pack(side = TOP)
    
    lb3 = Label(v, text="Introduzca equipo visitante: ")
    lb3.pack(side = TOP)
    en3 = Entry(v)
    #en3.bind("<Return>", listar_busqueda)
    en3.pack(side = TOP)
    
    buscar = Button(v, text="Buscar goles", command=listar_busqueda)
    buscar.pack(side=BOTTOM)
    
def extraer_goles(cursor):
    link = "https://resultados.as.com" + cursor.fetchone()[0]
    f = urllib.request.urlopen(link)
    s = BeautifulSoup(f,"lxml")
    l = s.find_all("div", class_="eventos-directo")
    imprimir_goles(l)


def imprimir_goles(l):
    
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    
    for i in l:
        for a in i.find_all("div", class_= ["txt-evento", "evento-ppal"]):
            if str(a.span["class"])=="['icono-evento', 'as-icon-futbol']":
                jugador = a.strong.string
                minuto = a.p.span.string
                lb.insert(END,"\n")
                s = 'Gol de '+ str(jugador)
                lb.insert(END,s)
                s = 'Minuto: ' + str(minuto)
                lb.insert(END,s)
                #lb.insert(END,"-----------------------------------------------------")
        
    
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)
    v.mainloop()
    
    
    
    
if __name__ == "__main__":
    ventana_principal()
