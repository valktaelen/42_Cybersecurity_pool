import sys
import os
import requests
from lxml import html

def usage():
    print ("""
USAGE:
./spider [-rlp] URL
-r          recursively downloads the images in a URL received as a parameter
-r -l [N]   indicates the maximum depth level of the recursive download. If not indicated, it will be 5
-p [PATH]   indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
""")

def get_real_url(relative: str, cur_url: str):
    if relative.startswith("#"):
        return None
    if relative.find("://") != -1:
        return relative
    if relative.startswith("/"):
        return get_base_url(cur_url) + relative
    if cur_url.rfind("/") < cur_url.rfind("."):
        i_end_path = cur_url.rfind("/")
        if i_end_path < cur_url.find("://")+3:
            cur_dir = get_base_url(cur_url)
        else:
            cur_dir = cur_url[:i_end_path]
        return cur_dir + "/" + relative
    return cur_url + "/" + relative


def get_base_url(url: str):
    i = url.find("/", len("https://"))
    if i == -1:
        return url
    return url[:i]

def get_page_urls(cur_url: str, r: requests.Response):
    root = html.fromstring(r.content)
    urls = root.xpath("//a[@href]")
    new_urls = []
    for url in urls:
        href = url.get("href")
        url_abs = get_real_url(href, cur_url)
        if url_abs is not None:
            new_urls.append(url_abs)
    return new_urls

def get_page_img(url: str, r: requests.Response):
    root = html.fromstring(r.content)
    imgs = root.xpath("//img[@src]")
    new_imgs = []
    for img in imgs:
        img_url = img.get("src")
        img_abs = get_real_url(img_url, url)
        if img_abs is not None:
            new_imgs.append(img_abs)
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

    def __init__(self, recursive = False, level = 5, path = "./data/", url = None):
        self.recursive = recursive
        self.level = level
        self.path = path
        self.url = url
        self.n_img = 0
        self.done = []
    
    def parsing(self, argv):
        level_data = False
        path_data = False
        for arg in argv:
            if self.url is not None:
                print ("All parameters after url are ignored")
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
    
    def create_dir(self):
        try:
            os.mkdir(self.path)
            print(f"Directory '{self.path}' created successfully.")
        except FileExistsError:
            print("Dir already exists")
        except Exception as e:
            raise SpiderException(f"Create dir {self.path}: {e}")
    
    def run_one_page(self, level: int = None, url: str = None):
        if level is None:
            level = self.level if self.recursive else 1
        if url is None:
            url = self.url
        if url in self.done:
            return
        # if get_base_url(url) != get_base_url(self.url):
        #     return
        self.done.append(url)
        r = requests.get(url)
        urls: list[str] =  get_page_urls(url, r)
        imgs: list[str] =  get_page_img(url, r)
        r.close()
        print(f"{url} | ref {len(urls)} | img {len(imgs)}")
        for img in imgs:
            img = img.replace("/./", "/")
            if img in self.done:
                continue
            self.done.append(img)
            if img.endswith(".jpg") or img.endswith(".jpeg") or img.endswith(".png") or img.endswith(".gif") or img.endswith(".bmp"):
                name = self.path + img[img.find("://") + 3:]
                print(name)
                dir = name[:img.rfind("/")]
                try:
                    r = requests.get(img, allow_redirects=True)
                    if r.status_code == 200:
                        os.makedirs(dir, exist_ok=True)
                        file = open(name, 'wb')
                        file.write(r.content)
                        self.n_img += 1
                        file.close()
                    r.close()
                except FileExistsError:
                    r.close()
                except OSError as e:
                    r.close()
                    raise SpiderException(f"Create dir {dir}: {e}")
                except Exception as err:
                    print(f"Fail to write '{name}'.")
                    file.close()
        if level > 1:
            for url in urls:
                if url not in self.done:
                    url = url.replace("/./", "/")
                    self.run_one_page(level - 1, url)


    def print(self):
        print("recursive : ", self.recursive)
        print("level : ", self.level)
        print("path : ", self.path)

def main():
    spider = Spider()
    try:
        spider.parsing(sys.argv[1:])
        spider.print()
        spider.create_dir()
        spider.run_one_page()
        print("num img: ",spider.n_img)
        print("num url: ", len(spider.done))

    except SpiderException as err:
        print("Error: ", err)
        usage()
        sys.exit(1)

if __name__ == '__main__':
    main()
