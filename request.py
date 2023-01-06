import requests 
import json


with open('userdata.json', 'r') as f:
  userdata = json.load(f)

def post_page(space,title,body,father=False):
    url = f'https://{userdata["URL"]}.atlassian.net/wiki/rest/api/content/'
    reqdata = {
        "type":"page",
        "title":title,
        "space":{"key":space},
        "body":{
            "storage":{
                "value":body,
                "representation":"storage"}}}

    if father:
        reqdata["ancestors"] = [{ "type": "page","id":father}]

    response = requests.post(url, auth = (userdata["username"], userdata["password"]), json= reqdata)
    res_dic = response.json()
    res_dic["statusCode"] = response.status_code
    return res_dic

def upload_image(file,id):
    url = f'https://{userdata["URL"]}.atlassian.net/wiki/rest/api/content/{str(id)}/child/attachment/'
    headers = {"X-Atlassian-Token": "nocheck"}
    content_type = 'image/jpeg'
    files = {'file': (file, open(file, 'rb'),content_type)}
    response = requests.post(url, headers=headers, files=files, auth = (userdata["username"], userdata["password"]))
    res_dic = response.json()
    res_dic["statusCode"] = response.status_code
    return res_dic

def upload_file(file,id):
    url = f'https://{userdata["URL"]}.atlassian.net/wiki/rest/api/content/{str(id)}/child/attachment/'
    headers = {"X-Atlassian-Token": "nocheck"}
    files = {'file': (file, open(file, 'rb'))}
    response = requests.post(url, headers=headers, files=files, auth = (userdata["username"], userdata["password"]))
    res_dic = response.json()
    res_dic["statusCode"] = response.status_code
    return res_dic

if __name__ == "__main__":
    response1 = post_page("DOC","Padre1",'body')
    response2 = post_page("DOC","Imagen1",'body',response1["id"])
    #response3 = upload_image('jpg.jpg',response2["id"]) 
    #response4 = upload_image('grafico.png',response2["id"]) 
    print(response1["statusCode"],response2["statusCode"])

