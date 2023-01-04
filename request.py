import requests 
import json


with open('userdata.json', 'r') as f:
  userdata = json.load(f)
url = f'https://{userdata["URL"]}.atlassian.net/wiki/rest/api/content/'

def PostPage(space,title,body):
    reqdata = {
        "type":"page",
        "title":title,
        "space":{"key":space},
        "body":{
            "storage":{
                "value":body,
                "representation":"storage"}}}
    response = requests.post(url, auth = (userdata["username"], userdata["password"]), json= reqdata)
    #print(response.json())
    return response.status_code

if __name__ == "__main__":
    print(PostPage("DOC","first","bla"))

