# import modules
import struct
import socket

ICMP_STRUCTURE_FMT = '!BBH'
IP_PACK = "BBHHHBBH4s4s"
IP_PACKET_SIZE = 20
ICMP_HEADER_SIZE = 4
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 15

ICMP_CODE = socket.getprotobyname('icmp')
ERROR_DESCR = {
    1: ' - Note that ICMP messages can only be '
       'sent from processes running as root.',
    10013: ' - Note that ICMP messages can only be sent by'
           ' users or processes with administrator rights.'
    }


class ICMPPacket:
    def __init__(self,
        icmp_type: int = ICMP_ECHO_REQUEST,
        icmp_code: int = 0,
        icmp_chks: int = 0,
        data: bytes    = ''  ,
        ):

        self.icmp_type = icmp_type
        self.icmp_code = icmp_code
        self.icmp_chks = icmp_chks
        #self.data      = bytes(data, encoding="utf-8")
        self.data      = data
        self.raw = None
        self.create_icmp_field()

    def create_icmp_field(self):
        self.raw = struct.pack(ICMP_STRUCTURE_FMT,
            self.icmp_type,
            self.icmp_code,
            self.icmp_chks,
            )

        # calculate checksum
        self.icmp_chks = self.checksum(self.raw+self.data)

        self.raw = struct.pack(ICMP_STRUCTURE_FMT,
            self.icmp_type,
            self.icmp_code,
            self.icmp_chks,
            ) + self.data

        return 

    def checksum(self, source):
        sum = 0
        countTo = (len(source)/2)*2
        count = 0
        while count<countTo -1:
            thisVal = source[count + 1]*256 + source[count]
            sum = sum + thisVal
            sum = sum & 0xffffffff
            count = count + 2

        if countTo<len(source):
            sum = sum + source[len(source) - 1]
            sum = sum & 0xffffffff 

        sum = (sum >> 16)  +  (sum & 0xffff)
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff

        answer = answer >> 8 | (answer << 8 & 0xff00)

        return answer


# ICMP HEADER Extraction
def parse_icmp_packet(data) -> ICMPPacket:
    icmp_header = data[IP_PACKET_SIZE:IP_PACKET_SIZE + ICMP_HEADER_SIZE]
    icmph=struct.unpack(ICMP_STRUCTURE_FMT, icmp_header)
    header={
    "type"  :   icmph[0],
    "code"  :   icmph[1],
    "checksum": icmph[2],
    }
    return ICMPPacket(header['type'], header['code'], header['checksum'], data[IP_PACKET_SIZE + ICMP_HEADER_SIZE:])

