import os
import sys
import logging

from twisted.internet import threads, reactor

logging.basicConfig(
    filename='worker.log',
    format='%(asctime)s %(process)d - %(levelname)s : %(message)s',
    level=logging.DEBUG
)
log = logging.getLogger('parent')
log.debug("Word Counter Started")


def count(text):
    log.debug("Text: %s", text)
    lines = text.split('\n')
    lines_count = len(lines)
    words = 0
    for line in lines:
        words += len(line.strip().split(' '))
    chars = len(text)
    output = '{} {} {}'.format(lines_count, words, chars)
    log.info("Counts lines: %s, words: %s, chars: %s", lines_count, words, chars)
    return output

def readInput():
    text = ''
    log.info("Reading Input....")
    while not sys.stdin.closed:
        c = sys.stdin.read(8)
        text += c
        # log.debug("read ....%s  Empty: %s", c, c=='')
        if c =='':
            break
    return text


def finishedReading(result):
    log.info("Input received: %s", result)
    log.info("is stdin closed %s", sys.stdin.closed)
    counts = count(result)
    sys.stdout.write(counts)
    reactor.callLater(2, reactor.stop)

# reactor.callInThread(readInput)
df = threads.deferToThread(readInput)
df.addCallback(finishedReading)
reactor.run()

