# Stockholm

## Introduction to ﬁle manipulation by creating a harmless malware

### Requirements

```bash
make
Do the following command:
source ./venv/bin/activate
pip3 install -r requirements.txt
```


### Run - crypt

At run, the program will probably override (crypt) some files in ~/infection/.

So do it carefully.

```bash
python3 stockholm.py
...
<my_super_key>
```

The key will be print at the end of the program.

### Run - decrypt

```bash
python3 stockholm.py -r <my_super_key>
```

Well done, all your files are back.

### Options

```
-h, --help            display the help
-v, --version         show the version of the program
-r, --reverse KEYFILE reverse the infection with the key entered as an argument
-s, --silent          not show each encrypted ﬁle during the process
```
