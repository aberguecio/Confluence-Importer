import os
import request
from bs4 import BeautifulSoup

def format_text(texto):
    name = texto.replace("%20"," ")
    name = name.replace("&","and")
    for l in ["a","e","i","o","u","A","E","I","O","U"]:
        name=name.replace(f"{l}%CC%81",str(l))
    return name

def format_name(text):
    name = text.replace("&","and")
    voc = ["a","e","i","o","u","A","E","I","O","U"]
    voc2 = ["á","é","í","ó","ú","Á","É","Í","Ó","Ú"]
    for x in range(10):
        name=name.replace(voc2[x],voc[x])
    return name

def link_replace(links):
    for link in links:
        link_parts =str(link['href']).split("/")
        if link_parts[0] != "https:":
            name = format_text(str(link_parts[-1]))
            if link_parts[-1][-5:] == ".html":
                format_soup = format_soup.replace(str(link), "<ac:link><ri:page ri:content-title='"+name[:-5]+"' /><ac:plain-text-link-body> <![CDATA["+name[:-5]+"]]></ac:plain-text-link-body></ac:link>")
            else:
                format_soup = format_soup.replace(str(link), "<ac:link><ri:attachment ri:filename='"+name+"' /><ac:plain-text-link-body> <![CDATA["+name+"]]></ac:plain-text-link-body></ac:link>")
    return format_soup

def image_replace(images):
    for image in images:
        image_parts = str(image['src']).split("/")
        if image_parts[0] != "https:":
            format_soup = format_soup.replace(str(image), '<ac:image><ri:attachment ri:filename="'+str(image_parts[-1].replace("%20"," "))+'" /></ac:image>')
    return format_soup

def pae_update(response,pae,folder,file,space):
        pae[0]+=1
        if os.path.exists(folder+"/"+file[:-5]):
            pae_hijo = content(folder+"/"+file[:-5], space, response["id"])
            pae[0]+=pae_hijo[0]
            pae[1]+=pae_hijo[1]
            pae[2].update(pae_hijo[2])
            pae[3].update(pae_hijo[3])
    
def content(folder, space, father = False):
    pae = [0,0,{},{}]
    list = os.listdir(folder)
    for file in list:
        if file[-5:] == ".html":
            name_page = format_name(file[:-5])

            # Opening the html file
            HTMLFile = open(folder+"/"+file, "r", encoding = 'UTF8')
            index = HTMLFile.read()
            soup = BeautifulSoup(index, 'lxml')
            format_soup = str(soup.body)

            # Remplaso imagenes
            images = soup.findAll('img')
            format_soup = image_replace(images)

            # Remplaso links
            links = soup.findAll('a', href=True)
            format_soup = link_replace(links)
           
            #Send Post request whit body
            print("Creating Page:",name_page)
            response = request.post_page(space,name_page,str(format_soup),father)
            if response["statusCode"] == 200:
                pae_update(response,pae,folder,file,space)
            else:
                print("Error:\n",response,"\nCreating Raw Page:",name_page)
                pae[2][name_page] = str(response)
                response = request.post_page(space,name_page,str(soup.body),father)
                if response["statusCode"] == 200:
                    pae_update(response,pae,folder,file,space)
                    print("\nCritical Error:\n",response,"\nSkipping Subfolders...")
                    pae[3][name_page] = str(response)

        # Attaching file
        elif (file[-5] == "." or file[-4] == "."):
            print(" -Attaching:",file)
            response = request.upload_file(folder+"/"+file,father)
            if response["statusCode"] == 200:
                pae[1]+=1
            else:
                print("\nError:\n",response,"\n")
                pae[2][file] = str(response)
    return pae


if __name__ == "__main__":
    fin = content('Export pro',"NI")
    print("\n>>>   RESULTS   <<<")
    print("Pages created:",fin[0])
    print("Attached files:",fin[1])
    print("Errors found:",len(fin[2]))
    for error in fin[2]:
        print(error,fin[2][error])
    print("CRITICAL ERRORS!:",len(fin[3]))
    for error in fin[3]:
        print(error,fin[3][error])
    print("\n>>>   END   <<<\n")