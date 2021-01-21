import socket
UDP_IP = "fe80::7991:8af1:bd58:30f4%18"
UDP_PORT = 10037

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)