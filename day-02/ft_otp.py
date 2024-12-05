import sys
import hashlib
import pyotp
import base64
import time

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



class HMAC:
    secret: bytes
    message: bytes
    block_size: int
    digest: any

    def xor(self, b1: bytes, b2: bytes) -> bytes:
        if len(b1) < self.block_size:
            b1 = b1 + b'\x00' * (self.block_size - len(b1))
        if len(b2) < self.block_size:
            b2 = b2 + b'\x00' * (self.block_size - len(b2))
        return bytes([_a ^ _b for _a, _b in zip(b1, b2)])

    def __init__(self, secret: bytes, message: bytes, digest = hashlib.sha1):
        self.secret = secret
        self.message = message
        self.digest = digest
        self.block_size = self.digest(b"").block_size

    def derived_key(self):
        if len(self.secret) > self.block_size:
            return self.digest(self.secret).digest()
        return self.secret

    def run(self) -> bytes:
        ipad = b'\x36' * self.block_size
        opad = b'\x5c' * self.block_size
        derived_key = self.derived_key()
        ret = self.digest(
            self.xor(
                derived_key,
                opad
            )
            + self.digest(
                self.xor(
                    derived_key,
                    ipad
                )
                + self.message
            ).digest()
        )
        print(f"HMAC : {ret.hexdigest()}")
        return ret.digest()

class HOTP:
    n_digit: int
    secret_key: int
    counter: int
    digest: any


    def __init__(self, secret_key: str, counter: int, n_digit: int = 6, digest = hashlib.sha1):
        self.secret_key = base64.b32decode(secret_key, casefold=True)
        self.counter = counter
        self.n_digit = n_digit
        self.digest = digest

    def truncate(self, hmac: bytes) -> bytes:
        val = hmac
        i = val[-1] & 0xF
        extract = val[i:i+4]
        extract = (
            (extract[0] & 0x7F) << 24
            | (extract[1] & 0xFF) << 16
            | (extract[2] & 0xFF) << 8
            | (extract[3] & 0xFF)
        )
        return extract

    def run(self) -> int:
        hmac = HMAC(self.secret_key, (self.counter).to_bytes(8, byteorder="big"), digest=self.digest)
        hotp = self.truncate(hmac.run())
        return hotp % (10 ** self.n_digit)

class TOTP:
    secret_key: str
    n_digit: int
    delta_time: int
    digest: any

    def __init__(self, secret_key: str, delta_time: int = 30, n_digit: int = 6, digest = hashlib.sha1):
        self.secret_key = secret_key
        self.n_digit = n_digit
        self.delta_time = delta_time
        self.digest = digest

    def run(self):
        c: int = int(time.time() // self.delta_time)
        hotp = HOTP(self.secret_key, c, self.n_digit, digest=self.digest)
        res = hotp.run()
        print(f"HOTP value : {res}")
        return res
class OTPException(Exception):
    pass

class OTP:
    generator_file: str | None
    key_file: str | None
    digest: any

    def __init__(self):
        self.generator_file = None
        self.key_file = None
        self.digest = hashlib.sha1

    def parse(self, args: list[str]):
        generator_file: bool = False
        key_file: bool = False
        digest: bool = False
        for arg in args:
            if generator_file:
                self.generator_file = arg
                generator_file = False
            elif key_file:
                self.key_file = arg
                key_file = False
            elif digest:
                if arg == "sha1":
                    self.digest = hashlib.sha1
                elif arg == "sha224":
                    self.digest = hashlib.sha224
                elif arg == "sha256":
                    self.digest = hashlib.sha256
                elif arg == "sha512":
                    self.digest = hashlib.sha512
                elif arg == "sha384":
                    self.digest = hashlib.sha384
                elif arg == "md5":
                    self.digest = hashlib.md5
                else:
                    print(f"{arg} : digest ignored")
                digest = False
            elif arg == "-g":
                generator_file = True
            elif arg == "-k":
                key_file = True
            elif arg == "--digest":
                digest = True
            else:
                raise OTPException(f"The parameter {arg} not reconized")

    def run(self):
        if self.generator_file is not None:
            print("################ Generate key")
            try:
                with open(self.generator_file) as file:
                    hex_file = file.read()
                    hex_file = hex_file.split()
                    if len(hex_file) != 1:
                        raise OTPException(f"{self.generator_file} : not an hexadecimal")
                    hex_file = hex_file[0]
                    l = len(hex_file)
                    if l < 64:
                        raise OTPException(f"{self.generator_file} : len of hex less than 64 characters")
                    if l % 2 != 0:
                        raise OTPException(f"{self.generator_file} : not an hexadecimal")
                    hex_str = ""
                    hex_converter: dict[str, int] = {}
                    for i in range (16):
                        char = hex(i)[-1]
                        hex_converter[char] = i
                        hex_converter[char.capitalize()] = i
                    # print(hex_converter)
                    for i in range(0, l, 2):
                        fst = hex_converter.get(hex_file[i], None)
                        sec = hex_converter.get(hex_file[i+1], None)
                        if fst is None or sec is None:
                            raise OTPException(f"{self.generator_file} : not an hexadecimal")
                        byte_val = (fst << 4) + sec
                        hex_str += chr(byte_val)
                    base = base64.b32encode(bytearray(hex_str, 'utf-8'))
                    base = base.decode()
                    print("hex    ", hex_file)
                    print("str    ", hex_str)
                    print("base32 ", base)
                    with open("ft_otp.key", 'w') as key_file:
                        key_file.write(base)
            except Exception as err:
                print(err)
        if self.key_file is not None:
            print("################ TOTP")
            try:
                with open(self.key_file) as file:
                    key_file = file.read()
                    key_file = key_file.split()
                    if len(key_file) != 1:
                        raise OTPException(f"{self.generator_file} : not a key")
                    key = key_file[0]
                    totp = TOTP(key, digest=self.digest)
                    res = totp.run()
                    print(f"TOTP value : {res}")
                    # teste = pyotp.TOTP(key, digest=self.digest)
                    # print("real",teste.now())
            except Exception as err:
                print(err)

def main():
    otp = OTP()
    try:
        otp.parse(sys.argv[1:])
        otp.run()
    except OTPException as err:
        print(f"{bcolors.FAIL}Error: {err}{bcolors.ENDC}")

if __name__ == '__main__':
    main()
