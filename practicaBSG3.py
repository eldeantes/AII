from bs4 import BeautifulSoup
import urllib.request, re, sqlite3
from tkinter import simpledialog
from tkinter import messagebox
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

def listar_bd_orden_pu():
    conn = sqlite3.connect('ulabox.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT DENOMINACION, PRECIOKGL FROM PRODUCTO ORDER BY PRECIOKGL ASC")
    imprimir_etiqueta_orden_pu(cursor)
    conn.close()

def imprimir_etiqueta_orden_pu(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,'PRODUCTO: '+row[0])
        lb.insert(END,'PRECIO POR KG O L: '+row[1])
        lb.insert(END,'--------------------------------------------')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)    

def buscar_bd_marca():
    def listar_busqueda(event):
        conn = sqlite3.connect('ulabox.db')
        conn.text_factory = str
        s = "%"+w.get()+"%" 
        cursor = conn.execute("""SELECT DENOMINACION, PRECIO FROM PRODUCTO WHERE MARCA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_por_marca(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Buscar productos por marca:")
    lb.pack(side = LEFT)
    conn = sqlite3.connect('ulabox.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT DISTINCT MARCA FROM PRODUCTO")

    values =[]
    for row in cursor:
        values.append(row[0])

    w = Spinbox(v, values=values)
    w.bind("<Return>", listar_busqueda)
    w.pack(side = LEFT)


    def imprimir_por_marca(cursor):
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        for row in cursor:
            nombre=row[0]
            lb.insert(END,"\n")
            s = 'PRODUCTO: '+ str(nombre)
            lb.insert(END,s)

            precio=row[0]
            lb.insert(END,"\n")
            s = 'PRECIO: '+ str(precio)
            lb.insert(END,s)
            
            lb.insert(END,'--------------------------------------------')
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)

def buscar_rebajas():
    conn = sqlite3.connect('ulabox.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT DENOMINACION, OLDPRECIO, PRECIO FROM PRODUCTO WHERE OLDPRECIO!=NULL""") # Si es != null es que tiene rebaja
    imprimir_rebajas(cursor)
    conn.close()

    def imprimir_rebajas(cursor):
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        for row in cursor:
            nombre=row[0]
            lb.insert(END,"\n")
            s = 'PRODUCTO: '+ str(nombre)
            lb.insert(END,s)

            precioAntiguo=row[1]
            lb.insert(END,"\n")
            s = 'PRECIO ANTIGUO: '+ str(precioAntiguo)
            lb.insert(END,s)

            precioFinal=row[2]
            lb.insert(END,"\n")
            s = 'PRECIO: '+ str(precioFinal)
            lb.insert(END,s)
            
            lb.insert(END,'--------------------------------------------')
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)

def ventana_principal():
    root = Tk()

    frame = Frame(root)
    frame.pack()

    button1 = Button(frame, text="Almacenar Productos", command=almacenar_bd)
    button1.pack(side=LEFT)

    button2 = Button(frame, text="Ordenar por Precio Unitario", command=listar_bd_orden_pu)
    button2.pack(side=LEFT)

    button3 = Button(frame, text="Mostrar Marca", command=buscar_bd_marca)
    button3.pack(side=LEFT)

    button4 = Button(frame, text="Buscar Rebajas", command=buscar_rebajas)
    button4.pack(side=LEFT)

    root.mainloop()

if __name__ == "__main__":
    ventana_principal()

