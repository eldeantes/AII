#encoding:latin-1
import os, re, shutil, urllib.request
from datetime import datetime
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, KEYWORD, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from bs4 import BeautifulSoup
import ssl


##############################Método para crear los ficheros para su búsqueda

def imprime_eventos():
    f=urllib.request.urlopen("https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades", context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
    s = BeautifulSoup(f,"lxml")
    eventos = s.find_all("article", class_="vevent")
    if not os.path.exists("Eventos"):
        os.mkdir("Eventos")
    else:
        shutil.rmtree("Eventos")
        os.mkdir("Eventos")
    #Por cada post: Título, link al tema, autor, fecha, número de respuestas, y número de visitas
    a=0
    for i in eventos:
        titulo = i.find_all("span", class_="summary")[0].string
        descripcion = i.find_all("p", class_="description")
        categories = i.find_all("li", class_="category")[0].find_all("span")
        categorias = ""
        x=0
        for cat in categories:
            if x==0:
                categorias = categorias + cat.string
                x=x+1
            else:
                categorias = categorias + "," + cat.string
                x=x+1


        fecha = i.find("div", class_="documentByLine")

        if(len(fecha.find_all("abbr"))==0):
            fechaInicio = str(fecha.contents[0].string).strip()
            fechaFin = str(fecha.contents[0].string).strip()
        elif(len(fecha.find_all("abbr"))==1):
            fechaInicio = fecha.find_all("abbr")[0].get("title")
            fechaFin = fecha.find_all("abbr")[0].get("title")
        elif(len(fecha.find_all("abbr"))==2):
            fechaInicio = fecha.find_all("abbr")[0].get("title")
            fechaFin = fecha.find_all("abbr")[1].get("title")

        if(len(fechaInicio)>10):
            fechaInicio = str(fechaInicio)
            fechaInicio = fechaInicio.replace("T"," ")
            fechaInicio = fechaInicio[:22] + fechaInicio[23:]
        else:
            fechaInicio=fechaInicio+" 00:00:00+0000"

        if(len(fechaFin)>10):
            fechaFin = str(fechaFin)
            fechaFin = fechaFin.replace("T"," ")
            fechaFin = fechaFin[:22] + fechaFin[23:]
        else:
            fechaFin=fechaFin+" 00:00:00+0000"

        with open('Eventos/'+str(a)+'.txt', 'w') as f:
            f.write(titulo+'\n')
            if(len(descripcion)>0):
                f.write(str(descripcion)+'\n')
            else:
                f.write('\n')
            f.write(categorias+'\n')
            f.write(fechaInicio+'\n')
            f.write(fechaFin+'\n')
        a=a+1

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
        'Buscar por título y descripción', 'Introduzca una palabra que esté en el título y la descripcion del tema')
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
            query = MultifieldParser(["fechaInicio","fechaFin"], ix.schema).parse(query)
            results = searcher.search(query)
            imprimir_resultados(results)
    except:
        print ("Error: Formato de fecha incorrecto")


def buscar_categorias(dirindex):
    def listar_busqueda(event):
        query = w.get()
        ix = open_dir(dirindex)

        with ix.searcher() as searcher:
            myquery = QueryParser("categorias", ix.schema).parse(query)
            results = searcher.search(myquery)
            imprimir_resultados(results)

    query = "admin"
    ix = open_dir(dirindex)

    with ix.searcher() as searcher:
        myquery = QueryParser("categorias", ix.schema,
                            group=qparser.NotGroup).parse(query)
        results = searcher.search(myquery)
        values =[]
        for r in results:
            values.append(r['categorias'])

    v = Toplevel()
    lb = Label(v, text="Buscar evento por categorias:")
    lb.pack(side = LEFT)



    w = Spinbox(v, values=values)
    w.bind("<Return>", listar_busqueda)
    w.pack(side = LEFT)


def get_schema():
    return Schema(titulo=TEXT(stored=True), descripcion=TEXT(stored=True), categorias=KEYWORD(stored=True, commas=True), fechaFin=DATETIME(stored=True),fechaInicio=DATETIME(stored=True),nombrefichero=ID(stored=True))


def add_doc(writer, path, docname):
    try:
        fileobj = open(path+'/'+docname, "rb")
        titulo = fileobj.readline().strip().decode()
        desc = fileobj.readline().strip().decode()
        categorias = fileobj.readline().strip().decode()
        fechaInicio = fileobj.readline().strip().decode()
        fechaInicio = datetime.strptime(fechaInicio, '%Y-%m-%d %H:%M:%S%z')
        fechaFin = fileobj.readline().strip().decode()
        fechaFin = datetime.strptime(fechaFin, '%Y-%m-%d %H:%M:%S%z')
        fileobj.close()
        writer.add_document(titulo=titulo, descripcion=desc, categorias=categorias, fechaInicio=fechaInicio,
        fechaFin=fechaFin, nombrefichero=docname)
        print ("Creado indice para fichero " + docname)
    except:
        print ("Error: No se ha podido a�adir el documento "+path+'/'+docname)


def indexar():
    imprime_eventos()
    crea_index("Eventos", "Index")


def buscar_titulo_descripcion_menu():
    buscar_titulo_descripcion("Index")


def buscar_fecha_menu():
    buscar_fecha("Index")

def buscar_categorias_menu():
    buscar_categorias("Index")


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
    editmenu.add_command(label="categorias", command=buscar_categorias_menu)
    menubar.add_cascade(label="Buscar", menu=editmenu)

    root.config(menu=menubar)
    root.mainloop()
