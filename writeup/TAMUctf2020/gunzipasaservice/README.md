# Solution
ghidraでデコンパイル。以下のgunzip関数がmain関数より呼ばれている。

```
void gunzip(void)

{
  undefined local_418 [512];
  undefined local_218 [512];
  undefined4 local_18;
  int local_14;
  size_t local_10;

  subprocess("gunzip",&local_14,&local_18);
  memset(local_218,0,0x200);
  local_10 = read(0,local_218,0x200);
  write(local_14,local_218,local_10);
  close(local_14);
  memset(local_418,0,0x200);
  gets_fd(local_418,local_18);
  fwrite(local_418,1,0x200,*(FILE **)PTR_stdout_0804bffc);
  return;
}
```

上記のgunzip関数は、親プロセスの標準入力より受け取ったデータを、子プロセスのgunzipコマンドに入力し、その結果（標準出力に出力されるデータ）を親プロセスはgetsで取得している。
そのため、gunzipコマンドの解凍結果を用いてbofを起こすことが可能。canaryもなし。        
gunzipコマンドを実行するためにexeclを使ってくれており、/bin/sh文字列も存在するので、それを用いてROPでシェルを起動し終了。

```
$ python3 exploit.py
[+] Opening connection to challenges.tamuctf.com on port 4709: Done
[*] Switching to interactive mode

gzip: stdin: unexpected end of file
$ ls
flag.txt
gunzipasaservice
$ cat flag.txt
gigem{r0p_71m3}$
```
