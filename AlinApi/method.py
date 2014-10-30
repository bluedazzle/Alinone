import random

def createverfiycode(count=6):
    return string.join(random.sample('0123456789', count)).replace(" ", "")

def sendverifycode(content, phone):
    return 0