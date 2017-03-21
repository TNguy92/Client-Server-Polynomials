import socket

#socket()
sock=socket.socket()
port = 12345
host = '127.0.0.1'
#connect()
sock.connect((host, port))
#write()


request = input("Enter The Polynomial:\n")
print("You've Entered:\n" + request)
sock.sendall(request.encode())
sock.shutdown(1)    # signal the server we're sending no more data

bytes = sock.recv(2048)
response = ""

while len(bytes)>0:
    response+=bytes.decode()
    bytes = sock.recv(2048)

print(response)

sock.close()

#read()

#close()