import subprocess, signal, os
from twisted.internet import task
from twisted.internet import reactor

timeout = 180.0 # tres minutos

process = None

def restartYowsup():
    global process
    if process == None:
        process = subprocess.Popen('nameko run --config ./serviceconfig.yml service', shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    else:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process = subprocess.Popen('nameko run --config ./serviceconfig.yml service', shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)

l = task.LoopingCall(restartYowsup)
l.start(timeout) # ejecutar cada tres minutos

reactor.run()