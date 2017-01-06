import pexpect
import logging
import random
import sys
import time

from nameko.extensions import DependencyProvider


class YowsupExtension(DependencyProvider):
    def setup(self):
        logging.info('Starting YowsUP...')

        number = self.container.config['YOWSUP_USERNAME']
        password = self.container.config['YOWSUP_PASSWORD']
        logging.info('Trying to connect via %s:%s'  % (number, password))
        startCommand = 'yowsup-cli demos --yowsup --login %s:%s' % (number, password)

        self.shell = pexpect.spawn(startCommand)
        self.expect([".+\[offline\]:"])
        strLogin = '/login %s %s' % (number, password)
        self.shell.sendline(strLogin)
        login = self.expect([".+\[connected\]:","Login Failed"],5)
        time.sleep(random.randint(2,6))
        self.shell.sendline('/presence available')
        if(login == 2):
            logging.info('Cannot login....cannot continue')
            exit()

        return True

    def login(self, number, password):
        logging.info('Trying to login via %s %s'  % (number, password))
        startCommand = '/login %s %s' % (number, password)
        self.shell.sendline(startCommand)
        logging.info('Connect')

    def expect(self,expectArr,timeout = 1):
        try:
            i = self.shell.expect(expectArr,timeout=timeout)
            i=i+1
        except:
            logging.info("Exception was thrown")
            logging.info("debug information:")
            logging.info(str(self.shell))
            i = 0
        return i

    def sendTextMessage(self, address,message):
        #jid = address+'@s.whatsapp.net'

        #Cambiar a estado a "En linea"
        #self.shell.sendline('/presence available')
        #time.sleep(random.randint(2,4))
        #Cambiar a estado "Escribiendo..."
        #start_typing = '/state typing %s' % jid
        #self.shell.sendline(start_typing)
        #time.sleep(random.randint(3,6))
        #Cambiar a estado "En linea"
        #stop_typing = '/state stoped %s' % jid
        #self.shell.sendline(stop_typing)

        time.sleep(random.randint(2,6))

        logging.info('Trying to send Message to %s:%s' % (address, message))

        messageCommand = '/message send %s "%s"' % (address, message)
        self.shell.sendline(messageCommand)

        #Cambiar a estado "Desconectado"
        #self.shell.sendline('/presence unavailable')
        
        return True

    def sendImageMessage(self, address,message):
        
        ########Ruta imagen########
        basePath = '/mnt/nfs/difusion/'
        ###########################
        
        #jid = address+'@s.whatsapp.net'

        #Cambiar a estado a "En linea"
        #self.shell.sendline('/presence available')
        #time.sleep(random.randint(2,4))
        #Cambiar a estado "Escribiendo..."
        #start_typing = '/state typing %s' % jid
        #self.shell.sendline(start_typing)
        #time.sleep(random.randint(3,6))
        #Cambiar a estado "En linea"
        #stop_typing = '/state stoped %s' % jid
        #self.shell.sendline(stop_typing)

        time.sleep(random.randint(2,6))

        logging.info('Trying to send Image to %s:%s' % (address, message))

        messageCommand = '/image send %s %s%s' % (address, basePath, message)
        self.shell.sendline(messageCommand)

        #Cambiar a estado "Desconectado"
        #self.shell.sendline('/presence unavailable')

    def get_dependency(self, worker_ctx):
        return self
