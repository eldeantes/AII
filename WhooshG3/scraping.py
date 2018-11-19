# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import os.path
import re
from bs4 import BeautifulSoup
import urllib.request
import ssl

def extraer_web(): 
    f=urllib.request.urlopen("https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades", context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
    s = BeautifulSoup(f,"lxml")
    l = s.find_all("article", class_="vevent")
    return l


def extractData():
    x=1
    l = extraer_web()
    for i in l:
        '''titulo = i.find_all("a", class_="title")[0].string
        for a in i.find_all("a", class_="title"):
            link = a['href']
        autor = i.find_all("strong")[0].string
        for b in i.find_all("a", class_="username understate"):
            title = b['title']
            fecha = re.compile('el \s*(.*)').search(title).group(1)     
        respuestas = i.find_all("a", class_="understate")[1].string
        visitasLong = i.find_all("li")[1].string
        visitas = re.compile(':\s*(.*)').search(visitasLong).group(1)'''


        titulo = i.find_all("span", class_="summary")[0].string
        print(titulo)

        fechaInicio, fechaFin = i.find_all("div", class_="documentByLine")[0].find_all("span").split(",")
        print(fechaInicio)
        print(fechaFin)


        categorias = i.find_all("li", class_="category")[0].find_all("span")
        categories = ""
        for cat in categorias:
            
            categories = categories + "," + cat.string
        print(categories)

        print("--------------------------------------------")

        
        '''file = open(dirdocs+'tema'+str(x)+'.txt','w')
        file.write(titulo + '\n')
        file.write("https://foros.derecho.com/" + link + '\n')
        file.write(autor + '\n')
        file.write(fecha + '\n')
        file.write(respuestas + '\n')
        file.write(visitas + '\n')
        file.close()'''
        x = x + 1


if __name__ == "__main__":
    extractData()
