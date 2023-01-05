import os
import json

def contenido(direccion):
    lista = os.listdir(direccion)
    cont = {}
    for archibo in lista:
        if archibo[-5:] == ".html":
            cont[archibo] = ""
    for html in cont:
        if os.path.exists(direccion+"/"+html[:-5]):
            retorno = contenido(direccion+"/"+html[:-5])
            if retorno:
                cont[html] = retorno
    return cont


if __name__ == "__main__":
    dicc = contenido('Export')
    #print(dicc)
    with open('data.json', 'w') as fp:
        json.dump(dicc, fp)