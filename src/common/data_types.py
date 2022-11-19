import struct

ICMP_OVER_TCP_STRUCTURE_FMT = '!16s'

class IcmpOverTcpPacket:

    def __init__(self,
        target_ip: str = '',
        data: bytes = b'',
        ):

        self.target_ip = target_ip
        self.data = data
        self.raw = None
        self.create_icmp_over_tcp_field()

    def create_icmp_over_tcp_field(self):
        self.raw = struct.pack(ICMP_OVER_TCP_STRUCTURE_FMT,
            self.target_ip.encode("latin-1"),
            ) + self.data

        return

    def parse_from_raw_data(self, raw):
        self.raw = raw
        print("first 16 bytes: ", self.raw[:16].decode("latin-1"))
        self.target_ip = struct.unpack(ICMP_OVER_TCP_STRUCTURE_FMT, self.raw[:16])[0].decode("latin-1")
        self.data = self.raw[16:]
        return