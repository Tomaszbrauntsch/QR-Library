import pyqrcode
from bs4 import BeautifulSoup
import requests
rurl = "grabify.link/track/SFP9YQ"
r = requests.get("https://" + rurl)
data = r.text
soup = BeautifulSoup(data, "html.parser")
all = soup.find_all('h2')
count = 0
for h2 in all:
    count += 1
    if count == 2:
        print (h2.text)
#print (all)
#qrurl = pyqrcode.create('https://www.apple.com')
#qrurl.svg('textqr.svg', scale=8)
# https://wawa-news.com/wp-content/uploads/2018/06/Thanks.jpg
# print(url.terminal(quiet_zone=1))
