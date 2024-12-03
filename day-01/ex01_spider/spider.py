import sys
import os
import requests
from lxml import html

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

def usage():
    print ("""
USAGE:
./spider [-rlp] URL
-r          recursively downloads the images in a URL received as a parameter
-r -l [N]   indicates the maximum depth level of the recursive download. If not indicated, it will be 5
-p [PATH]   indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
""")

def get_real_url(relative: str, cur_url: str):
    ret: str | None = None
    if relative.startswith("#"):
        ret = None
    elif relative == ".":
        ret = None
    elif relative.find("://") != -1:
        ret = relative
    elif relative.startswith("//"):
        ret = "https:" + relative
    elif relative.startswith("/"):
        ret = get_base_url(cur_url) + relative
    elif cur_url.endswith("/"):
        ret = cur_url + relative
    else:
        i_end_path = cur_url.rfind("/")
        cur_dir = cur_url[:i_end_path]
        if i_end_path < cur_url.find("://")+3:
            cur_dir = get_base_url(cur_url)
        ret = cur_dir + "/" + relative
    if ret is not None:
        ret = ret.replace("/./", "/")
    return ret


def get_base_url(url: str):
    i = url.find("/", len("https://"))
    if i == -1:
        return url
    return url[:i]

def get_main_domain(url1:str):
    base1 = get_base_url(url1)
    fst1 = base1.rfind(".")
    if fst1 != -1:
        fst1 = base1.rfind(".", 0, fst1)
    if fst1 != -1:
        base1 = base1[fst1 + 1:]
    else:
        base1 = base1[base1.find("://") + 3:]
    return base1

def get_page_urls(cur_url: str, r: requests.Response):
    new_urls = []
    try:
        root = html.fromstring(r.content)
        urls = root.xpath("//a[@href]")
        for url in urls:
            href = url.get("href")
            if href.startswith("mailto:") or href.startswith("tel:"):
                continue
            url_abs = get_real_url(href, cur_url)
            if url_abs is not None:
                new_urls.append(url_abs)
    except Exception as err:
        print(f"{bcolors.WARNING}{cur_url} : Urls not found {err}{bcolors.ENDC}")
    return new_urls

def get_page_img(url: str, r: requests.Response):
    new_imgs = []
    try:
        root = html.fromstring(r.content)
        imgs = root.xpath("//img[@src]")
        for img in imgs:
            img_url = img.get("src")
            img_abs = get_real_url(img_url, url)
            if img_abs is not None:
                new_imgs.append(img_abs)
    except Exception as err:
        print(f"{bcolors.WARNING}{url} : Image not found {err}{bcolors.ENDC}")
        return []
    return new_imgs

class SpiderException(Exception):
    pass
class Spider:
    recursive: int
    level: int
    path: str
    url: str
    done: list[str]
    n_img: int
    main_domain: str

    def __init__(self, recursive = False, level = 5, path = "./data/", url = None):
        self.recursive = recursive
        self.level = level
        self.path = path
        self.url = url
        self.n_img = 0
        self.done = []

    def parsing(self, argv: list[str]):
        level_data = False
        path_data = False
        for arg in argv:
            if self.url is not None:
                print (f"{bcolors.FAIL}All parameters after url are ignored{bcolors.ENDC}")
                break
            elif level_data:
                try:
                    self.level = int(arg)
                except:
                    raise SpiderException("level parametter not an integer")
                if self.level < 1:
                    raise SpiderException("level parametter < 1")
                level_data = False
            elif path_data:
                self.path = arg
                path_data = False
            elif arg == '-r':
                self.recursive = True
            elif arg == "-l":
                level_data = True
            elif arg == "-p":
                path_data = True
            else:
                self.url = arg
        if level_data:
            raise SpiderException("level parametter missing")
        if path_data:
            raise SpiderException("path parametter missing")
        if self.url is None:
            raise SpiderException("URL missing")
        self.main_domain = get_main_domain(self.url)
        self.path += "/"

    def create_dir(self):
        try:
            os.mkdir(self.path)
            print(f"{bcolors.OKCYAN}Directory '{self.path}' created successfully.{bcolors.ENDC}")
        except FileExistsError:
            print("Dir already exists")
        except Exception as e:
            raise SpiderException(f"Create dir {self.path}: {e}")

    def run_one_page(self, level: int = None, url: str = None):
        if level is None:
            level = self.level if self.recursive else 0
        if url is None:
            url = self.url
        if url in self.done:
            return
        if self.main_domain != get_main_domain(url):
            return
        self.done.append(url)
        t = 0
        code = 0
        urls: list[str] = []
        imgs: list[str] = []
        try:
            r = requests.get(url)
            code = r.status_code
            t = r.elapsed.total_seconds()
            urls =  get_page_urls(url, r)
            imgs =  get_page_img(url, r)
            r.close()
        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
        print(f"status code {bcolors.OKGREEN if (code >= 200 and code < 300) else bcolors.WARNING}{code:03d}{bcolors.ENDC} | ref {len(urls):04d} | img {len(imgs):04d} | time {t:.6f}s | {url}")
        for img in imgs:
            # print(get_main_domain(img), self.main_domain)
            if img in self.done or get_main_domain(img) != self.main_domain:
                continue
            self.done.append(img)
            if img.endswith(".jpg") or img.endswith(".jpeg") or img.endswith(".png") or img.endswith(".gif") or img.endswith(".bmp"):
                name = self.path + img[img.find("://") + 3:]
                dir = name[:img.rfind("/")]
                try:
                    r = requests.get(img, allow_redirects=True)
                    if r.status_code == 200:
                        os.makedirs(dir, exist_ok=True)
                        file = open(name, 'wb')
                        file.write(r.content)
                        print(f"{bcolors.OKBLUE}{name}{bcolors.ENDC}")
                        self.n_img += 1
                        file.close()
                    r.close()
                except FileExistsError:
                    r.close()
                except OSError as e:
                    r.close()
                    raise SpiderException(f"Create dir {dir}: {e}")
                except Exception as err:
                    print(f"{bcolors.WARNING}Fail to write '{name}'.{bcolors.ENDC}")
                    file.close()
        if level > 0:
            for url in urls:
                if url not in self.done:
                    self.run_one_page(level - 1, url)

    def run(self, argv: list[str]):
        self.parsing(argv)
        self.create_dir()
        self.run_one_page()


    def __str__(self):
        return f"""
Spider :
    recursive {self.recursive}
    level     {self.level}
    path      {self.path}
    url       {self.url}
    n_img     {self.n_img}
    done      {len(self.done)} url done
        """

def main():
    spider = Spider()
    try:
        spider.run(sys.argv[1:])

    except SpiderException as err:
        print(f"{bcolors.FAIL}Error: {err}{bcolors.ENDC}")
        print(spider)
        usage()
        sys.exit(1)
    except Exception as err:
        print(f"{bcolors.FAIL}Error: -- {err}{bcolors.ENDC}")
    print(spider)

if __name__ == '__main__':
    main()
