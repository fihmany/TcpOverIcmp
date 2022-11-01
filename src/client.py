from common.icmp import ICMP_ECHO_REPLAY, ICMP_ECHO_REQUEST, ICMP_HEADER_SIZE, IP_PACKET_SIZE, ICMPPacket, parse_icmp_packet
import socket

def main():
    print("Hello Client")

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    icmp_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)

    tcp_client_add = ("0.0.0.0", 9999)
    icmp_server_add = ("127.0.0.1", 5353)

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
        print("Received from tcp client: ", data.decode("utf-8"))

        # Format data as icmp packet and send to icmp server
        icmp = ICMPPacket(icmp_type=ICMP_ECHO_REQUEST, data=data)
        icmp_sock.sendto(icmp.raw, icmp_server_add)
        data = None

        # Receive response from icmp server
        data, addr = icmp_sock.recvfrom(icmp_packet_max)
        data = handle_icmp(data)
        while data == None:
            data, addr = icmp_sock.recvfrom(icmp_packet_max)
            data = handle_icmp(data)
        print("Response from icmp server: ", data)

        # Send response to tcp client
        conn.send(data)
        print ("loop")
        break

def handle_icmp(data: bytes) -> bytes:
    packet = parse_icmp_packet(data)
    if (packet.icmp_type != ICMP_ECHO_REPLAY):
        return None
    return data

if __name__ == "__main__":
    main()