from nameko.rpc import rpc
import logging

from pprint import pprint
from src.yowsupextension import YowsupExtension


class yowsup(object):
    name = "yowsup"

    y = YowsupExtension()

    @rpc
    def send(self, type, body, address):
        logging.info('Get message: %s,%s,%s' % (type, body, address))
        output = self.y.sendTextMessage(address, body)

        return True

    @rpc
    def sendimage(self, type, body, address):
        logging.info('Get message: %s,%s,%s' % (type, body, address))
        output = self.y.sendImageMessage(address, body)

        return True



