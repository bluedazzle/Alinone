import subprocess

def spiderprocess(id):
    shelltext = 'python manage.py cronorder ' + str(id)
    subprocess.Popen(shelltext, shell = True)