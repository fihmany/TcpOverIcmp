# import modules
import struct
import socket

ICMP_STRUCTURE_FMT = 'BBH'
IP_PACK = "BBHHHBBH4s4s"
IP_PACKET_SIZE = 20
ICMP_HEADER_SIZE = 4
ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris.

ICMP_CODE = socket.getprotobyname('icmp')
ERROR_DESCR = {
    1: ' - Note that ICMP messages can only be '
       'sent from processes running as root.',
    10013: ' - Note that ICMP messages can only be sent by'
           ' users or processes with administrator rights.'
    }


class ICMPPacket:
    def __init__(self,
        icmp_type = ICMP_ECHO_REQUEST,
        icmp_code = 0,
        icmp_chks = 0,
        data      = '' ,
        ):

        self.icmp_type = icmp_type
        self.icmp_code = icmp_code
        self.icmp_chks = icmp_chks
        self.data      = bytes(data, encoding="utf-8")
        self.raw = None
        self.create_icmp_field()

    def create_icmp_field(self):
        self.raw = struct.pack(ICMP_STRUCTURE_FMT,
            self.icmp_type,
            self.icmp_code,
            self.icmp_chks,
            )

        # calculate checksum
        self.icmp_chks = self.chksum(self.raw+self.data)

        self.raw = struct.pack(ICMP_STRUCTURE_FMT,
            self.icmp_type,
            self.icmp_code,
            self.icmp_chks,
            ) + self.data

        return 

    def chksum(self, msg):
        s = 0       # Binary Sum
        msg = str(msg)
        # loop taking 2 characters at a time
        for i in range(0, len(msg), 2):

            a = ord(msg[i]) 
            b = ord(msg[i+1])
            s = s + (a+(b << 8))
            
        
        # One's Complement
        s = s + (s >> 16)
        s = ~s & 0xffff

        return s


# ICMP HEADER Extraction
def ext_icmp_header(data):
    icmph=struct.unpack(ICMP_STRUCTURE_FMT, data)
    data={
    'type'  :   icmph[0],
    "code"  :   icmph[1],
    "checksum": icmph[2],
    }
    return data