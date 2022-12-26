from bs4 import BeautifulSoup

with open(r"https://www.youtube.com/@rennyyo6644", encoding="utf-8") as f:
    soup = BeautifulSoup(f)
    
    c = soup.find_all(class_='body')
    for cc in c:
        txt = cc.text
        x = txt.strip()
        print(x)