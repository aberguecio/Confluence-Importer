import request
import os
from bs4 import BeautifulSoup

def formato_texto(texto):
    nombre = texto.replace("%20"," ")
    nombre = nombre.replace("&","and")
    for l in ["a","e","i","o","u","A","E","I","O","U"]:
        nombre=nombre.replace(f"{l}%CC%81",str(l))
    return nombre

def formato_nombre(texto):
    nombre = texto.replace("&","and")
    voc = ["a","e","i","o","u","A","E","I","O","U"]
    voc2 = ["á","é","í","ó","ú","Á","É","Í","Ó","Ú"]
    for x in range(10):
        nombre=nombre.replace(voc2[x],voc[x])
    return nombre
    

def contenido(direccion, espacio, padre = False):
    pae = [0,0,{},{}]
    lista = os.listdir(direccion)
    for archibo in lista:
        if archibo[-5:] == ".html":
            nombre_pagina = formato_nombre(archibo[:-5])

            # Opening the html file
            HTMLFile = open(direccion+"/"+archibo, "r", encoding = 'UTF8')
            index = HTMLFile.read()
            soup = BeautifulSoup(index, 'lxml')
            format_soup = str(soup.body)

            # Remplaso imagenes
            images = soup.findAll('img')
            print("Preparando Archibo:",nombre_pagina)

            for image in images:
                image_parts = str(image['src']).split("/")
                if image_parts[0] != "https:":
                    format_soup = format_soup.replace(str(image), '<ac:image><ri:attachment ri:filename="'+str(image_parts[-1].replace("%20"," "))+'" /></ac:image>')
            
            # Remplaso links
            links = soup.findAll('a', href=True)
            for link in links:
                link_parts =str(link['href']).split("/")
                nombre = formato_texto(str(link_parts[-1]))
                if link_parts[-1][-5:] == ".html":
                    format_soup = format_soup.replace(str(link), "<ac:link><ri:page ri:content-title='"+nombre[:-5]+"' /><ac:plain-text-link-body> <![CDATA["+nombre[:-5]+"]]></ac:plain-text-link-body></ac:link>")
                else:
                    format_soup = format_soup.replace(str(link), "<ac:link><ri:attachment ri:filename='"+nombre+"' /><ac:plain-text-link-body> <![CDATA["+nombre+"]]></ac:plain-text-link-body></ac:link>")
            
            #Send Post request whit body
            print("Creando Pagina:",nombre_pagina)
            respuesta = request.post_page(espacio,nombre_pagina,str(format_soup),padre)
            if respuesta["statusCode"] == 200:
                pae[0]+=1
                if os.path.exists(direccion+"/"+archibo[:-5]):
                    pae_hijo =contenido(direccion+"/"+archibo[:-5], espacio, respuesta["id"])
                    pae[0]+=pae_hijo[0]
                    pae[1]+=pae_hijo[1]
                    pae[2].update(pae_hijo[2])
                    pae[3].update(pae_hijo[3])
            else:
                print("Error:\n",respuesta,)
                pae[2][nombre_pagina] = str(respuesta)

                print("Creando Pagina sin formato:",nombre_pagina)
                respuesta = request.post_page(espacio,nombre_pagina,str(soup.body),padre)
                if respuesta["statusCode"] == 200:
                    pae[0]+=1
                    if os.path.exists(direccion+"/"+archibo[:-5]):
                        pae_hijo =contenido(direccion+"/"+archibo[:-5], espacio, respuesta["id"])
                        pae[0]+=pae_hijo[0]
                        pae[1]+=pae_hijo[1]
                        pae[2].update(pae_hijo[2])
                        pae[3].update(pae_hijo[3])
                else:
                    print("\nError:\n",respuesta,"\nSaltando subcarpetas...")
                    pae[3][nombre_pagina] = str(respuesta)

        # Attaching file
        elif (archibo[-5] == "." or archibo[-4] == "."):
            print("Adjuntando:",archibo)
            respuesta = request.upload_file(direccion+"/"+archibo,padre)
            if respuesta["statusCode"] == 200:
                print("Respuesta:",respuesta["statusCode"])
                pae[1]+=1
            else:
                print("\nError:\n",respuesta,"\n")
                pae[2][archibo] = str(respuesta)
    return pae


if __name__ == "__main__":
    fin = contenido('Export pro',"TI20")
    print("\n>>>   RESULTADOS   <<<")
    print("Paginas creadas:",fin[0])
    print("Archibos adjuntos:",fin[1])
    print("Errores encontrados:",len(fin[2]))
    for error in fin[2]:
        print(error,fin[2][error])
    print("ERRORES CRITICOS!:",len(fin[3]))
    for error in fin[3]:
        print(error,fin[3][error])
    print("\n>>>   FIN   <<<\n")