import socket
import struct
from common.icmp import ICMPPacket, ext_icmp_header, IP_PACKET_SIZE, ICMP_HEADER_SIZE, ICMP_STRUCTURE_FMT

def main():
    print("Hello Server")

    target_addr = "https://raw.githubusercontent.com/fihmany/TcpOverIcmp/main/README.md"
    target_addr_tuple = (target_addr, 80)
    icmp_client_add = ("127.0.0.1", 5353)

    icmp_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)

    icmp_packet_max = 65535

    while True:
        # Receive data from the icmp client
        data, addr = icmp_sock.recvfrom(icmp_packet_max)
        
        # Print the received packet hex
        icmp_len = struct.calcsize(ICMP_STRUCTURE_FMT)
        icmp_header = ext_icmp_header(data[IP_PACKET_SIZE:(IP_PACKET_SIZE+icmp_len)])
        icmp_payload = data[(IP_PACKET_SIZE+icmp_len):]
        
        print("Received Hex: ", data.hex())
        print("Received Data Len: ", len(data))
        print("Request Header", icmp_header)
        print("Request Payload: ", icmp_payload)

        # Access the target address and send the received icmp payload to it
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect(target_addr_tuple)

        # send the data to it
        tcp_sock.send(icmp_payload)
        tcp_resposnse = tcp_sock.recv(icmp_packet_max)
        
        # Format data as icmp packet and send it back to the icmp client
        icmp_packet = ICMPPacket(data=tcp_resposnse)
        icmp_sock.sendto(icmp_packet.raw, icmp_client_add)




if __name__ == "__main__":
    main()