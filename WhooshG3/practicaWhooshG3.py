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

def imprime_posts():
    fichero = urllib.request.urlopen("https://foros.derecho.com/foro/20-Derecho-Civil-General")
    documento = BeautifulSoup(fichero, "lxml")
    threads = documento.find_all("li", class_="threadbit")
    if not os.path.exists("Threads"):
        os.mkdir("Threads")
    else:
        shutil.rmtree("Threads")
        os.mkdir("Threads")
    #Por cada post: Título, link al tema, autor, fecha, número de respuestas, y número de visitas
    i=1
    for thread in threads:
        title = thread.find_all("a", class_="title")[0].string
        link = "https://foros.derecho.com/" + thread.find_all("a", class_="title")[0].get("href")
        autor = thread.find_all("a", class_="username understate")[0].string

        span_fecha = thread.find_all("div", class_="author")[0].span
        regex = '\\d{2}/\\d{2}/\\d{4}\\s\\d{2}:\\d{2}'
        m = re.search(regex, str(span_fecha))
        fecha = m.group(0)

        respuestas_visitas = thread.find_all("ul", class_="threadstats")[0]
        respuestas = respuestas_visitas.find_all("li")[0].a.string

        visitas = respuestas_visitas.find_all("li")[1].string.split("Visitas: ",1)[1]

        with open('Threads/'+str(i)+'.txt', 'w') as f:
            f.write(title+'\n')
            f.write(link+'\n')
            f.write(autor+'\n')
            f.write(fecha+'\n')
            f.write(respuestas+'\n')
            f.write(visitas+'\n')
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
        lb.insert(END, 'AUTOR: '+row['autor'])
        lb.insert(END, 'FECHA: '+row['fecha'].strftime('%d/%m/%Y %H:%M'))
        lb.insert(END, '--------------------------------------------')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def buscar_titulo_enlace(dirindex):
    query = simpledialog.askstring(
        'Buscar por título', 'Introduzca una palabra que esté en el título y la url del tema')
    ix = open_dir(dirindex)

    with ix.searcher() as searcher:
        myquery = MultifieldParser(["titulo","link"], ix.schema).parse(query)
        results = searcher.search(myquery)
        imprimir_resultados(results)


def buscar_fecha(dirindex):
    query = simpledialog.askstring("Buscar por fecha","Introduzca la fecha (AAAAMMDDHHmm): ")
    ix=open_dir(dirindex)
    try:
        with ix.searcher() as searcher:
            query = QueryParser("fecha", ix.schema).parse(query)
            results = searcher.search(query)
            imprimir_resultados(results)
    except:
        print ("Error: Formato de fecha incorrecto")


def buscar_autor(dirindex):
    def listar_busqueda(event):
        query = w.get()
        ix = open_dir(dirindex)

        with ix.searcher() as searcher:
            myquery = QueryParser("autor", ix.schema).parse(query)
            results = searcher.search(myquery)
            imprimir_resultados(results)

    query = "admin"
    ix = open_dir(dirindex)

    with ix.searcher() as searcher:
        myquery = QueryParser("autor", ix.schema,
                            group=qparser.NotGroup).parse(query)
        results = searcher.search(myquery)
        values =[]
        for r in results:
            values.append(r['autor'])

    v = Toplevel()
    lb = Label(v, text="Buscar temas por autor:")
    lb.pack(side = LEFT)



    w = Spinbox(v, values=values)
    w.bind("<Return>", listar_busqueda)
    w.pack(side = LEFT)


def get_schema():
    return Schema(titulo=TEXT(stored=True), link=TEXT(stored=True), autor=TEXT(stored=True), fecha=DATETIME(stored=True), respuestas=TEXT(stored=True), visitas=TEXT(stored=True), nombrefichero=ID(stored=True))


def add_doc(writer, path, docname):
    try:
        fileobj = open(path+'/'+docname, "rb")
        title = fileobj.readline().strip().decode()
        link = fileobj.readline().strip().decode()
        autor = fileobj.readline().strip().decode()
        fecha = fileobj.readline().strip().decode()
        fecha = datetime.strptime(fecha, '%d/%m/%Y %H:%M')
        respuestas = fileobj.readline().strip().decode()
        visitas = fileobj.read().decode()
        fileobj.close()
        writer.add_document(titulo=title, link=link, autor=autor, fecha=fecha,
                            respuestas=respuestas, visitas=visitas, nombrefichero=docname)
        print ("Creado indice para fichero " + docname)
    except:
        print ("Error: No se ha podido a�adir el documento "+path+'/'+docname)


def indexar():
    imprime_posts()
    crea_index("Threads", "Index")


def buscar_titulo_enlace_menu():
    buscar_titulo_enlace("Index")


def buscar_fecha_menu():
    buscar_fecha("Index")

def buscar_autor_menu():
    buscar_autor("Index")


if __name__ == '__main__':
    root = Tk()
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Cargar", command=indexar)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(label="Datos", menu=filemenu)

    editmenu = Menu(menubar, tearoff=0)

    editmenu.add_command(label="Titulo y enlace", command=buscar_titulo_enlace_menu)
    editmenu.add_command(label="Fecha", command=buscar_fecha_menu)
    editmenu.add_command(label="Autor", command=buscar_autor_menu)
    menubar.add_cascade(label="Buscar", menu=editmenu)

    root.config(menu=menubar)
    root.mainloop()