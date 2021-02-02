import socket
import bsm
from Vehicle import Vehicle

def udp_receive():
    UDP_IP = "fe80::7991:8af1:bd58:30f4%18"
    UDP_PORT = 10037

    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)

def udp_send(message):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 52001
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message, (UDP_IP, UDP_PORT))


if __name__ == "__main__":
    v = Vehicle()
    v.send_message()