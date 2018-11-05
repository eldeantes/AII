from bs4 import BeautifulSoup
import urllib.request, re, sqlite3
import tkinter as tk
from tkinter import simpledialog
from tkinter import *



def procesar_pagina(d:str):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, "lxml")
    news = documento.find_all("div", class_="news-summary")

    for n in news:
        print('TÍTULO: '+n.find("div", class_="center-content").h2.a.string+'\n')

        print('ENLACE: '+n.find("div", class_="center-content").h2.a.get("href")+'\n')

        print('AUTOR: '+n.find("div", class_="news-submitted").find_all("a")[1].string+'\n')

        print('HORA PUBLICACIÓN: '+n.find("div", class_="news-submitted").find_all("span", class_="ts visible")[0].string+'\n')
        #print('HORA PUBLICACIÓN: '+str(n.find("div", class_="news-submitted").find_all("span", class_="ts visible")[0])+'\n')

        try:
            print('CONTENIDO: '+n.find("div", class_="news-content").string+'\n\n\n')
        except:
            print('CONTENIDO: '+n.find("div", class_="news-content").find(text=True, recursive=False)+'\n\n\n')


    return documento


def almacenar_bd(numero_paginas):
    conn = sqlite3.connect('test.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS NOTICIAS")   
    conn.execute("""CREATE TABLE NOTICIAS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       TITULO           TEXT    NOT NULL,
       ENLACE           TEXT    NOT NULL,
       AUTOR            TEXT    NOT NULL,
       FECHA            TEXT    NOT NULL,
       CONTENIDO       TEXT    NOT NULL);""")

    for i in range(1,numero_paginas+1):
        documento = procesar_pagina("https://www.meneame.net/?page="+str(i))
        news = documento.find_all("div", class_="center-content")

        for n in news:
            titulo=n.h2.a.string

            enlace=n.h2.a.get("href")

            autor=n.find("div", class_="news-submitted").find_all("a")[1].string

            hora=n.find("div", class_="news-submitted").find_all("span", class_="ts visible")[0].string

            try:
                contenido=''+n.find("div", class_="news-content").string
            except:
                contenido=''+n.find("div", class_="news-content").find(text=True, recursive=False)

            conn.execute("""INSERT INTO NOTICIAS (TITULO, ENLACE, AUTOR, FECHA, CONTENIDO) VALUES (?,?,?,?,?)""",(titulo,enlace,autor,hora,contenido))
            conn.commit()

    cursor = conn.execute("SELECT COUNT(*) FROM NOTICIAS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()


def listar_bd():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO, ENLACE, AUTOR, FECHA, CONTENIDO FROM NOTICIAS")
    imprimir_etiqueta(cursor)
    conn.close()
    
def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,row[3])
        lb.insert(END,row[4])
        lb.insert(END,'--------------------------------------------')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)


def buscar_bd_noticia():
    def listar_busqueda(event):
        conn = sqlite3.connect('test.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO, ENLACE, AUTOR, FECHA, CONTENIDO  FROM NOTICIAS WHERE CONTENIDO LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Buscar noticia:")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)

def buscar_bd_autor():
    def listar_busqueda(event):
        conn = sqlite3.connect('test.db')
        conn.text_factory = str
        s = "%"+w.get()+"%" 
        cursor = conn.execute("""SELECT TITULO, ENLACE, AUTOR, FECHA, CONTENIDO  FROM NOTICIAS WHERE AUTOR LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Buscar noticias de autor:")
    lb.pack(side = LEFT)
    conn = sqlite3.connect('test.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT AUTOR FROM NOTICIAS")

    values =[]
    for row in cursor:
        values.append(row[0])

    w = Spinbox(v, values=values)
    w.bind("<Return>", listar_busqueda)
    w.pack(side = LEFT)

def hello():
    print("hola")

def almacenar_bd_menu():
    almacenar_bd(simpledialog.askinteger('Cargar resultados', 'Número de páginas',minvalue=3))

root = tk.Tk()
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Cargar", command=almacenar_bd_menu)
filemenu.add_command(label="Mostrar", command=listar_bd)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Datos", menu=filemenu)

editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Noticia", command=buscar_bd_noticia)
editmenu.add_command(label="Autor", command=buscar_bd_autor)
editmenu.add_command(label="Fecha", command=hello)
menubar.add_cascade(label="Buscar", menu=editmenu)


root.config(menu=menubar)
root.mainloop()


