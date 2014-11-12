import subprocess

def spiderprocess(id):
    shelltext = list(['python', 'manage.py', 'cronorder', str(id)])
    subprocess.Popen(shelltext, shell = False)