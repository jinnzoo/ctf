# Solution

実行すると以下のメニューが出る。
```
$ ./aerofloat
{?} Enter name: jinnzoo
1. Set rating
2. View rating list
3. View porfile info
4. Exit
>
```

1のSetでidとscoreを入力することができる。

```
> 1
{?} Enter your ticket id: 11
{?} Enter your rating: 22
{+} You set rating <22.000000> to ticket <11>
1. Set rating
2. View rating list
3. View porfile info
4. Exit
```

1のSetは、idはstrでそのままstackに格納され、scoreはidが格納された次の8バイトにscanf("%lf",,,)によって格納される。      
      
ここで、1のSetはバッファーを超えても値を書き込むことができ、バッファオーバーフローを起こす。そのため「idがstrで格納」と「scoreはscanf("%lf")で格納」に気を付ければ、ROPを用いて攻略可能。       

なお、exploit.pyの38行目で「set_(r, p32(0x0)+p32(11), GOMI)」と行っている理由は、1のSetと2のViewがどこからどこまでのアドレスを参照するかの値が、stackのこの位置に格納されているので、その値を壊さないようにしているというためである。



