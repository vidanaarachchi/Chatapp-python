import socket

import time

from datetime import datetime

 

class color:

   PURPLE = '\033[95m'

   CYAN = '\033[96m'

   DARKCYAN = '\033[36m'

   BLUE = '\033[94m'

   GREEN = '\033[92m'

   YELLOW = '\033[93m'

   RED = '\033[91m'

   BOLD = '\033[1m'

   ITALIC='\033[3m'

   FAINT='\033[2m'

   UNDERLINE = '\033[4m'

   END = '\033[0m'

 

 

def PrintMsg(msg):

    hdr=(msg[:32])

    pld=(msg[32:])

    msgType = hdr[:1]

    time = hdr[1:-21 ]

    client = hdr[11:-13]

    group = hdr[19:-5]

 

    print(color.BLUE+color.ITALIC+color.FAINT+"At "+ str(datetime.fromtimestamp(int(time)) )+" user "+client+ " says:"+color.END)

    print(color.BOLD+"\t" + pld + color.END)

 

 

 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as get:

    get.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    get.bind(('',33330))

    get.listen()

    while True:

        SvrCon, addr = get.accept()

        with SvrCon:

            while True:

                data= SvrCon.recv(1024).decode('utf-8')

                if data:

                    PrintMsg(data)

                else:

                    break
