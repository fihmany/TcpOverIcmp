from common.icmp import ICMPPacket
import socket

def main():

    print("Hello Client")
    sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)

    #while True:
    #msg = input("Enter message: ")
    msg = "Hello World"
    icmp = ICMPPacket(data=msg)
    
    sock.sendto(icmp.raw, ("127.0.0.1", 7))

    # Receive data
    #data, addr = sock.recvfrom(65535)
    #print("Response: ", data)

if __name__ == "__main__":
    main()