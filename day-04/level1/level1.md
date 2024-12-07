```asm
000011c0 <main>:
    11c0:       55                      push   ebp
    11c1:       89 e5                   mov    ebp,esp
    11c3:       53                      push   ebx
    11c4:       81 ec 84 00 00 00       sub    esp,0x84
    11ca:       e8 00 00 00 00          call   11cf <main+0xf>
    11cf:       5b                      pop    ebx
    11d0:       81 c3 31 2e 00 00       add    ebx,0x2e31
    11d6:       89 5d 80                mov    DWORD PTR [ebp-0x80],ebx
    11d9:       c7 45 f8 00 00 00 00    mov    DWORD PTR [ebp-0x8],0x0
    11e0:       8b 83 08 e0 ff ff       mov    eax,DWORD PTR [ebx-0x1ff8]
    11e6:       89 45 86                mov    DWORD PTR [ebp-0x7a],eax
    11e9:       8b 83 0c e0 ff ff       mov    eax,DWORD PTR [ebx-0x1ff4]
    11ef:       89 45 8a                mov    DWORD PTR [ebp-0x76],eax
    11f2:       8b 83 10 e0 ff ff       mov    eax,DWORD PTR [ebx-0x1ff0]
    11f8:       89 45 8e                mov    DWORD PTR [ebp-0x72],eax
    11fb:       66 8b 83 14 e0 ff ff    mov    ax,WORD PTR [ebx-0x1fec]
    1202:       66 89 45 92             mov    WORD PTR [ebp-0x6e],ax
    1206:       8d 83 16 e0 ff ff       lea    eax,[ebx-0x1fea]
    120c:       89 04 24                mov    DWORD PTR [esp],eax
    120f:       e8 4c fe ff ff          call   1060 <printf@plt>
    1214:       8b 5d 80                mov    ebx,DWORD PTR [ebp-0x80]
    1217:       8d 45 94                lea    eax,[ebp-0x6c]
    121a:       8d 8b 29 e0 ff ff       lea    ecx,[ebx-0x1fd7]
    1220:       89 0c 24                mov    DWORD PTR [esp],ecx
    1223:       89 44 24 04             mov    DWORD PTR [esp+0x4],eax
    1227:       e8 44 fe ff ff          call   1070 <__isoc99_scanf@plt>
    122c:       8b 5d 80                mov    ebx,DWORD PTR [ebp-0x80]
    122f:       8d 4d 94                lea    ecx,[ebp-0x6c]
    1232:       8d 55 86                lea    edx,[ebp-0x7a]
    1235:       89 e0                   mov    eax,esp
    1237:       89 50 04                mov    DWORD PTR [eax+0x4],edx
    123a:       89 08                   mov    DWORD PTR [eax],ecx
    123c:       e8 ff fd ff ff          call   1040 <strcmp@plt>
    1241:       83 f8 00                cmp    eax,0x0
    1244:       0f 85 16 00 00 00       jne    1260 <main+0xa0>
    124a:       8b 5d 80                mov    ebx,DWORD PTR [ebp-0x80]
    124d:       8d 83 2c e0 ff ff       lea    eax,[ebx-0x1fd4]
    1253:       89 04 24                mov    DWORD PTR [esp],eax
    1256:       e8 05 fe ff ff          call   1060 <printf@plt>
    125b:       e9 11 00 00 00          jmp    1271 <main+0xb1>
    1260:       8b 5d 80                mov    ebx,DWORD PTR [ebp-0x80]
    1263:       8d 83 37 e0 ff ff       lea    eax,[ebx-0x1fc9]
    1269:       89 04 24                mov    DWORD PTR [esp],eax
    126c:       e8 ef fd ff ff          call   1060 <printf@plt>
    1271:       31 c0                   xor    eax,eax
    1273:       81 c4 84 00 00 00       add    esp,0x84
    1279:       5b                      pop    ebx
    127a:       5d                      pop    ebp
    127b:       c3                      ret 
```

```bash
gdb level1
(gdb) b *main+0x7c
Breakpoint 1 at 0x123c
(gdb) r
Please enter key: lol
Breakpoint 1, 0x5655623c in main ()
(gdb) disas
   0x56556235 <+117>:   mov    %esp,%eax
   0x56556237 <+119>:   mov    %edx,0x4(%eax)
   0x5655623a <+122>:   mov    %ecx,(%eax)
=> 0x5655623c <+124>:   call   0x56556040 <strcmp@plt>
   0x56556241 <+129>:   cmp    $0x0,%eax
(gdb) p (char *) $edx
$1 = 0xffffcace "__stack_check"
(gdb) p (char *) $ecx
$2 = 0xffffcadc "lol"
```

```bash
gdb level1 -ex 'set disassembly-flavor intel' -ex 'b*main+0x7c' -ex r -ex disas -ex 'p (char *) $edx' -ex 'p (char *) $ecx' --batch <<EOF
lol
EOF
```

```bash
./level1 
Please enter key: __stack_check
Good job.
```
