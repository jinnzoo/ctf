# Solution
次の2つのことを行いました。
+ リモートのlibcのバージョン特定。
  + find_libcversion.pyを使用して、リモートのlibcの関数アドレスをリークさせることにより、各関数間のオフセットを計算する。
  + 計算したオフセットをローカルのlibcdbの各libcの各関数間のオフセットと比較して一致するlibcを特定する。
+ tcache-poisoningでgotのputsをone_gadgetへ書き換え。
  + fpoolのおかげでdouble freeを行うことができるので、tcahce-poisoningを行う。
  + そもそも、同じアドレスを2回連続でfree出来る時点で、1個目のlibc特定の手順をやる必要はあまりなかった。
