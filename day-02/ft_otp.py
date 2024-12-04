import sys
from hashlib import sha1

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
import binascii



class HMAC:
    secret: bytes
    message: bytes
    block_size: int

    def xor(self, b1: bytes, b2: bytes) -> bytes:
        if len(b1) < self.block_size:
            b1 = b1 + (0).to_bytes(1, byteorder="little") * (self.block_size - len(b1))
        if len(b2) < self.block_size:
            b2 = b2 + (0).to_bytes(1, byteorder="little") * (self.block_size - len(b2))
        return bytes([_a ^ _b for _a, _b in zip(b1, b2)])

    def concate(self, b1: bytes, b2: bytes) -> bytes:
        a1 = bytearray(b1)
        a2 = bytearray(b2)
        a1.extend(a2)
        return bytes(a1)

    def __init__(self, secret: bytes, message: bytes, block_size: int = 64):
        self.secret = secret
        self.message = message
        self.block_size = block_size

    def derived_key(self):
        if len(self.secret) > self.block_size:
            return sha1(self.secret).digest()
        return self.secret

    def run(self):
        print("opad", binascii.hexlify(self.opad()))
        print("ipad", binascii.hexlify(self.ipad()))
        key_out = self.xor(self.derived_key(), self.opad())
        key_in = self.xor(self.derived_key(), self.ipad())
        concat_in = self.concate(key_in, self.message)
        sha_in = sha1(concat_in).digest()
        to_hash = self.concate(key_out, sha_in)
        print("opad", self.opad())
        print("ipad", self.ipad())
        print("key_out", key_out)
        print("key_in", key_in)
        print("concat_in", concat_in)
        print("sha_in", sha_in)
        print("to_hash", to_hash)
        return sha1(to_hash).hexdigest()

    def ipad(self):
        unit: bytes = (0x36).to_bytes(1, byteorder="little")
        return unit * self.block_size

    def opad(self):
        unit: bytes = (0x5c).to_bytes(1, byteorder="little")
        return unit * self.block_size

class OTPException(Exception):
    pass

class OTP:
    generator_file: str | None
    key_file: str | None

    def __init__(self):
        self.generator_file = None
        self.key_file = None

    def parse(self, args: list[str]):
        generator_file: bool = False
        key_file: bool = False
        for arg in args:
            if generator_file:
                self.generator_file = arg
                generator_file = False
            elif key_file:
                self.key_file = arg
                key_file = False
            elif arg == "-g":
                generator_file = True
            elif arg == "-k":
                key_file = True
            else:
                raise OTPException(f"The parameter {arg} not reconized")

    def run(self):
        #TODO open files
        # hmac = HMAC(str.encode("l" * 64), (54).to_bytes(8, byteorder="little"))
        # hmac.run()
        hmac = HMAC(str.encode("key"), str.encode("The quick brown fox jumps over the lazy dog"))
        hmac = hmac.run()
        print(hmac)

def main():
    otp = OTP()
    try:
        otp.parse(sys.argv[1:])
        otp.run()
    except OTPException as err:
        print(f"{bcolors.FAIL}Error: {err}{bcolors.ENDC}")

if __name__ == '__main__':
    main()
