#encoding:latin-1
import os
from datetime import datetime
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser
from whoosh import qparser
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox


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


def buscar_titulo(dirindex):
    query = simpledialog.askstring(
        'Buscar por título', 'Introduzca el título de los temas a buscar')
    ix = open_dir(dirindex)

    with ix.searcher() as searcher:
        myquery = QueryParser("titulo", ix.schema).parse(query)
        results = searcher.search(myquery)
        imprimir_resultados(results)


'''def apartado_b(dirindex):
    query = input("Introduzca la fecha (AAAAMMDD): ")
    myquery='{'+ query + 'TO]'
    ix=open_dir(dirindex)
    try:
        with ix.searcher() as searcher:
            query = QueryParser("fecha", ix.schema).parse(myquery)
            results = searcher.search(query)
            for r in results:
                print ("Fecha: "+r['fecha'].strftime('%d-%m-%Y'), "   RTTE: "+r['remitente'], "   DESTINARIOS: "+r['destinatarios'], "   ASUNTO: "+r['asunto'])
    except:
        print ("Error: Formato de fecha incorrecto")'''


def apartado_c(dirindex):
    query = input("Introduzca palabras spam: ")
    ix = open_dir(dirindex)

    with ix.searcher() as searcher:
        query = QueryParser("asunto", ix.schema,
                            group=qparser.OrGroup).parse(query)
        results = searcher.search(query)
        for r in results:
            print ("FICHERO: "+r['nombrefichero'])


def get_schema():
    return Schema(titulo=TEXT(stored=True), link=TEXT(stored=True), autor=TEXT(stored=True), fecha=DATETIME(stored=True), respuestas=TEXT(stored=True), visitas=TEXT(stored=True), nombrefichero=ID(stored=True))


def add_doc(writer, path, docname):
    i = -1
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
        i = 3
        writer.add_document(titulo=title, link=link, autor=autor, fecha=fecha,
                            respuestas=respuestas, visitas=visitas, nombrefichero=docname)
        print ("Creado indice para fichero " + docname)
    except:
        print ("Error: No se ha podido a�adir el documento "+path+'/'+docname)
        print(i)


def indexar():
    crea_index("Threads", "Index")


def buscar_titulo_menu():
    buscar_titulo("Index")


def buscar_autor_menu():
    buscar_titulo("Index")


if __name__ == '__main__':
    root = Tk()
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Indexar", command=indexar)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.quit)
    menubar.add_cascade(label="Inicio", menu=filemenu)

    editmenu = Menu(menubar, tearoff=0)

    editmenu.add_command(label="Titulo", command=buscar_titulo_menu)
    editmenu.add_command(label="Autor", command=buscar_autor_menu)
    menubar.add_cascade(label="Buscar temas", menu=editmenu)

    root.config(menu=menubar)
    root.mainloop()
