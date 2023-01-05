import requests 
import json


with open('userdata.json', 'r') as f:
  userdata = json.load(f)
url = f'https://{userdata["URL"]}.atlassian.net/wiki/rest/api/content/'

def PostPage(space,title,body,father=False):
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
        print(reqdata)

    response = requests.post(url, auth = (userdata["username"], userdata["password"]), json= reqdata)
    res_dic = response.json()
    res_dic["statusCode"] = response.status_code
    return res_dic

if __name__ == "__main__":
    response1 = PostPage("DOC","Title23","Body")
    response2 = PostPage("DOC","Title24","Body",response1["id"])
    print(response1["statusCode"],response2["statusCode"])

