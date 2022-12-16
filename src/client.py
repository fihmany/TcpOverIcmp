import select
from socket import socket, AF_INET, SOCK_RAW, IPPROTO_ICMP, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout
from queue import Queue

from common.icmp import ICMP_ECHO_REPLY, ICMP_ECHO_REQUEST, ICMPPacket, parse_icmp_packet
from common.data_types import IcmpOverTcpPacket, QUIT_COMMAND
from common.utils import ICMP_PACKET_MAX, TCP_PACKET_MAX, STOP_COMMAND

class ProxyClient:
    def __init__(self, source_ip: str = "127.0.0.1", target_ip:
                 str = "www.example.com", target_port: str = "80",
                 in_queue: Queue = Queue(), out_queue: Queue = Queue()):
        self.source_ip = source_ip
        self.target_ip = target_ip
        self.target_port = target_port
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.sockets = []
        self.current_tcp_session = None
        self.in_session = False
        self.icmp_server_addr = (self.source_ip, 5353)
        self.icmp_sock = socket(
            AF_INET, SOCK_RAW, IPPROTO_ICMP)
        self.tcp_server_sock = socket(
            AF_INET, SOCK_STREAM)
        self.tcp_server_sock.setsockopt(
            SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcp_server_sock.settimeout(0.2)  # timeout for listening
        self.tcp_server_sock.bind(("0.0.0.0", 9999))

    def client_serve(self):
        # Start up the gui on a seperate thread
        print("Hello Client")

        # print up the received parameters for debugging
        print("source ip: " + self.source_ip)
        print("target ip: " + self.target_ip)
        print("target port: " + self.target_port)
        self.in_session = True

        while self.in_session:
            # accept a connection from the tcp client
            self.tcp_server_sock.listen(10)

            try:
                self.current_tcp_session, addr = self.tcp_server_sock.accept()
            except timeout:
                #print("connection timeout")
                self.has_received_quit_command(self.in_queue)
                continue

            print("Connected to: ", addr)
            # Receive data from tcp client
            self.sockets = [self.current_tcp_session, self.icmp_sock]
            while self.current_tcp_session is not None:
                # use select to fill the ready_to_read list with sockets that have data to read

                ready_to_read, _, _ = select.select(
                    self.sockets, [], [], 0.2)                
                for sock in ready_to_read:
                    if sock == self.icmp_sock:
                        self.handle_icmp_packet(sock)
                    else:
                        if (self.handle_tcp_packet(sock) == STOP_COMMAND):
                            self.current_tcp_session = None

            print("loop")

    def handle_icmp_packet(self, sock: socket):
         # Receive response from icmp server
        data = None
        data, _ = sock.recvfrom(ICMP_PACKET_MAX)
        data = ProxyClient.handle_icmp(data)
        while data is None:
            data, _ = sock.recvfrom(ICMP_PACKET_MAX)
            data = ProxyClient.handle_icmp(data)
        print("Response from icmp server: ", data.data)

        # Send response to tcp client
        self.current_tcp_session.send(data.data)

    def handle_tcp_packet(self, sock: socket):
        data = sock.recv(TCP_PACKET_MAX)
    
        print("checking the in queue")
        # if there is no data, check if there is data in the queue
        if (len(data) == 0):
            self.has_received_quit_command(self.in_queue)
            return STOP_COMMAND

        # print("Received from tcp client: ", data.decode("utf-8"))

        # Forward the icmp packet to the icmp server, but as an icmp over tcp packet
        icmp_proxy_message = IcmpOverTcpPacket(
            target_ip=self.target_ip, data=data)

        # Format data as icmp packet
        icmp_packet = ICMPPacket(icmp_type=ICMP_ECHO_REQUEST,
                            data=icmp_proxy_message.raw)

        # Log the packet being sent for display in the gui
        self.out_queue.put(("packet_out", len(icmp_packet.raw)))

        print("Sending to icmp server: ", icmp_proxy_message.target_ip)
        self.icmp_sock.sendto(icmp_packet.raw, self.icmp_server_addr)

    @staticmethod
    def handle_icmp(data: bytes) -> ICMPPacket:
        packet = parse_icmp_packet(data)
        if packet.icmp_type != ICMP_ECHO_REPLY:
            print("received echo request! ignoring")
            return None
        return packet

    def has_received_quit_command(self, in_queue: Queue) -> bool:
        # if the quit command is in the queue, quit
        if not in_queue.empty():
            print("received a command")
            data = in_queue.get()
            if data == QUIT_COMMAND:
                print("received the quit command")
                self.in_session = False
                return True
        return False


if __name__ == "__main__":
    client = ProxyClient()
    client.client_serve()
