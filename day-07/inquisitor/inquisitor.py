import sys
import ipaddress
import re
import signal

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
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", arg.lower()):
            return arg
    except Exception as e:
        raise InquisitorException(f"{arg} not a mac address -- {e}")
    raise InquisitorException(f"{arg} not a mac address")


def main(argv: list[str]):
    if len(argv) != 5:
        raise InquisitorException("need 4 arguments")
    ip_src = get_ip(argv[1])
    mac_src = get_mac(argv[2])
    ip_target = get_ip(argv[3])
    mac_target = get_mac(argv[4])


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
        signal.signal(signal.SIGINT, signal_handler)
        main(sys.argv)
    except InquisitorException as e:
        print(f"Error : {e}")
        usage()
