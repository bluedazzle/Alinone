from bs4 import BeautifulSoup
import urllib

html = ''
html = urllib.urlopen('http://jiuye.lut.cn/www/ContentsMain.asp?Classid=27&page=1')
# with open('abc.txt','r') as f1:
#     line = f1.readline()
#     while line:
#         html += line
#         line = f1.readline()
soup = BeautifulSoup(html)
res = soup.findAll('table', attrs={'class': 'bord1'})
tdres = res[2].findAll('td')
for itm in range(4, len(tdres)):
    time =  tdres[itm].find('span', attrs={'class': 'blue'})
    if time is not None:
        print time.string