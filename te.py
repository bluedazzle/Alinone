import datetime
import time
import random
import urllib

url = "http://127.0.0.1:8000/alin_admin/create_order?id="
i = 1
while True:
    url += str(i)
    req = urllib.urlopen(url)
    print req.read()
    i += 1
    time.sleep(5)
