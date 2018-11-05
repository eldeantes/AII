from bs4 import BeautifulSoup
import urllib.request, re, sqlite3
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import *

def procesar_pagina(d:str):
    fichero = urllib.request.urlopen(d)
    documento = BeautifulSoup(fichero, "lxml")
    productos = documento.find_all("article", class_="product-item--grid")

    for n in productos:
        print("DENOMINACIÓN:  " + n.find("h3", class_="product-item__name").find_all("a")[0].string+'\n')
        print("MARCA:  "+ n.find("h4", class_="product-item__brand").find_all("a")[0].string+'\n')
        print("PRECIO POR KILO/LITRO:   "+re.sub("[^0-9,]", "", n.find("small", class_="product-item__ppu").string).replace(",",".")+'\n')
        if(len(n.find("span", class_="product-grid-footer__price").contents)==2):
            print("PRECIO ANTIGUO:  "+n.find("span", class_="product-grid-footer__price").find_all("del")[0].string+'\n')
        print("PRECIO:  "+n['data-price']+'\n')
        print("----------------------------------------------------------------\n\n\n")

    return documento


def almacenar_bd():
    conn = sqlite3.connect('ulabox.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS PRODUCTO")   
    conn.execute("""CREATE TABLE PRODUCTO
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       DENOMINACION     TEXT    NOT NULL,
       MARCA            TEXT    NOT NULL,
       PRECIOKGL        NUMBER    NOT NULL,
       OLDPRECIO        TEXT    ,
       PRECIO           TEXT    NOT NULL);""")

   
    documento = procesar_pagina("https://www.ulabox.com/campaign/productos-sin-gluten#gref")
    productos = documento.find_all("article", class_="product-item--grid")

    for n in productos:
        denominacion=n.find("h3", class_="product-item__name").find_all("a")[0].string

        marca=n.find("h4", class_="product-item__brand").find_all("a")[0].string

        precio=n['data-price']

        preciokgl=float(re.sub("[^0-9,]", "", n.find("small", class_="product-item__ppu").string).replace(",","."))

        if(len(n.find("span", class_="product-grid-footer__price").contents)==2):
            oldprecio = n.find("span", class_="product-grid-footer__price").find_all("del")[0].string
        else:
            oldprecio = ''

        conn.execute("""INSERT INTO PRODUCTO (DENOMINACION, MARCA, PRECIOKGL, OLDPRECIO, PRECIO) VALUES (?,?,?,?,?)""",(denominacion,marca,preciokgl,oldprecio,precio))
        conn.commit()

    cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTO")
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
        lb.insert(END,'PRECIO POR KG O L: '+str(row[1]))
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

            precio=row[1]
            lb.insert(END,"\n")
            s = 'PRECIO: '+ str(precio)
            lb.insert(END,s)
            
            lb.insert(END,'--------------------------------------------')
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)

def buscar_rebajas():
    conn = sqlite3.connect('ulabox.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT DENOMINACION, OLDPRECIO, PRECIO FROM PRODUCTO WHERE OLDPRECIO!=''""") # Si es != null es que tiene rebaja
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

