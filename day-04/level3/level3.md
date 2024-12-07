
```asm

00000000000012e0 <___syscall_malloc>:
    12e0:       55                      push   rbp
    12e1:       48 89 e5                mov    rbp,rsp
    12e4:       48 8d 3d 48 0d 00 00    lea    rdi,[rip+0xd48]        # 2033 <_IO_stdin_used+0x33>
    12eb:       e8 40 fd ff ff          call   1030 <puts@plt>
    12f0:       bf 01 00 00 00          mov    edi,0x1
    12f5:       e8 b6 fd ff ff          call   10b0 <exit@plt>
    12fa:       66 0f 1f 44 00 00       nop    WORD PTR [rax+rax*1+0x0]

0000000000001300 <____syscall_malloc>:
    1300:       55                      push   rbp
    1301:       48 89 e5                mov    rbp,rsp
    1304:       48 8d 3d 2e 0d 00 00    lea    rdi,[rip+0xd2e]        # 2039 <_IO_stdin_used+0x39>
    130b:       e8 20 fd ff ff          call   1030 <puts@plt>
    1310:       5d                      pop    rbp
    1311:       c3                      ret    
    1312:       66 2e 0f 1f 84 00 00    cs nop WORD PTR [rax+rax*1+0x0]
    1319:       00 00 00 
    131c:       0f 1f 40 00             nop    DWORD PTR [rax+0x0]

0000000000001320 <main>:
    1320:       55                      push   rbp
    1321:       48 89 e5                mov    rbp,rsp
    1324:       48 83 ec 60             sub    rsp,0x60
    1328:       c7 45 fc 00 00 00 00    mov    DWORD PTR [rbp-0x4],0x0
    132f:       48 8d 3d 0d 0d 00 00    lea    rdi,[rip+0xd0d]        # 2043 <_IO_stdin_used+0x43>
    1336:       b0 00                   mov    al,0x0
    1338:       e8 13 fd ff ff          call   1050 <printf@plt>
    133d:       48 8d 75 c0             lea    rsi,[rbp-0x40]
    1341:       48 8d 3d 0e 0d 00 00    lea    rdi,[rip+0xd0e]        # 2056 <_IO_stdin_used+0x56>
    1348:       b0 00                   mov    al,0x0
    134a:       e8 51 fd ff ff          call   10a0 <__isoc99_scanf@plt>
    134f:       89 45 f8                mov    DWORD PTR [rbp-0x8],eax
    1352:       b8 01 00 00 00          mov    eax,0x1
    1357:       3b 45 f8                cmp    eax,DWORD PTR [rbp-0x8]
    135a:       0f 84 05 00 00 00       je     1365 <main+0x45>
    1360:       e8 7b ff ff ff          call   12e0 <___syscall_malloc>
    1365:       0f be 4d c1             movsx  ecx,BYTE PTR [rbp-0x3f]
    1369:       b8 32 00 00 00          mov    eax,0x32
    136e:       39 c8                   cmp    eax,ecx
    1370:       0f 84 05 00 00 00       je     137b <main+0x5b>
    1376:       e8 65 ff ff ff          call   12e0 <___syscall_malloc>
    137b:       0f be 4d c0             movsx  ecx,BYTE PTR [rbp-0x40]
    137f:       b8 34 00 00 00          mov    eax,0x34
    1384:       39 c8                   cmp    eax,ecx
    1386:       0f 84 05 00 00 00       je     1391 <main+0x71>
    138c:       e8 4f ff ff ff          call   12e0 <___syscall_malloc>
    1391:       48 8b 05 48 2c 00 00    mov    rax,QWORD PTR [rip+0x2c48]        # 3fe0 <stdin@GLIBC_2.2.5>
    1398:       48 8b 38                mov    rdi,QWORD PTR [rax]
    139b:       e8 e0 fc ff ff          call   1080 <fflush@plt>
    13a0:       48 8d 7d df             lea    rdi,[rbp-0x21]
    13a4:       31 f6                   xor    esi,esi
    13a6:       ba 09 00 00 00          mov    edx,0x9
    13ab:       e8 b0 fc ff ff          call   1060 <memset@plt>
    13b0:       c6 45 df 2a             mov    BYTE PTR [rbp-0x21],0x2a
    13b4:       c6 45 bf 00             mov    BYTE PTR [rbp-0x41],0x0
    13b8:       48 c7 45 e8 02 00 00    mov    QWORD PTR [rbp-0x18],0x2
    13bf:       00 
    13c0:       c7 45 f4 01 00 00 00    mov    DWORD PTR [rbp-0xc],0x1
    13c7:       48 8d 7d df             lea    rdi,[rbp-0x21]
    13cb:       e8 70 fc ff ff          call   1040 <strlen@plt>
    13d0:       48 89 c1                mov    rcx,rax
    13d3:       31 c0                   xor    eax,eax
    13d5:       48 83 f9 08             cmp    rcx,0x8
    13d9:       88 45 bb                mov    BYTE PTR [rbp-0x45],al
    13dc:       0f 83 21 00 00 00       jae    1403 <main+0xe3>
    13e2:       48 8b 45 e8             mov    rax,QWORD PTR [rbp-0x18]
    13e6:       48 89 45 b0             mov    QWORD PTR [rbp-0x50],rax
    13ea:       48 8d 7d c0             lea    rdi,[rbp-0x40]
    13ee:       e8 4d fc ff ff          call   1040 <strlen@plt>
    13f3:       48 89 c1                mov    rcx,rax
    13f6:       48 8b 45 b0             mov    rax,QWORD PTR [rbp-0x50]
    13fa:       48 39 c8                cmp    rax,rcx
    13fd:       0f 92 c0                setb   al
    1400:       88 45 bb                mov    BYTE PTR [rbp-0x45],al
    1403:       8a 45 bb                mov    al,BYTE PTR [rbp-0x45]
    1406:       a8 01                   test   al,0x1
    1408:       0f 85 05 00 00 00       jne    1413 <main+0xf3>
    140e:       e9 4e 00 00 00          jmp    1461 <main+0x141>
    1413:       48 8b 45 e8             mov    rax,QWORD PTR [rbp-0x18]
    1417:       8a 44 05 c0             mov    al,BYTE PTR [rbp+rax*1-0x40]
    141b:       88 45 bc                mov    BYTE PTR [rbp-0x44],al
    141e:       48 8b 45 e8             mov    rax,QWORD PTR [rbp-0x18]
    1422:       8a 44 05 c1             mov    al,BYTE PTR [rbp+rax*1-0x3f]
    1426:       88 45 bd                mov    BYTE PTR [rbp-0x43],al
    1429:       48 8b 45 e8             mov    rax,QWORD PTR [rbp-0x18]
    142d:       8a 44 05 c2             mov    al,BYTE PTR [rbp+rax*1-0x3e]
    1431:       88 45 be                mov    BYTE PTR [rbp-0x42],al
    1434:       48 8d 7d bc             lea    rdi,[rbp-0x44]
    1438:       e8 53 fc ff ff          call   1090 <atoi@plt>
    143d:       88 c1                   mov    cl,al
    143f:       48 63 45 f4             movsxd rax,DWORD PTR [rbp-0xc]
    1443:       88 4c 05 df             mov    BYTE PTR [rbp+rax*1-0x21],cl
    1447:       48 8b 45 e8             mov    rax,QWORD PTR [rbp-0x18]
    144b:       48 83 c0 03             add    rax,0x3
    144f:       48 89 45 e8             mov    QWORD PTR [rbp-0x18],rax
    1453:       8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
    1456:       83 c0 01                add    eax,0x1
    1459:       89 45 f4                mov    DWORD PTR [rbp-0xc],eax
    145c:       e9 66 ff ff ff          jmp    13c7 <main+0xa7>
    1461:       48 63 45 f4             movsxd rax,DWORD PTR [rbp-0xc]
    1465:       c6 44 05 df 00          mov    BYTE PTR [rbp+rax*1-0x21],0x0
    146a:       48 8d 35 93 0b 00 00    lea    rsi,[rip+0xb93]        # 2004 <_IO_stdin_used+0x4>
    1471:       48 8d 7d df             lea    rdi,[rbp-0x21]
    1475:       e8 f6 fb ff ff          call   1070 <strcmp@plt>
    147a:       89 45 f0                mov    DWORD PTR [rbp-0x10],eax
    147d:       8b 45 f0                mov    eax,DWORD PTR [rbp-0x10]
    1480:       89 45 ac                mov    DWORD PTR [rbp-0x54],eax
    1483:       83 e8 fe                sub    eax,0xfffffffe
    1486:       0f 84 aa 00 00 00       je     1536 <main+0x216>
    148c:       e9 00 00 00 00          jmp    1491 <main+0x171>
    1491:       8b 45 ac                mov    eax,DWORD PTR [rbp-0x54]
    1494:       83 e8 ff                sub    eax,0xffffffff
    1497:       0f 84 8f 00 00 00       je     152c <main+0x20c>
    149d:       e9 00 00 00 00          jmp    14a2 <main+0x182>
    14a2:       8b 45 ac                mov    eax,DWORD PTR [rbp-0x54]
    14a5:       85 c0                   test   eax,eax
    14a7:       0f 84 b1 00 00 00       je     155e <main+0x23e>
    14ad:       e9 00 00 00 00          jmp    14b2 <main+0x192>
    14b2:       8b 45 ac                mov    eax,DWORD PTR [rbp-0x54]
    14b5:       83 e8 01                sub    eax,0x1
    14b8:       0f 84 5a 00 00 00       je     1518 <main+0x1f8>
    14be:       e9 00 00 00 00          jmp    14c3 <main+0x1a3>
    14c3:       8b 45 ac                mov    eax,DWORD PTR [rbp-0x54]
    14c6:       83 e8 02                sub    eax,0x2
    14c9:       0f 84 53 00 00 00       je     1522 <main+0x202>
    14cf:       e9 00 00 00 00          jmp    14d4 <main+0x1b4>
    14d4:       8b 45 ac                mov    eax,DWORD PTR [rbp-0x54]
    14d7:       83 e8 03                sub    eax,0x3
    14da:       0f 84 60 00 00 00       je     1540 <main+0x220>
    14e0:       e9 00 00 00 00          jmp    14e5 <main+0x1c5>
    14e5:       8b 45 ac                mov    eax,DWORD PTR [rbp-0x54]
    14e8:       83 e8 04                sub    eax,0x4
    14eb:       0f 84 59 00 00 00       je     154a <main+0x22a>
    14f1:       e9 00 00 00 00          jmp    14f6 <main+0x1d6>
    14f6:       8b 45 ac                mov    eax,DWORD PTR [rbp-0x54]
    14f9:       83 e8 05                sub    eax,0x5
    14fc:       0f 84 52 00 00 00       je     1554 <main+0x234>
    1502:       e9 00 00 00 00          jmp    1507 <main+0x1e7>
    1507:       8b 45 ac                mov    eax,DWORD PTR [rbp-0x54]
    150a:       83 e8 73                sub    eax,0x73
    150d:       0f 84 55 00 00 00       je     1568 <main+0x248>
    1513:       e9 5a 00 00 00          jmp    1572 <main+0x252>
    1518:       e8 c3 fd ff ff          call   12e0 <___syscall_malloc>
    151d:       e9 55 00 00 00          jmp    1577 <main+0x257>
    1522:       e8 b9 fd ff ff          call   12e0 <___syscall_malloc>
    1527:       e9 4b 00 00 00          jmp    1577 <main+0x257>
    152c:       e8 af fd ff ff          call   12e0 <___syscall_malloc>
    1531:       e9 41 00 00 00          jmp    1577 <main+0x257>
    1536:       e8 a5 fd ff ff          call   12e0 <___syscall_malloc>
    153b:       e9 37 00 00 00          jmp    1577 <main+0x257>
    1540:       e8 9b fd ff ff          call   12e0 <___syscall_malloc>
    1545:       e9 2d 00 00 00          jmp    1577 <main+0x257>
    154a:       e8 91 fd ff ff          call   12e0 <___syscall_malloc>
    154f:       e9 23 00 00 00          jmp    1577 <main+0x257>
    1554:       e8 87 fd ff ff          call   12e0 <___syscall_malloc>
    1559:       e9 19 00 00 00          jmp    1577 <main+0x257>
    155e:       e8 9d fd ff ff          call   1300 <____syscall_malloc>
    1563:       e9 0f 00 00 00          jmp    1577 <main+0x257>
    1568:       e8 73 fd ff ff          call   12e0 <___syscall_malloc>
    156d:       e9 05 00 00 00          jmp    1577 <main+0x257>
    1572:       e8 69 fd ff ff          call   12e0 <___syscall_malloc>
    1577:       31 c0                   xor    eax,eax
    1579:       48 83 c4 60             add    rsp,0x60
    157d:       5d                      pop    rbp
    157e:       c3                      ret   
```
