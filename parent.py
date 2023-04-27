import logging

from twisted.internet import reactor, protocol
from twisted.python import failure

logging.basicConfig(
    format='%(asctime)s %(process)d - %(levelname)s : %(message)s',
    level=logging.DEBUG
)
log = logging.getLogger('parent')

class WorkerProcess(protocol.ProcessProtocol):

    def __init__(self, text):
        self.text = bytes(text, encoding='ascii')

    def connectionMade(self):
        log.info("Connected to Process")
        self.transport.write(self.text)
        self.transport.closeStdin()


    def outReceived(self, data: bytes):
        log.info("Out Received from worker/child process: %s", data)
        self.printOutput(data)

    def errReceived(self, data: bytes):
        log.info("Err received from worker/child process: %s", data)

    def inConnectionLost(self):
        log.error("inConnectionLost!  stdin of child is closed")

    def outConnectionLost(self):
        log.error("outConnectionLost! stdout of child is closed")

    def errConnectionLost(self):
        log.error("errConnectionLost! stderr of child is closed")

    def processExited(self, reason: failure.Failure):  # Called when process ended normally or terminated
        log.error("Child Process Exited with status: %s", reason.value.exitCode)

    def processEnded(self, reason: failure.Failure):
        """ This would called when all file descriptors of child are closed
            it will be last callback to be called """
        log.error("Child Process Ended with status: %s", reason.value.exitCode)

    def printOutput(self, text):
        lines, words, chars = text.split()
        log.info("Total Lines: %s, Words: %s and Characters: %s", lines, words, chars)

if __name__ == '__main__':
    text = ''' Python is great to use anyware
            Python combined with twisted is unstoppable '''
    process = WorkerProcess(text)
    reactor.spawnProcess(process, 'python', ['python', 'word_counter.py'])
    reactor.run()