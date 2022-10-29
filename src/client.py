from common.icmp import ICMPPacket
import socket

def main():
    print("Hello Client")

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    icmp_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)

    tcp_client_add = ("0.0.0.0", 9999)
    icmp_server_add = ("0.0.0.0", 5353)
    icmp = ICMPPacket(data=b"test")
    icmp_sock.sendto(icmp.raw, icmp_server_add)

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
        icmp = ICMPPacket(data=data)
        icmp_sock.sendto(icmp.raw, icmp_server_add)

        # Receive response from icmp server
        data, addr = icmp_sock.recvfrom(icmp_packet_max)
        print("Response from icmp server: ", data)

        # Send response to tcp client
        conn.send(data)


if __name__ == "__main__":
    main()