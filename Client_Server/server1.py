import socket
import logging
import polynomials
port=12345

def multiply1 (a, b):
    return a*b;

logging.basicConfig(level=logging.ERROR)

#socket()
listener=socket.socket()
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bind(): Ip address with port number
listener.bind(('127.0.0.1', port))
#listen()
listener.listen(0)
#accept()

while True:
    (sock , addr) = listener.accept()  ## waits for a connection request
                                       # when successful, returns a socket
                                       # to use to communicate with the client
    #read()
    logging.debug("Server connected to:"+str(addr))
    bytes = sock.recv(2048)

    client_data = ""
    # get data from the client
    while len(bytes) > 0:
        client_data += bytes.decode()
        bytes = sock.recv(2048)

    # parse and process the data from the client

    if client_data[0] == 'E':
        try:
            print("Received Data Before Splitting: " + client_data)
            list_of_parts = client_data.split(' ')
            print("Data After Split: " + str(list_of_parts))
            xVal = float(list_of_parts[0][1:])
            poly = list(map(int, list_of_parts[1:]))
            result = polynomials.evaluate(xVal, poly)
            print("Evaluate Polynomial Calculation Completed: " + str(result))
        except:
            # signal an error
            # error response
            response_status = 'X:'
            response_message = ' Invalid Format Numeric Data to Evaluate!'
            logging.error(response_message)
    elif client_data[0] == 'S':
        try:
            print("Received Data Before Splitting: " + client_data)
            list_of_parts = client_data.split(' ')
            print("Data After Split: " + str(list_of_parts))
            aVal = int(list_of_parts[0][1:])
            bVal = int(list_of_parts[1])
            polyBisec = list(map(int, list_of_parts[2:-1]))
            tol = float(list_of_parts[-1])
            print("a: " + str(aVal) + "\nb: " + str(bVal) + "\nPoly: " + str(polyBisec) + "\nTolerance: " + str(tol))
            result = polynomials.bisection(aVal, bVal, polyBisec, tol)
            print("Bisection calculation completed: " + str(result))
        except:
            # signal an error
            # error response
            response_status = 'X:'
            response_message = ' Invalid Format Numeric Data For Bisection Function!'
            logging.error(response_message)
    else:
        try:
            # try to convert the two value to int
            # compute them and create a correct response
            result = multiply1(int(list_of_parts[0]), int(list_of_parts[1]))
            response_status = 'B'
            response_message = str(result)
        except:
            # signal a conversion or computation problem
            # error response
            response_status = 'E'
            response_message = 'Conversion or computation problem '
            logging.error(response_message)

        #write()
        message = response_status + response_message
        response_bytes=message.encode()
        sock.sendall(response_bytes)
    sock.shutdown(1)  #signal close of the writing the socket
    # close()
    sock.close()