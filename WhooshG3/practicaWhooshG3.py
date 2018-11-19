#encoding:latin-1
import os, re, shutil, urllib.request
from datetime import datetime
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from bs4 import BeautifulSoup


##############################Método para crear los ficheros para su búsqueda

def imprime_eventos():
    fichero = urllib.request.urlopen("https://foros.derecho.com/foro/20-Derecho-Civil-General")
    documento = BeautifulSoup(fichero, "lxml")
    eventos = documento.find_all("li", class_="threadbit")
    if not os.path.exists("Eventos"):
        os.mkdir("Eventos")
    else:
        shutil.rmtree("Eventos")
        os.mkdir("Eventos")
    #Por cada post: Título, link al tema, autor, fecha, número de respuestas, y número de visitas
    i=1
    for evento in eventos:
        titulo = ""#TODO
        descripcion = "" #TODO
        categoria = ""#TODO
        fechaInicio = ""#TODO
        fechaFin= ""#TODO

        with open('Eventos/'+str(i)+'.txt', 'w') as f:
            f.write(titulo+'\n')
            f.write(descripcion+'\n')
            f.write(categoria+'\n')
            f.write(fechaInicio+'\n')
            f.write(fechaFin+'\n')
        i=i+1

##############################################################################


#Crea un indice desde los documentos contenidos en dirdocs
#El indice lo crea en un directorio (dirindex)
def crea_index(dirdocs, dirindex):
    if not os.path.exists(dirdocs):
        print ("Error: no existe el directorio de documentos " + dirdocs)
    else:
        if not os.path.exists(dirindex):
            os.mkdir(dirindex)
    if not len(os.listdir(dirindex)) == 0:
        sn = messagebox.askyesno(
            "Indexar", "Indice no vacio. Desea reindexar?")
    else:
        sn = True

    i = 0
    if sn:
            ix = create_in(dirindex, schema=get_schema())
            writer = ix.writer()
            for docname in os.listdir(dirdocs):
                if not os.path.isdir(dirdocs+docname):
                    add_doc(writer, dirdocs, docname)
                    i += 1
            writer.commit()
    messagebox.showinfo("Fin de indexado",
                        "Se han indexado "+str(i) + " nuevos posts")


def imprimir_resultados(results):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in results:
        lb.insert(END, 'TITULO: '+row['titulo'])
        lb.insert(END, 'FECHA DE INICIO: '+row['fechaInicio'].strftime('%d/%m/%Y %H:%M'))
        lb.insert(END, 'FECHA DE FIN: '+row['fechaFin'].strftime('%d/%m/%Y %H:%M'))
        lb.insert(END, '--------------------------------------------')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def buscar_titulo_descripcion(dirindex):
    query = simpledialog.askstring(
        'Buscar por título', 'Introduzca una palabra que esté en el título y la descripcion del tema')
    ix = open_dir(dirindex)

    with ix.searcher() as searcher:
        myquery = MultifieldParser(["titulo","descripcion"], ix.schema).parse(query)
        results = searcher.search(myquery)
        imprimir_resultados(results)


def buscar_fecha(dirindex):
    query = simpledialog.askstring("Buscar por fecha","Introduzca la fecha (AAAAMMDD): ")
    ix=open_dir(dirindex)
    try:
        with ix.searcher() as searcher:
            query = QueryParser("fecha", ix.schema).parse(query)
            results = searcher.search(query)
            imprimir_resultados(results)
    except:
        print ("Error: Formato de fecha incorrecto")


def buscar_categoria(dirindex):
    def listar_busqueda(event):
        query = w.get()
        ix = open_dir(dirindex)

        with ix.searcher() as searcher:
            myquery = QueryParser("categoria", ix.schema).parse(query)
            results = searcher.search(myquery)
            imprimir_resultados(results)

    query = "admin"
    ix = open_dir(dirindex)

    with ix.searcher() as searcher:
        myquery = QueryParser("categoria", ix.schema,
                            group=qparser.NotGroup).parse(query)
        results = searcher.search(myquery)
        values =[]
        for r in results:
            values.append(r['categoria'])

    v = Toplevel()
    lb = Label(v, text="Buscar evento por categoria:")
    lb.pack(side = LEFT)



    w = Spinbox(v, values=values)
    w.bind("<Return>", listar_busqueda)
    w.pack(side = LEFT)


def get_schema():
    return Schema(titulo=TEXT(stored=True), descripcion=TEXT(stored=True), categoria=TEXT(stored=True), fechaFin=DATETIME(stored=True),fechaInicio=DATETIME(stored=True),nombrefichero=ID(stored=True))


def add_doc(writer, path, docname):
    try:
        fileobj = open(path+'/'+docname, "rb")
        titulo = fileobj.readline().strip().decode()
        desc = fileobj.readline().strip().decode()
        categoria = fileobj.readline().strip().decode()
        fechaInicio = fileobj.readline().strip().decode()
        fechaInicio = datetime.strptime(fechaInicio, '%d/%m/%Y %H:%M')
        fechaFin = fileobj.readline().strip().decode()
        fechaFin = datetime.strptime(fechaFin, '%d/%m/%Y %H:%M')
        fileobj.close()
        writer.add_document(titulo=titulo, descripcion=desc, categoria=categoria, fechaInicio=fechaInicio,
        fechaFin=fechaFin, nombrefichero=docname)
        print ("Creado indice para fichero " + docname)
    except:
        print ("Error: No se ha podido a�adir el documento "+path+'/'+docname)


def indexar():
    imprime_posts()
    crea_index("Eventos", "Index")


def buscar_titulo_descripcion_menu():
    buscar_titulo_descripcion("Index")


def buscar_fecha_menu():
    buscar_fecha("Index")

def buscar_categoria_menu():
    buscar_categoria("Index")


if __name__ == '__main__':
    root = Tk()
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Cargar", command=indexar)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(label="Datos", menu=filemenu)

    editmenu = Menu(menubar, tearoff=0)

    editmenu.add_command(label="Titulo y descripcion", command=buscar_titulo_descripcion_menu)
    editmenu.add_command(label="Fecha", command=buscar_fecha_menu)
    editmenu.add_command(label="Categoria", command=buscar_categoria_menu)
    menubar.add_cascade(label="Buscar", menu=editmenu)

    root.config(menu=menubar)
    root.mainloop()
