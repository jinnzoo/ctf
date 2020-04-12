# Solution
```
$ checksec ./chall
[*] '/home/jinnzoo/ctf/bytebanditsctf2020/look-beyond/dist/chall'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE
```

```
$ ./chall
size: 10
idx: 0
where: 0
0
```
プログラムの挙動は次の通り。     
+ sizeにて指定した数値を引数としたmallocが実行される。
+ idxにて数値Bを指定すると、mallocにて返ってきたアドレス+Bのアドレスへ1を書き込む。
+ whereで指定したアドレスへ8バイトの書き込みが可能（readによる書き込み）     
     
以上よりaddressのリークは不可能。readで任意のアドレスへ8バイトの書き込みが可能。          
しかし、readの直後にはcanaryが破壊されていた場合に走るstack_chk_fail命令しか存在しない。また.fini_arrayは書き込み不可。       
 
そこでsizeとidxに適切な数値を入力することによりcanaryを破壊し、readでstack_chk_fail@gotを上書きしmain関数の先頭へ戻すことを考える。    
main関数の先頭へ戻すとputs@gotのアドレスをリークしてくれるため、libcが計算可能になる。(1回目のmain関数の最後のあたりの命令でglobal領域の変数を更新するため)
そのため、2回目もあらかじめcanaryを破壊しておいて、readでstack_chk_fail@gotをone_gadgetに上書きしシェルを起動する。

canaryを破壊する方法は以下。
+ size:にて大きい値（例えば999999）を入力するとmallocでlibcの直後の領域のアドレスAが返ってくる。
+ master canaryはlibcの直後のrw可能なmapped領域に配置されている。
+ idx:にて数値Bを入力すると、A(mallocで返ってきたアドレス)+Bのアドレスに0x1を書き込むことができる。
+ 以上の手順より、master canaryを破壊する。

idxに入力する値(mallocの戻り値とmaster canaryのオフセット)が1回目と2回目のmain関数で異なる。
加えて、2回目のオフセットはローカルとリモートで異なっていたため、運営が掲載していた以下の情報を用いて自分で環境構築しその上にDockerコンテナを立てて、リモートのオフセットを特定し攻撃成功。
```
Remote kernel is

Linux 4.15.0-1057-aws #59-Ubuntu SMP Wed Dec 4 10:02:00 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```

exploit codeでまとめてpayloadを送っているのは、7文字以上の入力を個別に送ると、改行が次の入力値に影響を与えてしまうため。(内部ではfgetsを使っている)

```
$ python3 exploit.py
[+] Opening connection to pwn.byteband.it on port 8000: Done
[*] Switching to interactive mode
 where: 6295576$ ls
chall
flag.txt
$ cat flag.txt
flag{tls_isnt_b1ack_magic}
```
