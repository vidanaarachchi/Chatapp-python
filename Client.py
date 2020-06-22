import socket

import time

from datetime import datetime

HOST = '192.168.8.103'  # The server's hostname or IP address

PORT = 33333  # The port used by the server


def ProcessPkt(msgType, sndrID, rsvrID, msgPld):
    pdu = msgType + int(time.mktime(datetime.now().timetuple())).__str__() + sndrID + rsvrID + "00000" + msgPld
    return pdu;


SID = input('Enter Your CB:')

NME = input('Enter your Name:')

RID = input('Enter Target:')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.connect((HOST, PORT))

    pktmsg = ProcessPkt('R', SID, RID, NME)

    s.sendall(bytes(pktmsg, 'utf-8'))

    s.close()

while 1:
    msg = input('Type your message: ')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.connect((HOST, PORT))

        pktmsg = ProcessPkt('M', SID, RID, msg)

        s.sendall(bytes(pktmsg, 'utf-8'))

        s.close()
