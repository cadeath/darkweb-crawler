from bs4 import BeautifulSoup
import requests
from datetime import datetime

# pip install BeautifulSoup

# @cadeath
# add save_csvf to have CSV format ready
# replace RE with BeautifulSoup
# restructured saving filename
# csv sanitizer added

def save_csvf(result):
    try:
        linkText = result.find('a').get_text(strip=True)
        url = result.find('a')['href']
        desc = result.find('p').get_text(strip=True)
        tor = result.find('cite').get_text(strip=True)
        lastSeen = result.find('span', class_="lastSeen").get_text(strip=True)

        lastSeen_ts = ""
        lastSeen_span = result.find('span', class_='lastSeen')
        if lastSeen_span:
            lastSeen_ts = lastSeen_span['data-timestamp']
            
        desc = csv_sanitize(desc)
        linkText = csv_sanitize(linkText)
        lastSeen = csv_sanitize(lastSeen)
        lastSeen_ts = csv_sanitize(lastSeen_ts)

        return f"{tor},{linkText},{tor}{url},{desc},{lastSeen_ts},{lastSeen}\n"
    except Exception as e:        
        print(e)
        print("Incoming:",result)

        return None
    
def csv_sanitize(str):
    str = str.replace('"', '""')
    
    if ',' in str or '\n' in str or '"' in str:
        str = f'"{str}"'
    
    return str

def scrape(newdata):
        yourquery = newdata                                                 #Takes new Data
        
        if " " in yourquery:
            yourquery = yourquery.replace(" ", "+")
        url = "https://ahmia.fi/search/?q={}".format(yourquery)
        request = requests.get(url)
        content = request.text

        soup = BeautifulSoup(content, 'html.parser')
        with open("tmp.txt","w", encoding='utf-8') as f:
             f.write(content)
             f.close()

        results = soup.find_all('li', class_='result')
        
        now = datetime.now()
        file_postfix = now.strftime("%d%m%Y-%H%M%S")
        
        filename = "sites-{}.txt".format(str(file_postfix))
        print("Saving to...", filename)
        
        f = open(filename,"w")
        f.write("r2 csv result extarct @cadeath\n")
        f.write("tor,title,url,desc,timestamp,seen\n")
        f.close()

        for k in results:
            with open(filename, "a",encoding='utf-8') as newfile:
                newfile.write(save_csvf(k))

        print("All the files written to a text file: ", filename)
        if len(results) > 0:
            print(f"{len(results)} entries saved.")
            
newdata=input("[*]Please enter your query: ")
scrape(newdata)
# scrape("Philippines")
