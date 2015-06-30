__author__ = 'AleksejMurzanev'

from sys import exit
from signal import signal, SIGINT
import socket
import json
from thread import start_new_thread
import random

# Constants
PACKAGE_SIZE = 8196
DGRAM_ERROR = -2

HOST = ''
PORT = 5001


# KeyboardInterrupt
def signal_handler(signal, frame):
    exit(0)
signal(SIGINT, signal_handler)

# Initialize DGRAM
print "Initializing DGRAM ... ",
dgram = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    dgram.bind((HOST, PORT))
except socket.error, msg:
    print
    print "DGRAM error \"{0}\" ({1}) Closing ...".format(msg[1], msg[0])
    exit(DGRAM_ERROR)
print "OK."

# Success ... start looping and maintaining server
print "Start server looping ..."
while 1:

    (data, addr) = dgram.recvfrom(PACKAGE_SIZE)

    # Escape \r\n
    data = data.replace("\n", "").replace("\r", "")

    # Check Data
    if not data or data == '': continue

    # Logging
    print "  [{0}:{1}] - {2}".format(addr[0], addr[1], data)

    # Generate Reply
    js = None
    try:
        js = json.loads(data)
    except:
        print "    Bad json!"
        continue

    reply = None
    if js["operation"] == "balance":
        reply = "123.45$"

    # Send Reply
    dgram.sendto(reply, addr)