# Solution
musl-libcでビルドされているバイナリ。しかし、今回そこは関係なかった。       
      
プログラムの挙動としては、全部で3回入力を行うことができ、その3つの文字列に対して比較が行われ、成功すればflagが表示される。             
           
1回目は howdy              
2回目は gig 'em                   
を入力すればよいだけだが、3回目はユーザが入力した値が文字列を格納したアドレスとみなされて、そのアドレスの指す先の文字列と'whoop\n'との比較が行われる。その命令が以下。以下の命令を突破すれば（等しいとみなされれば）、flagが出力される。             
アドレスリークはできないため、どのように攻略するか。                  

```
=> 0x555bc987b3ad <main+420>:   call   0x555bc987b080 <strcmp@plt>
   0x555bc987b3b2 <main+425>:   test   eax,eax
   0x555bc987b3b4 <main+427>:   je     0x555bc987b3cc <main+451>
   0x555bc987b3b6 <main+429>:   lea    rdi,[rip+0xcc2]        # 0x555bc987c07f
   0x555bc987b3bd <main+436>:   call   0x555bc987b030 <puts@plt>
Guessed arguments:
arg[0]: 0x7f432ce3000a --> 0xd45000007f432ce2               ★1
arg[1]: 0x7ffc37fbf640 --> 0xa000a706f6f6877 ('whoop\n')
arg[2]: 0x7ffc37fbf640 --> 0xa000a706f6f6877 ('whoop\n')
[------------------------------------stack-------------------------------------]
0000| 0x7ffc37fbf630 --> 0x0
0008| 0x7ffc37fbf638 --> 0x0
0016| 0x7ffc37fbf640 --> 0xa000a706f6f6877 ('whoop\n')
0024| 0x7ffc37fbf648 --> 0x7f432ce32a00 --> 0x0
0032| 0x7ffc37fbf650 --> 0x0
0040| 0x7ffc37fbf658 --> 0x610
0048| 0x7ffc37fbf660 --> 0x0
0056| 0x7ffc37fbf668 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x0000555bc987b3ad in main ()
gdb-peda$ searchmem whoop
Searching for 'whoop' in: None ranges
Found 2 results, display max 2 items:
 mapped : 0x7f432ce33360 --> 0xa000a706f6f6877 ('whoop\n')    ★2
[stack] : 0x7ffc37fbf640 --> 0xa000a706f6f6877 ('whoop\n')
```

★1が、3回目の入力で改行のみを入力した場合で, 0x7f432ce3000aといったように先頭の2バイトが改行コード＋NULLとなっていることが分かる。
加えて★1の元の値がwhoopを格納している0x7f432ce33360であることもデバッグにより分かった。                    
whoopを格納しているのは、★2の2つのアドレス。                 
                    
しかし★1の結果を見てもわかるように改行だけ入力しても改行コードとNULL文字が入力されアドレスが上書きされてしまう。              
                   
そこで次の2つを考えた。                 
+ 調節してmappedな領域のwhoop\nを指すアドレスにする。
+ fgetsによって入力された文字列はスタック上の格納先だけではなく、mappedな領域にも保存されるため、その挙動を利用して、mappedな領域にwhoop\nを展開しそこを指すようにアドレスを調節する。
                
上記の2つは難しく失敗した。最終的にユーザ入力を受け取るfgetsを失敗させればwhoopを格納しているアドレスをそのままstrcmpに渡すことができるのではということに気づき、3回目の入力はEOF相当を送ることにより成功。             

```
$ python3 exploit.py
[+] Opening connection to challenges.tamuctf.com on port 4352: Done
[+] Recieving all data: Done (36B)
[*] Closed connection to challenges.tamuctf.com port 4352
b'\r\n\r\ngigem{fg3ts_g3t5_c0nfu5ed_2}\r\n\r\n'
```
