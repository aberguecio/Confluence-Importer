import os
from bs4 import BeautifulSoup
import request
import time

defoult_size = 104857600 # Confluence default: 104857600

def format_text(text):
    name = text.replace("%20"," ")
    name = name.replace("&","and")
    name = name.replace("%C2%B0","°")
    name = name.replace("n%CC%83","ñ")
    name = name.replace("%E2%80%98","‘")
    name = name.replace("%E2%80%99","’")
    name = name.replace("'","´")
    for leter in ["a","e","i","o","u","A","E","I","O","U"]:
        name=name.replace(f"{leter}%CC%81",str(leter))
    return name

def format_name(text):
    name = text.replace("&","and")
    name = name.replace("'","´")
    voc = ["a","e","i","o","u","A","E","I","O","U"]
    voc2 = ["á","é","í","ó","ú","Á","É","Í","Ó","Ú"]
    for x in range(10):
        name=name.replace(voc2[x],voc[x])
    return name

def link_replace(links,format_soup):
    for link in links:
        link_parts =str(link['href']).split("/")
        if link_parts[0] != "https:" and link_parts[0] != "http:":
            page_link = format_text(str(link_parts[-1]))
            link_name = ' '.join(page_link.split()[:-1])
            if link_parts[-1][-5:] == ".html":
                page_link = page_link[:-5]
                format_soup = format_soup.replace(str(link), "<ac:link><ri:page ri:content-title='"+page_link+"' /><ac:plain-text-link-body> <![CDATA["+link_name+"]]></ac:plain-text-link-body></ac:link>")
            else:
                format_soup = format_soup.replace(str(link), "<ac:link><ri:attachment ri:filename='"+page_link+"' /><ac:plain-text-link-body> <![CDATA["+link_name+"]]></ac:plain-text-link-body></ac:link>")
    return format_soup

def image_replace(images,format_soup):
    for image in images:
        image_parts = str(image['src']).split("/")
        if image_parts[0] != "https:" and image_parts[0] != "http:":
            format_soup = format_soup.replace(str(image), '<ac:image><ri:attachment ri:filename="'+str(image_parts[-1].replace("%20"," "))+'" /></ac:image>')
    return format_soup

def pae_update(pae,pae_hijo):
    pae[0]+=pae_hijo[0]
    pae[1]+=pae_hijo[1]
    pae[2].update(pae_hijo[2])
    pae[3].update(pae_hijo[3]) 
    pae[4].update(pae_hijo[4]) 

def content(folder, space, father = False):
    pae = [0,0,{},{},{}]
    folder_content = os.listdir(folder)
    for file in folder_content:
        if file[-5:] == ".html":

            # Opening the html file
            with open(folder+"/"+file, "r", encoding = 'UTF8') as html_file:
                index = html_file.read()
            soup = BeautifulSoup(index, 'lxml')
            format_soup = str(soup.body)

            # Remplaso imagenes
            images = soup.findAll('img')
            format_soup = image_replace(images,format_soup)

            # Remplaso links
            links = soup.findAll('a', href=True)
            format_soup = link_replace(links,format_soup)

            #Send Post request whit body
            name_page = format_name(file[:-5])
            print("Creating Page:",name_page)
            response = request.post_page(space,name_page,str(format_soup),father)
            if response["statusCode"] == 200:
                pae[0]+=1
                if os.path.exists(folder+"/"+file[:-5]):
                    pae_hijo = content(folder+"/"+file[:-5], space, response["id"])
                    pae_update(pae,pae_hijo)
            else:
                print("Error:\n",name_page,response,"\nCreating Raw Page:",name_page)
                pae[2][name_page] = str(response)

                response = request.post_page(space,name_page,str(soup.body),father)
                if response["statusCode"] == 200:
                    pae[0]+=1
                    if os.path.exists(folder+"/"+file[:-5]):
                        pae_hijo = content(folder+"/"+file[:-5], space, response["id"])
                        pae_update(pae,pae_hijo)
                else:
                    print("\nCritical Error:\n",name_page,response,"\nSkipping Subfolders...")
                    pae[3][name_page] = str(response)

        # Attaching file
        elif (file[-5] == "." or file[-4] == "." or file[-3] == "."):
            print("Attaching file:", file)
            size = os.path.getsize(folder+"/"+file)
            if size < defoult_size: # Confluence default: 104857600
                try:
                    response = request.upload_file(folder+"/"+file,father)
                except:
                    pae[2][file] = f"Error ataching {file} of size {size}"
                    print("Error ataching"+file)
                else:
                    if response["statusCode"] == 200:
                        pae[1]+=1
                    else:
                        print("\nError:\n",response,"\n")
                        pae[2][file] = str(response)
            else:
                print(f"File '{file}' to big")
                pae[4][file] = [folder,size]

    return pae

def timer(start_time):
    total_time = int(time.time() - start_time)
    total_time = time.strftime('%H:%M:%S', time.gmtime(total_time))
    return total_time

if __name__ == "__main__":
    start_time = time.time()
    end_data = content("<notion export folder>", "<confluence space id>")
    total_time = timer(start_time)
    with open("info.txt", "w") as file:
        file.write(">>>  IFORMATION  <<<\n")
        file.write(f"Pages Created:{end_data[0]}\n")
        file.write(f"Attached Files:{end_data[1]}\n")
        file.write(f"Execution Time {total_time}\n" )
        file.write(f"Errors found:{len(end_data[2])}\n")
        for error in end_data[2]:
            file.write(f"{error}: {end_data[2][error]}\n")
        file.write(f"CRITICAL ERRORS:{len(end_data[3])}\n")
        for error in end_data[3]:
            file.write(f"{error}: {end_data[3][error]}\n")
        file.write(f"Files to big:{len(end_data[4])}\n")
        for error in end_data[4]:
            file.write(f"{error}: {end_data[4][error]}\n")
        file.write(">>>   END   <<<")
