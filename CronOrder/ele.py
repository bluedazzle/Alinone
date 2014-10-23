from bs4 import BeautifulSoup
import datetime


html = ''
with open('nap.txt', 'r') as f1:
    line = f1.readline()
    while line:
        html += line
        line = f1.readline()
    f1.close()
soup = BeautifulSoup('''<li class = 'aaa'>abc</li>''')
print soup.li.next
