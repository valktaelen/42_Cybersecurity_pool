import sys
import os
import requests

def usage():
    print ("")
    print ("USAGE: ")
    print ("./spider [-rlp] URL")
    print ("-r\t recursively downloads the images in a URL received as a parameter")
    print ("-r -l [N]\tindicates the maximum depth level of the recursive download. If not indicated, it will be 5")
    print ("-p [PATH]\t indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.")

def get_url(body: str, base_url: str, cur_url: str):
    equal = False
    i_begin = -1
    i_end = -1
    for i, c in enumerate(body):
        if not equal:
            if c != ' ' and c != '=':
                return None
            if c == '=':
                equal = True
        elif i_begin == -1:
            if c != ' ' and c != '"':
                return None
            if c == '"':
                i_begin = i
        elif i_begin and c == '"':
            i_end = i
            break
    if i_begin == -1 or i_end == -1:
        return None
    url = body[i_begin + 1:i_end]
    if url.startswith("#"):
        return None
    if url.find("://") != -1:
        return url
    if url.startswith("/"):
        return base_url + url
    if cur_url.rfind("/") < cur_url.rfind("."):
        i_end_path = cur_url.rfind("/")
        if i_end_path < cur_url.find("://")+3:
            cur_dir = base_url
        else:
            cur_dir = cur_url[:i_end_path]
        return cur_dir + "/" + url
    return cur_url + "/" + url


def get_end_img_balise(html: str):
    in_quote = False
    in_simp_quote = False
    for i, c in enumerate(html):
        if c == '"':
            if not in_quote and not in_simp_quote:
                in_quote = True
            elif in_quote:
                in_quote = False
        elif c == '\'':
            if not in_quote and not in_simp_quote:
                in_simp_quote = True
            elif in_simp_quote:
                in_simp_quote = False
        elif not in_quote and not in_simp_quote:
            if c == '>':
                return i
    return -1

def get_url_img(body: str, base_url: str, url: str):
    end = get_end_img_balise(body)
    if end == -1:
        return None
    body = body[:end]
    in_quote = False
    in_simp_quote = False
    for i, c in enumerate(body):
        if c == '"':
            if not in_quote and not in_simp_quote:
                in_quote = True
            elif in_quote:
                in_quote = False
        elif c == '\'':
            if not in_quote and not in_simp_quote:
                in_simp_quote = True
            elif in_simp_quote:
                in_simp_quote = False
        elif not in_quote and not in_simp_quote:
            i_src = body.startswith("src", i)
            if i_src:
                return get_url(body[i+len("src"):], base_url, url)
    return None



def get_base_url(url: str):
    i = url.find("/", len("https://"))
    if i == -1:
        return url
    return url[:i]

def get_page_urls(url: str, r: requests.Response):
    body = r.text
    symbol="href"
    indexs = []
    i = 0
    i_tmp = 0
    while i_tmp != -1:
        i_tmp = body[i:].find(symbol)
        i += i_tmp
        if i != -1:
            indexs.append(i)
        i += 1
    new_urls = []
    for i in indexs:
        new_url = get_url(body[i+len(symbol):], get_base_url(url), url)
        if new_url is not None:
            i_sharp = new_url.rfind("#")
            if i_sharp != -1:
                i_next = new_url.rfind("/")
                if i_next == -1:
                    new_url = new_url[:i_sharp]
                elif i_sharp < i_next:
                    new_url = new_url[:i_sharp] + new_url[i_next:]
            new_urls.append(new_url)
    return new_urls

def get_page_img(url: str, r: requests.Response):
    body = r.text
    symbol="img"
    indexs = []
    i = 0
    i_tmp = 0
    while i_tmp != -1:
        i_tmp = body[i:].find(symbol)
        i += i_tmp
        if i != -1:
            indexs.append(i)
        i += 1
    new_urls = []
    for i in indexs:
        new_url = get_url_img(body[i+len(symbol):], get_base_url(url), url)
        if new_url is not None:
            i_sharp = new_url.rfind("#")
            if i_sharp != -1:
                i_next = new_url.rfind("/")
                if i_next == -1:
                    new_url = new_url[:i_sharp]
                elif i_sharp < i_next:
                    new_url = new_url[:i_sharp] + new_url[i_next:]
            new_urls.append(new_url)
    return new_urls

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
        if get_base_url(url) != get_base_url(self.url):
            return
        self.done.append(url)
        urls = []
        imgs: list[str] = []
        try:
            r = requests.get(url)
            urls = get_page_urls(url, r)
            imgs = get_page_img(url, r)
            r.close()
        except Exception as err:
            return
        print(url)
        # print("urls", urls)
        # print("imgs", imgs)
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
