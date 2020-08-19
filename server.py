import socket #allow connections to come into our server through a port
import sys
from _thread import *

#server needs to keep track of p1 and p2 on both sides - can be on harddrive or on memory.
#for this we are storing on memory

#using a port on our server to look for connections
server = "10.225.21.101" #address of the computer that server srcipt is being run on - cmd.exe > ipconfig
port = 5555

#initialise
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #types of sockets to use

#bind socket and server together
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

#argument is how many people you want to connect
s.listen(2)
print("Waiting for a connection, Server started.")

def read_pos(str):
        str = str.split(",")
        return int(str[0]),int(str[1])

def make_pos(tup):
    return str(tup[0])+","+str(tup[1])


#2 tuples of locations [p1, p2]
pos = [(0,0),(100,100)]

#THREADING - start another process that will run in the background
#threaded function
def threaded_client(conn, player): 
    #pass #you don't need to wait for this function to finish executing and you can start the next line of code 
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            #reply = data.decode("utf-8")
            pos[player] = data

            if not data:
                print("Disconnected") #if no info recieved from server
                break
            else:
                #if 1, send 0's data
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Recieved: ", data)
                print("Sending: ", reply)
            
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost Connection")
    conn.close()


#need to keep track of players
currentPlayer = 0

#continuously look for connections
while True:
    conn, addr = s.accept() #store any incoming connections and their addresses
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,currentPlayer))
    # update when new connection added
    currentPlayer += 1
    print("Player: ", currentPlayer)

