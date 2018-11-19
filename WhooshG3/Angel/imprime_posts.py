#encoding:latin-1
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import shutil


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
