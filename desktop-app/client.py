import socket
import sys
import Tkinter

class Client:
    def __init__(self,address):
        self.connectToServer(address)

    def connectToServer(self,address):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        self.server_address = (address, 8888)
        print >> sys.stderr, 'connecting to %s port %s' % self.server_address
        self.sock.connect(self.server_address)

    def sendDataToServer(self,filename):
        try:
            # Send data
            file = open(filename, 'rb')
            somedata = file.read(1024)
            print >> sys.stderr, 'sending file'
            while (somedata):
                self.sock.sendall(somedata)
                somedata = file.read(1024)
            file.close()
            print >> sys.stderr, 'file sent'

        finally:
            print >> sys.stderr, 'closing socket'
            self.sock.close()