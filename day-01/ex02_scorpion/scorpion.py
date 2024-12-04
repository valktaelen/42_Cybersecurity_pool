import sys
import os
import time
import PIL.Image
from PIL.ExifTags import TAGS, GPSTAGS

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

class ScorpionException(Exception):
    pass

def get_val(text: str, val):
    ret = f"{text}"
    if isinstance(val, dict):
        ret += "\n"
        if text == "GPSInfo":
            ret += ("\n".join([f"\t{GPSTAGS[k]} {val[k]}" for k in val.keys()]))
    else:
        ret += f" {val}"
    return ret


class Scorpion:
    path: str

    def __init__(self, path: str):
        print("#########################################")
        if path.endswith(".jpeg") or path.endswith(".jpg") or path.endswith(".gif") or path.endswith(".bmp") or path.endswith(".png"):
            self.path = path
        else:
            raise ScorpionException(f"{path} have no .jpeg .jpg .gif .bmp extensions")

    def run(self):
        print(self.path)
        try:
            img = PIL.Image.open(self.path)
        except Exception as err:
            raise ScorpionException(err)
        try:
            print(f"created: {time.ctime(os.path.getctime(self.path))}")
            print(f"modified: {time.ctime(os.path.getmtime(self.path))}")
            print(f"access: {time.ctime(os.path.getatime(self.path))}")
        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
        if hasattr(img, 'size'):
            print(f"Size: {img.size}")
        if hasattr(img, 'width'):
            print(f"Width: {img.width}")
        if hasattr(img, 'height'):
            print(f"Height: {img.height}")
        if hasattr(img, 'is_animated'):
            print(f"Is_animated: {img.is_animated}")
        exif_data = img.getexif()._get_merged_dict()
        keys = list(exif_data.keys())
        keys = [k for k in keys if k in TAGS]
        print("\n".join([f"{get_val(TAGS[k], exif_data[k])}" for k in keys]))

def main():
    for arg in sys.argv[1:]:
        try:
            scorpion = Scorpion(arg)
            scorpion.run()
        except ScorpionException as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")


if __name__ == '__main__':
    main()
