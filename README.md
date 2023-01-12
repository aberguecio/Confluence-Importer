# Confluence-Importer
Notion to Confluence importer
## Notion Export 
In Notion go to Settings and members > Settings > Export all workspace content  
And in the options put:
- Export format: HTML
- Include content: Everything
- Create folders for subpages: yes  

Extract the files and leave them in this folder

## Start
Install requests and BeautifulSoup
```
pip install requests
pip install BeautifulSoup
```
Create userdata.json with:
```
{
    "username":"<usuario>",
    "password":"<Api Token>",
    "URL":"<url>"
}
```
In importer.py edit the line 121:
```
end_data = content("<notion export folder>", <confluence space id>")
```
And run importer.py