import sys
import ipaddress
import re
import signal
from pylibpcap import get_iface_list, send_packet, sniff
import uuid
import socket

IFACE='eth0'

OP_REQUEST=1
OP_REPLY=2
ARP_PORT=219

class InquisitorException(Exception):
    pass

def get_ip(arg: str):
    try:
        ip = ipaddress.ip_address(arg)
        if isinstance(ip, ipaddress.IPv6Address):
            raise InquisitorException(f"{arg} not a valid address ipv4")
        return ip
    except Exception as e:
        raise InquisitorException(f"{arg} not a valid address ipv4")

def get_mac(arg:str):
    try:
        if re.match("^[0-9a-f]{2}([:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", arg.lower()):
            if len(arg) == 17:
                return bytes.fromhex("".join(arg.split(":")))
    except Exception as e:
        raise InquisitorException(f"{arg} not a mac address -- {e}")
    raise InquisitorException(f"{arg} not a mac address")

def padding(data: bytes, length: int):
    if len(data) < length:
        data = data + b"\x00" * (length - len(data))
    return data

class ARP:
    hardware_type: int
    protocole_type: int
    hardware_len: int
    protocole_len: int
    operation: int
    sender_hardware_addr: bytes
    sender_protocole_addr: bytes
    target_hardware_addr: bytes
    target_protocole_addr: bytes


    def __init__(self):
        pass

    def create_request(self, src_ip: ipaddress.IPv4Address, src_mac: bytes, dst_ip: ipaddress.IPv4Address):
        self.hardware_type: int = 1
        self.protocole_type: int = 0x0800
        self.hardware_len: int = 6
        self.protocole_len: int = 4
        self.operation: int = OP_REQUEST
        self.sender_hardware_addr = src_mac
        self.sender_protocole_addr = src_ip.packed
        self.target_hardware_addr = b""
        self.target_protocole_addr = dst_ip.packed
    
    def dump_data(self, endian = "big"):
        hardware_type = self.hardware_type.to_bytes(2, endian)
        protocole_type = self.protocole_type.to_bytes(2, endian)
        hardware_len = self.hardware_len.to_bytes(1, endian)
        protocole_len = self.protocole_len.to_bytes(1, endian)
        operation = self.operation.to_bytes(2, endian)
        sender_hardware_addr = padding(self.sender_hardware_addr, 6)
        sender_protocole_addr = padding(self.sender_protocole_addr, 4)
        target_hardware_addr = padding(self.target_hardware_addr, 6)
        target_protocole_addr = padding(self.target_protocole_addr, 4)
        return (
            hardware_type
            + protocole_type
            + hardware_len
            + protocole_len
            + operation
            + sender_hardware_addr
            + sender_protocole_addr
            + target_hardware_addr
            + target_protocole_addr
        )

def get_my_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return ipaddress.IPv4Address(IPAddr)

def send_arp_request(ip: str, mac_addr: str):
    pass



def main(argv: list[str]):
    if len(argv) != 5:
        raise InquisitorException("need 4 arguments")
    ip_src = get_ip(argv[1])
    mac_src = get_mac(argv[2])
    ip_target = get_ip(argv[3])
    mac_target = get_mac(argv[4])
    my_mac_addr = uuid.getnode().to_bytes(6, "big")
    my_ip_addr = get_my_ip()
    print("me", my_ip_addr, my_mac_addr)
    print("src", ip_src, mac_src)
    print("target", ip_target, mac_target)
    iface = get_iface_list()
    if IFACE not in iface:
        raise InquisitorException(f"interface {IFACE} not found")
    arp = ARP()
    arp.create_request(my_ip_addr, my_mac_addr, ip_src)
    data = arp.dump_data()
    print(data, len(data))
    send_packet(IFACE, data)
    arp.create_request(my_ip_addr, my_mac_addr, ip_target)
    data = arp.dump_data()
    print(data, len(data))
    send_packet(IFACE, data)
    sniffobj = None

    # try:
    #     sniffobj = sniff(IFACE, filters=f"port {ARP_PORT}", count=1, promisc=0, out_file="pcap.pcap")

    #     for plen, t, buf in sniffobj:
    #         print("[+]: Payload len=", plen)
    #         print("[+]: Time", t)
    #         print("[+]: Payload", buf)
    # except KeyboardInterrupt:
    #     pass
    # except Exception as e:
    #     print(e)
    # for plen, t, buf in sniff(IFACE, filters=f"port {ARP_PORT}", count=-1, promisc=1, out_file="pcap.pcap"):
    #     print("[+]: Payload len=", plen)
    #     print("[+]: Time", t)
    #     print("[+]: Payload", buf)


def usage():
    print("""
python3 inquisitor.py <IP-src> <MAC-src> <IP-target> <SRC-target>
""")

def signal_handler(signum, frame):
    print("Ctrl+C caught! Exiting gracefully...")
    # TODO restore ARP table
    sys.exit(0)

if __name__ == '__main__':
    try:
        # signal.signal(signal.SIGINT, signal_handler)
        main(sys.argv)
    except InquisitorException as e:
        print(f"Error : {e}")
        usage()
