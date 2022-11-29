from common.icmp import ICMP_ECHO_REPLY, ICMP_ECHO_REQUEST, ICMP_HEADER_SIZE, IP_PACKET_SIZE, ICMPPacket, parse_icmp_packet
from common.data_types import IcmpOverTcpPacket, QUIT_COMMAND
import socket
from queue import Queue

def has_received_quit_command(in_queue: Queue) -> bool:
    # if the quit command is in the queue, quit
    if (not in_queue.empty()):
        print("received a command")
        data = in_queue.get()
        if (data == QUIT_COMMAND):
            print("received the quit command")
            return True
    return False

def main(source_ip = "127.0.0.1", target_ip = "www.example.com", target_port = "80",
         in_queue = Queue(), out_queue = Queue()):
    # Start up the gui on a seperate thread
    # TODO: pass the target ip and port to the server 
    print("Hello Client")

    # print up the received parameters for debugging
    print("source ip: " + source_ip)
    print("target ip: " + target_ip)
    print("target port: " + target_port)

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    icmp_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)

    tcp_client_add = ("0.0.0.0", 9999)
    icmp_server_add = (source_ip, 5353)

    tcp_packet_max = 65535
    icmp_packet_max = 65535

    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.settimeout(0.2) # timeout for listening

    tcp_sock.bind(tcp_client_add)

    # accept a connection from the tcp client
    tcp_sock.listen(10)

    try: 
        conn, addr = tcp_sock.accept(timeout=1)
    except socket.timeout:
        print("connection timeout")
        has_received_quit_command(in_queue)
        return

    print("Connected to: ", addr)

    while True:
        # Receive data from tcp client
        data = conn.recv(tcp_packet_max, timeout=1)

        print("checking the in queue")
        # if there is no data, check if there is data in the queue 
        if (len(data) == 0):
            has_received_quit_command(in_queue)
            continue

        # print("Received from tcp client: ", data.decode("utf-8"))

        # Forward the icmp packet to the icmp server, but as an icmp over tcp packet
        icmp_over_tcp = IcmpOverTcpPacket(target_ip=target_ip, data=data)

        # Format data as icmp packet
        icmp = ICMPPacket(icmp_type=ICMP_ECHO_REQUEST, data=icmp_over_tcp.raw)

        # Log the packet being sent for display in the gui
        out_queue.put(("packet_out", len(icmp.raw)))

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