import sys
from hashlib import sha1
import pyotp
import os
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
import binascii



class HMAC:
    secret: bytes
    message: bytes
    block_size: int

    def xor(self, b1: bytes, b2: bytes) -> bytes:
        if len(b1) < self.block_size:
            b1 = b1 + b'\x00' * (self.block_size - len(b1))
        if len(b2) < self.block_size:
            b2 = b2 + b'\x00' * (self.block_size - len(b2))
        return bytes([_a ^ _b for _a, _b in zip(b1, b2)])

    def __init__(self, secret: bytes, message: bytes):
        self.secret = secret
        self.message = message
        self.block_size = sha1(b"").block_size

    def derived_key(self):
        if len(self.secret) > self.block_size:
            return sha1(self.secret).digest()
        return self.secret

    def run(self) -> bytes:
        ipad = b'\x36' * self.block_size
        opad = b'\x5c' * self.block_size
        derived_key = self.derived_key()
        ret = sha1(
            self.xor(
                derived_key,
                opad
            )
            + sha1(
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


    def __init__(self, secret_key: str, counter: int, n_digit: int = 6):
        self.secret_key = base64.b32decode(secret_key, casefold=True)
        self.counter = counter
        self.n_digit = n_digit

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
        hmac = HMAC(self.secret_key, (self.counter).to_bytes(8, byteorder="big"))
        hotp = self.truncate(hmac.run())
        return hotp % (10 ** self.n_digit)

class TOTP:
    def __init__(self, secret_key: str, delta_time: int = 30, n_digit: int = 6):
        self.secret_key = secret_key
        self.n_digit = n_digit
        self.delta_time = delta_time
    
    def run(self):
        c: int = int(time.time() // self.delta_time)
        hotp = HOTP(self.secret_key, c, self.n_digit)
        res = hotp.run()
        print(f"HOTP value : {res}")
        return res
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
        a="ONZXG43TONZXG43TONZXG43TONZXG43TONZXG43TONZXG43TONZXG43TONZXG43TONZXG43TONZXG43TONZXG43TONZXG43TONZXG4Y="
        teste = pyotp.HOTP(a, digest=sha1)
        print("real",teste.at(0))
        print("#########")
        totp = TOTP(a)
        res = totp.run()
        print(f"TOTP value : {res}")

def main():
    otp = OTP()
    try:
        otp.parse(sys.argv[1:])
        otp.run()
    except OTPException as err:
        print(f"{bcolors.FAIL}Error: {err}{bcolors.ENDC}")

if __name__ == '__main__':
    main()
