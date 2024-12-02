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

def get_url(body: str, base_url: str):
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
    if url.startswith("https"):
        return url
    if url.startswith("/"):
        return base_url + url
    return base_url + "/" + url

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

def get_url_img(body: str, base_url: str):
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
                return get_url(body[i+len("src"):], base_url)
    return None



def get_base_url(url: str):
    i = url.find("/", len("https://"))
    if i == -1:
        return url
    return url[:i]

def get_page_urls(url: str):
    r = requests.get(url)
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
        new_url = get_url(body[i+len(symbol):], get_base_url(url))
        if new_url is not None:
            new_urls.append(new_url)
    return new_urls

def get_page_img(url: str):
    r = requests.get(url)
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
        new_url = get_url_img(body[i+len(symbol):], get_base_url(url))
        if new_url is not None:
            new_urls.append(new_url)
    return new_urls

class SpiderException(Exception):
    pass
class Spider:
    recursive: int
    level: int
    path: str
    url: str

    def __init__(self, recursive = False, level = 5, path = "./data/", url = None):
        self.recursive = recursive
        self.level = level
        self.path = path
        self.url = url
    
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
        urls = get_page_urls(url)
        imgs = get_page_img(url)
        print("urls")
        print(urls)
        print("img")
        print(imgs)
        if level > 1:
            for url in urls:
                self.run_one_page(level, url)
        for img in imgs:
            name = self.path + img[img.find("://") + 3:]
            dir = name[:img.rfind("/")]
            try:
                os.makedirs(dir, exist_ok=True)
                print(f"Directory '{dir}' created successfully.")
            except FileExistsError:
                pass
            except Exception as e:
                raise SpiderException(f"Create dir {dir}: {e}")
            r = requests.get(img, allow_redirects=True)
            open(name, 'wb').write(r.content)

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

    except SpiderException as err:
        print("Error: ", err)
        usage()
        sys.exit(1)

if __name__ == '__main__':
    main()
