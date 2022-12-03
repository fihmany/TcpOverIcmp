import select
import socket
from common.icmp import ICMPPacket, parse_icmp_packet, ICMP_ECHO_REQUEST, ICMP_ECHO_REPLY
from common.data_types import IcmpOverTcpPacket
from common.utils import ICMP_PACKET_MAX, TCP_PACKET_MAX


class ProxyServer:

    def __init__(self):
        # target_addr = "www.example.com"
        # target_addr_tuple = (target_addr, 80)
        self.icmp_client_addr = ("127.0.0.1", 5353)
        self.icmp_sock = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.icmp_sock.bind(self.icmp_client_addr)
        self.sockets = [self.icmp_sock]

    def server_serve(self):
        print("Hello Server")

        while True:
            ready_to_read, _, _ = select.select(self.sockets, [], [])
            for sock in ready_to_read:
                if sock.protocol == socket.IPPROTO_ICMP:
                    self.handle_icmp_packet(sock)
                else:
                    self.handle_tcp_packet(sock)

    def handle_tcp_packet(self, sock: socket.socket):
        tcp_resposnse = sock.recv(TCP_PACKET_MAX)

        # print("Response from target: ", tcp_resposnse)
        # Format data as icmp packet and send it back to the icmp client
        icmp_packet = ICMPPacket(icmp_type=ICMP_ECHO_REPLY, data=tcp_resposnse)
        self.icmp_sock.sendto(icmp_packet.raw, self.icmp_client_addr)
        if sock in self.sockets:
            sock.close()
            self.sockets.remove(sock)

    def handle_icmp_packet(self, sock: socket.socket):
        # Receive data from the icmp client
        data, _ = sock.recvfrom(ICMP_PACKET_MAX)
        # print (data)
        # Print the received packet hex
        icmp_packet = parse_icmp_packet(data)
        if (icmp_packet.icmp_type != ICMP_ECHO_REQUEST):
            return

        # Pase the data as an icmp over tcp packet
        icmp_over_tcp = IcmpOverTcpPacket()
        print("Received from icmp client: ", icmp_packet.data)
        icmp_over_tcp.parse_from_raw_data(icmp_packet.data)

        # clean target ip from trailing null bytes
        target_addr = icmp_over_tcp.target_ip.rstrip('\x00')

        # Format the data to the correct host and port
        data_to_send = icmp_over_tcp.data.replace(
            b"localhost:9999", "{}:80".format(target_addr).encode("utf-8"))

        print("Received ip icmp client: ", target_addr)

        #print("Received Hex: ", data.hex())
        #print("Received Data Len: ", len(data))
        #print("Request Header", icmp_packet.raw)
        #print("Request Payload: ", icmp_packet.data)

        # Access the target address and send the received icmp payload to it
        tcp_sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

        # TODO RAZ: mabye pass the port of connection as well ?
        tcp_sock.connect((target_addr, 80))

        # send the data to it
        tcp_sock.send(data_to_send)
        self.sockets.append(tcp_sock)


if __name__ == "__main__":
    server = ProxyServer()
    server.server_serve()
