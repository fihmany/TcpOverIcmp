import socket
from common.icmp import ICMPPacket, parse_icmp_packet, ICMP_ECHO_REQUEST, ICMP_ECHO_REPLY

def main():
    print("Hello Server")

    target_addr = "www.example.com"
    target_addr_tuple = (target_addr, 80)
    icmp_client_add = ("127.0.0.1", 5353)

    icmp_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    icmp_sock.bind(icmp_client_add)

    icmp_packet_max = 65535

    while True:
        print ("waiting for icmp packet")
        # Receive data from the icmp client
        data, addr = icmp_sock.recvfrom(icmp_packet_max)
        print (data)
        # Print the received packet hex
        icmp_packet = parse_icmp_packet(data)
        if (icmp_packet.icmp_type != ICMP_ECHO_REQUEST):
            continue
        
        #print("Received Hex: ", data.hex())
        #print("Received Data Len: ", len(data))
        #print("Request Header", icmp_packet.raw)
        #print("Request Payload: ", icmp_packet.data)

        # Access the target address and send the received icmp payload to it
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect(target_addr_tuple)

        # send the data to it
        data_to_send = icmp_packet.data.replace(b"localhost:9999", "{}:80".format(target_addr).encode("utf-8"))
        tcp_sock.send(data_to_send)
        tcp_resposnse = tcp_sock.recv(icmp_packet_max)

        print("Response from target: ", tcp_resposnse)
        
        # Format data as icmp packet and send it back to the icmp client
        icmp_packet = ICMPPacket(icmp_type=ICMP_ECHO_REPLY, data=tcp_resposnse)
        icmp_sock.sendto(icmp_packet.raw, icmp_client_add)

        # create tcp client

if __name__ == "__main__":
    main()