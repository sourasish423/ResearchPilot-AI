import requests #This library lets Python send HTTP requests to websites and retrieve their webpage content.
from bs4 import BeautifulSoup#Webpages are usually written in HTML. BeautifulSoup helps us extract readable text from that HTML.

def read_webpage(url:str):
     response = requests.get(url, timeout=15)

     soup=BeautifulSoup(response.text,"html.parser")

     for tag in soup(["script", "style", "nav", "footer", "header"]):#Finds unwanted page elements
        tag.decompose()#remove those elements
    
     text = soup.get_text(separator=" ", strip=True)#Extracts readable text
     #get_text() is a BeautifulSoup method that extracts readable text from HTML.s

     return text[:5000]
        