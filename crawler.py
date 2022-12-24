import bs4 
from bs4 import BeautifulSoup
import requests
response = requests.get("https://open.spotify.com/artist/6VZlJla5fcw20R97dOIadz")
#YOUTUBE_API_KEY = "AIzaSyBCLgvmy9gBNMOygN8SkNRLglfzug-SxLc"
soup = BeautifulSoup(response.text, "html.parser")
number = soup.find("div",{"class":"Type__TypeElement-sc-goli3j-0 jqfHBy"})
#.getText()
print(number)