
```asm
00001220 <no>:
    1220:       55                      push   ebp
    1221:       89 e5                   mov    ebp,esp
    1223:       53                      push   ebx
    1224:       83 ec 14                sub    esp,0x14
    1227:       e8 00 00 00 00          call   122c <no+0xc>
    122c:       5b                      pop    ebx
    122d:       81 c3 d4 5d 00 00       add    ebx,0x5dd4
    1233:       89 5d f8                mov    DWORD PTR [ebp-0x8],ebx
    1236:       8d 83 08 b0 ff ff       lea    eax,[ebx-0x4ff8]
    123c:       89 04 24                mov    DWORD PTR [esp],eax
    123f:       e8 3c fe ff ff          call   1080 <puts@plt>
    1244:       8b 5d f8                mov    ebx,DWORD PTR [ebp-0x8]
    1247:       c7 04 24 01 00 00 00    mov    DWORD PTR [esp],0x1
    124e:       e8 3d fe ff ff          call   1090 <exit@plt>
    1253:       90                      nop
    1254:       90                      nop
    1255:       90                      nop
    1256:       90                      nop
    1257:       90                      nop
    1258:       90                      nop
    1259:       90                      nop
    125a:       90                      nop
    125b:       90                      nop
    125c:       90                      nop
    125d:       90                      nop
    125e:       90                      nop
    125f:       90                      nop

...

000012a0 <ok>:
    12a0:       55                      push   ebp
    12a1:       89 e5                   mov    ebp,esp
    12a3:       53                      push   ebx
    12a4:       50                      push   eax
    12a5:       e8 00 00 00 00          call   12aa <ok+0xa>
    12aa:       5b                      pop    ebx
    12ab:       81 c3 56 5d 00 00       add    ebx,0x5d56
    12b1:       8d 83 11 bd ff ff       lea    eax,[ebx-0x42ef]
    12b7:       89 04 24                mov    DWORD PTR [esp],eax
    12ba:       e8 c1 fd ff ff          call   1080 <puts@plt>
    12bf:       83 c4 04                add    esp,0x4
    12c2:       5b                      pop    ebx
    12c3:       5d                      pop    ebp
    12c4:       c3                      ret    
    12c5:       90                      nop
    12c6:       90                      nop
    12c7:       90                      nop
    12c8:       90                      nop
    12c9:       90                      nop
    12ca:       90                      nop
    12cb:       90                      nop
    12cc:       90                      nop
    12cd:       90                      nop
    12ce:       90                      nop
    12cf:       90                      nop

000012d0 <main>:
    12d0:       55                      push   ebp
    12d1:       89 e5                   mov    ebp,esp
    12d3:       53                      push   ebx
    12d4:       83 ec 54                sub    esp,0x54
    12d7:       e8 00 00 00 00          call   12dc <main+0xc>
    12dc:       5b                      pop    ebx
    12dd:       81 c3 24 5d 00 00       add    ebx,0x5d24
    12e3:       89 5d c0                mov    DWORD PTR [ebp-0x40],ebx
    12e6:       c7 45 f8 00 00 00 00    mov    DWORD PTR [ebp-0x8],0x0
    12ed:       8d 83 1b bd ff ff       lea    eax,[ebx-0x42e5]
    12f3:       89 04 24                mov    DWORD PTR [esp],eax
    12f6:       e8 65 fd ff ff          call   1060 <printf@plt>
    12fb:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    12fe:       8d 45 cb                lea    eax,[ebp-0x35]
    1301:       8d 8b 2e bd ff ff       lea    ecx,[ebx-0x42d2]
    1307:       89 0c 24                mov    DWORD PTR [esp],ecx
    130a:       89 44 24 04             mov    DWORD PTR [esp+0x4],eax
    130e:       e8 ad fd ff ff          call   10c0 <__isoc99_scanf@plt>
    1313:       89 45 f4                mov    DWORD PTR [ebp-0xc],eax
    1316:       b8 01 00 00 00          mov    eax,0x1
    131b:       3b 45 f4                cmp    eax,DWORD PTR [ebp-0xc]
    131e:       0f 84 08 00 00 00       je     132c <main+0x5c>
    1324:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    1327:       e8 f4 fe ff ff          call   1220 <no>
    132c:       0f be 4d cc             movsx  ecx,BYTE PTR [ebp-0x34]
    1330:       b8 30 00 00 00          mov    eax,0x30
    1335:       39 c8                   cmp    eax,ecx
    1337:       0f 84 08 00 00 00       je     1345 <main+0x75>
    133d:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    1340:       e8 db fe ff ff          call   1220 <no>
    1345:       0f be 4d cb             movsx  ecx,BYTE PTR [ebp-0x35]
    1349:       b8 30 00 00 00          mov    eax,0x30
    134e:       39 c8                   cmp    eax,ecx
    1350:       0f 84 08 00 00 00       je     135e <main+0x8e>
    1356:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    1359:       e8 c2 fe ff ff          call   1220 <no>
    135e:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    1361:       8b 83 f4 ff ff ff       mov    eax,DWORD PTR [ebx-0xc]
    1367:       8b 00                   mov    eax,DWORD PTR [eax]
    1369:       8b 8b f4 ff ff ff       mov    ecx,DWORD PTR [ebx-0xc]
    136f:       89 04 24                mov    DWORD PTR [esp],eax
    1372:       e8 f9 fc ff ff          call   1070 <fflush@plt>
    1377:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    137a:       8d 45 e3                lea    eax,[ebp-0x1d]
    137d:       31 c9                   xor    ecx,ecx
    137f:       89 04 24                mov    DWORD PTR [esp],eax
    1382:       c7 44 24 04 00 00 00    mov    DWORD PTR [esp+0x4],0x0
    1389:       00 
    138a:       c7 44 24 08 09 00 00    mov    DWORD PTR [esp+0x8],0x9
    1391:       00 
    1392:       e8 19 fd ff ff          call   10b0 <memset@plt>
    1397:       c6 45 e3 64             mov    BYTE PTR [ebp-0x1d],0x64
    139b:       c6 45 ca 00             mov    BYTE PTR [ebp-0x36],0x0
    139f:       c7 45 ec 02 00 00 00    mov    DWORD PTR [ebp-0x14],0x2
    13a6:       c7 45 f0 01 00 00 00    mov    DWORD PTR [ebp-0x10],0x1
    13ad:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    13b0:       8d 4d e3                lea    ecx,[ebp-0x1d]
    13b3:       89 e0                   mov    eax,esp
    13b5:       89 08                   mov    DWORD PTR [eax],ecx
    13b7:       e8 e4 fc ff ff          call   10a0 <strlen@plt>
    13bc:       89 c1                   mov    ecx,eax
    13be:       31 c0                   xor    eax,eax
    13c0:       83 f9 08                cmp    ecx,0x8
    13c3:       88 45 bf                mov    BYTE PTR [ebp-0x41],al
    13c6:       0f 83 22 00 00 00       jae    13ee <main+0x11e>             ;; (8)len(buf2) >= 8
    13cc:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    13cf:       8b 45 ec                mov    eax,DWORD PTR [ebp-0x14]
    13d2:       89 45 b8                mov    DWORD PTR [ebp-0x48],eax
    13d5:       8d 4d cb                lea    ecx,[ebp-0x35]
    13d8:       89 e0                   mov    eax,esp
    13da:       89 08                   mov    DWORD PTR [eax],ecx
    13dc:       e8 bf fc ff ff          call   10a0 <strlen@plt>
    13e1:       89 c1                   mov    ecx,eax
    13e3:       8b 45 b8                mov    eax,DWORD PTR [ebp-0x48]
    13e6:       39 c8                   cmp    eax,ecx
    13e8:       0f 92 c0                setb   al
    13eb:       88 45 bf                mov    BYTE PTR [ebp-0x41],al
    13ee:       8a 45 bf                mov    al,BYTE PTR [ebp-0x41]
    13f1:       a8 01                   test   al,0x1                          ;; al == 1
    13f3:       0f 85 05 00 00 00       jne    13fe <main+0x12e>
    13f9:       e9 4c 00 00 00          jmp    144a <main+0x17a>               ;;; ok path
    13fe:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    1401:       8b 45 ec                mov    eax,DWORD PTR [ebp-0x14]
    1404:       8a 44 05 cb             mov    al,BYTE PTR [ebp+eax*1-0x35]
    1408:       88 45 c7                mov    BYTE PTR [ebp-0x39],al
    140b:       8b 45 ec                mov    eax,DWORD PTR [ebp-0x14]
    140e:       8a 44 05 cc             mov    al,BYTE PTR [ebp+eax*1-0x34]
    1412:       88 45 c8                mov    BYTE PTR [ebp-0x38],al
    1415:       8b 45 ec                mov    eax,DWORD PTR [ebp-0x14]
    1418:       8a 44 05 cd             mov    al,BYTE PTR [ebp+eax*1-0x33]
    141c:       88 45 c9                mov    BYTE PTR [ebp-0x37],al
    141f:       8d 45 c7                lea    eax,[ebp-0x39]
    1422:       89 04 24                mov    DWORD PTR [esp],eax
    1425:       e8 a6 fc ff ff          call   10d0 <atoi@plt>
    142a:       88 c1                   mov    cl,al
    142c:       8b 45 f0                mov    eax,DWORD PTR [ebp-0x10]
    142f:       88 4c 05 e3             mov    BYTE PTR [ebp+eax*1-0x1d],cl
    1433:       8b 45 ec                mov    eax,DWORD PTR [ebp-0x14]
    1436:       83 c0 03                add    eax,0x3
    1439:       89 45 ec                mov    DWORD PTR [ebp-0x14],eax
    143c:       8b 45 f0                mov    eax,DWORD PTR [ebp-0x10]
    143f:       83 c0 01                add    eax,0x1
    1442:       89 45 f0                mov    DWORD PTR [ebp-0x10],eax
    1445:       e9 63 ff ff ff          jmp    13ad <main+0xdd>
    144a:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    144d:       8b 45 f0                mov    eax,DWORD PTR [ebp-0x10]
    1450:       c6 44 05 e3 00          mov    BYTE PTR [ebp+eax*1-0x1d],0x0
    1455:       8d 4d e3                lea    ecx,[ebp-0x1d]
    1458:       8d 93 33 bd ff ff       lea    edx,[ebx-0x42cd]
    145e:       89 e0                   mov    eax,esp
    1460:       89 50 04                mov    DWORD PTR [eax+0x4],edx
    1463:       89 08                   mov    DWORD PTR [eax],ecx
    1465:       e8 d6 fb ff ff          call   1040 <strcmp@plt>
    146a:       83 f8 00                cmp    eax,0x0
    146d:       0f 85 0d 00 00 00       jne    1480 <main+0x1b0>
    1473:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    1476:       e8 25 fe ff ff          call   12a0 <ok>
    147b:       e9 08 00 00 00          jmp    1488 <main+0x1b8>
    1480:       8b 5d c0                mov    ebx,DWORD PTR [ebp-0x40]
    1483:       e8 98 fd ff ff          call   1220 <no>
    1488:       31 c0                   xor    eax,eax
    148a:       83 c4 54                add    esp,0x54
    148d:       5b                      pop    ebx
    148e:       5d                      pop    ebp
    148f:       c3                      ret    

...

```

```bash
gdb --batch -ex 'b *main+0x3e' -ex r -ex 'p (char *) $ecx' -ex 'p (char*)*((char **) $esp)' level2
```

==> scanf("%23s", buf)


```bash
gdb --batch -ex 'b *main+0x4b' -ex r -ex 'p $eax' -ex 'p *((int *)($ebp - 0xc))' level2
```

==> scanf("%23s", buf) == 1


```bash
gdb --batch -ex 'b *main+0x65' -ex r -ex 'p $eax' -ex 'p (char *)($ebp-0x34)' -ex 'p $ecx' level2 <<EOF
abcdefg
EOF
```

==> 0x30 == 48 == buf[1]
48 == "0"

Donc buf = "*0*****..."

```bash
gdb --batch -ex 'b *main+0x7e' -ex r -ex 'p $eax' -ex 'p (char *)($ebp-0x35)' -ex 'p $ecx' level2 <<EOF
a0cdefg
EOF
```
==> 0x30 == 48 == "0" == buf[0]

Donc buf = "00*****..."


```bash
gdb --batch -ex 'b *main+0x7e' -ex r -ex 'p (char *)($ebp-0x35)' -ex 'b *main+0xa2' -ex c -ex 'p/x $eax' -ex 'p/x $ecx' -ex 'b *main+0xc2' -ex c -ex 'p (char *)$eax' level2 <<EOF
00cdefg
EOF
```

0xa2 = fflush
0xc2 = memset

buf1[23] = input
buf2[9]

memset(buf2, 0, 9)


```bash
gdb --batch -ex 'b *main+0x7e' -ex r -ex 'p (char *)($ebp-0x35)' -ex 'b *main+0xa2' -ex c -ex 'p/x $eax' -ex 'p/x $ecx' -ex 'b *main+0xc2' -ex c -ex 'p (char *)$eax' level2 <<EOF
00cdefg
EOF
```


0xe7 = strlen
0xf0 = cmp

```bash
gdb --batch -ex 'b *main+0x15a' -ex r -ex 'p $al' -ex 'p (char *)($ebp-0x39)' -ex c -ex 'p $al' -ex 'p (char *)($ebp-0x39)' -ex c -ex 'p $al' -ex 'p (char *)($ebp-0x39)' -ex c -ex 'p $al' -ex 'p (char *)($ebp-0x39)' -ex c -ex 'p $al' -ex 'p (char *)($ebp-0x39)'  -ex c -ex 'p $al' -ex 'p (char *)($ebp-0x39)' -ex c -ex 'p $al' -ex 'p (char *)($ebp-0x39)' -ex c -ex 'p $al' -ex 'p (char *)($ebp-0x39)' -ex c -ex 'p $al' -ex 'p (char *)($ebp-0x39)' -ex c -ex 'p $al' -ex 'p (char *)($ebp-0x39)' level2 <<EOF
00101108097098101114101
EOF
```
0x15a = atoi

```bash
gdb --batch -ex 'b *main+0x163' -ex r -ex 'p *((int*)($ebp+$eax-0x1d))' -ex 'p/u $cl' -ex c -ex 'p *((int*)($ebp+$eax-0x1d))' -ex 'p/u $cl' level2 <<EOF
00142097
EOF
```

