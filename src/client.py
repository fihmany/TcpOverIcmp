from common.icmp import ICMP_ECHO_REPLY, ICMP_ECHO_REQUEST, ICMP_HEADER_SIZE, IP_PACKET_SIZE, ICMPPacket, parse_icmp_packet
from common.data_types import IcmpOverTcpPacket
import socket

def main(source_ip = "127.0.0.1", target_ip = "www.example.com", target_port = "80"):
    # Start up the gui on a seperate thread
    # TODO: pass the target ip and port to the server 
    print("Hello Client")

    # if no configuration queue is present, use the default values
    if (configuration_queue is not None):
        configuration = configuration_queue.get()
        source_ip = configuration["source_ip"]
        target_ip = configuration["target_ip"]
        target_port = configuration["target_port"]

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    icmp_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)

    tcp_client_add = ("0.0.0.0", 9999)
    icmp_server_add = (source_ip, 5353)

    tcp_packet_max = 65535
    icmp_packet_max = 65535

    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind(tcp_client_add)

    # accept a connection from the tcp client
    tcp_sock.listen(10)
    conn, addr = tcp_sock.accept()
    print("Connected to: ", addr)

    while True:
        # Receive data from tcp client
        data = conn.recv(tcp_packet_max)
        # print("Received from tcp client: ", data.decode("utf-8"))

        # Forward the icmp packet to the icmp server, but as an icmp over tcp packet
        icmp_over_tcp = IcmpOverTcpPacket(target_ip=target_ip, data=data)

        # Format data as icmp packet
        icmp = ICMPPacket(icmp_type=ICMP_ECHO_REQUEST, data=icmp_over_tcp.raw)

        print("Sending to icmp server: ", icmp_over_tcp.target_ip)
        icmp_sock.sendto(icmp.raw, icmp_server_add)
        data = None

        # Receive response from icmp server
        data, addr = icmp_sock.recvfrom(icmp_packet_max)
        data = handle_icmp(data)
        while data == None:
            data, addr = icmp_sock.recvfrom(icmp_packet_max)
            data = handle_icmp(data)
        print("Response from icmp server: ", data.data)

        # Send response to tcp client
        conn.send(data.data)
        print ("loop")
        

def handle_icmp(data: bytes) -> ICMPPacket:
    packet = parse_icmp_packet(data)
    if (packet.icmp_type != ICMP_ECHO_REPLY):
        print("received echo request! ignoring")
        return None
    return packet
 
if __name__ == "__main__":
    main()