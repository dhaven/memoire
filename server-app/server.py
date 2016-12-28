import boto3
import socket
import sys

client = boto3.client('s3')
ret = client.create_bucket(Bucket='memoirebuckettest')
print ret

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 8888)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)
Listen = True
while Listen:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >> sys.stderr, 'connection from', client_address
        file = open("imagefile.png", 'wb')
        # Receive the data in small chunks and write to file
        while True:
            data = connection.recv(1024)
            if not data:
                print >> sys.stderr, 'no more data from', client_address
                file.close()
                client.upload_file("imagefile.png","memoirebuckettest","imagefile.png")
                break
            else:
                file.write(data)

    finally:
        # Clean up the connection
        connection.close()
        sock.close()
        Listen = False