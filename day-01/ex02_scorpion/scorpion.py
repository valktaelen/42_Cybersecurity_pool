import datetime
import sys
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
        img = PIL.Image.open(self.path)
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