# Confluence-Importer
Notion to Confluence importer
## Start
install requests and BeautifulSoup
```
pip install requests
pip install BeautifulSoup
```
create userdata.json with:
```
{
    "username":"<usuario>",
    "password":"<Api Token>",
    "URL":"<url>"
}
```
in importer.py edit the line 92:
```
fin = contenido("<carpeta>","<espacio_id>")
```