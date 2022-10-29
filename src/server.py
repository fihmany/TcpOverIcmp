import socket
import struct
from common.icmp import ICMPPacket, ext_icmp_header, IP_PACKET_SIZE, ICMP_HEADER_SIZE, ICMP_STRUCTURE_FMT

def main():
    print("Hello Server")

    sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    sock.bind(("127.0.0.1", 7))

    while True:
        # Receive data
        data, addr = sock.recvfrom(65535)
        # print the received packet hex
        icmp_pack_len = struct.calcsize(ICMP_STRUCTURE_FMT)
        print(icmp_pack_len)
        icmp = ext_icmp_header(data[IP_PACKET_SIZE:(IP_PACKET_SIZE+icmp_pack_len)])
        print("Received Hex: ", data.hex())
        # pritn data len
        print("Received Data Len: ", len(data))
        
        #struct_data = ICMPPacket(data)
        print("server" + str(icmp))
        print("Response: ", data[(IP_PACKET_SIZE+icmp_pack_len):])

        #msg = input("Enter message: ")
        #sock.sendto(str.encode(msg), ("127.0.0.1", 3232))


if __name__ == "__main__":
    main()