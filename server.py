import socket

from datetime import datetime

 

HOST = '192.168.8.103'  # Standard loopback interface address (localhost)

PORT = 33333        # Port to listen on (non-privileged ports are > 1023)

 

userIPset=[]

 

def regUser(clientIP,client,group,name,time):

    print("User registration initiated ::"+ name+" on IP "+ clientIP)

    for ExtUser in userIPset:

        if ExtUser[0]==clientIP:

            userIPset.remove(ExtUser)

    userIPset.insert(0,[clientIP,client,group,name,time])

    print("\t User DB updated successfully!")

    RecvMsg('')

 

def fwdMsg(hdr,msg,grp):

    print ("\t Begin forwarding messege to group " + grp.upper())

    for Client in userIPset:

        if grp.upper()==Client[2].upper():

            print( " \t \t Sending to :-->"+Client[0])

            try:

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send:

                    send.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

                    send.connect((Client[0],33330))

                    send.sendall(bytes(hdr+msg,'utf-8'))

                    send.close()

            except:

                send.close()

                print("\t \t Error Sending to client")

            finally:

                send.close()

                print(" \t\t Done forwarding meessege!")

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    RecvMsg('')

 

def ProcMSG(hdr,pld,sndrIP):

    #print(hdr)

    #print(pld)

    msgType = hdr[:1]

    time = hdr[1:-21 ]

    client = hdr[11:-13]

    group = hdr[19:-5]

    if msgType=="R":

        regUser(sndrIP,client,group,pld,time)

 

    if msgType=="M":

        print("Messege from User :" + client+" to Group : "+ group+" at : "+ str(datetime.fromtimestamp(int(time)) )+" reads: "+ pld)

        print(" to Group : "+ group)

        fwdMsg(hdr,pld,group)

 

def RecvMsg(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            print('Server on standby...')

            s.bind((HOST, PORT))

            s.listen()

            uIP = '';

            conn, addr = s.accept()

            sndrIP = conn.getpeername()[0]

 

            with conn:

                while True:

                    data = conn.recv(1024).decode('utf-8')

                    hdr =(data[:32])

                    pld = (data[32:])

                    s.close()

                    print('Messege received : Processing Now')

                    ProcMSG(hdr,pld,sndrIP)

 

while True:

    RecvMsg('')
