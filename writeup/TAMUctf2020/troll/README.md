# Solution
以下のghidraのデコンパイル結果を見ると、100回連続で乱数予測に成功させたらクリア。
なお乱数取得のたびに10万以下の数値にする計算がmain関数で走るため、それも行う必要あり。

```
{
  int iVar1;
  char local_98 [64];
  char local_58 [44];
  int local_2c;
  FILE *local_28;
  int local_1c;
  time_t local_18;
  int local_c;

  setvbuf(stdout,(char *)0x2,0,0);
  local_18 = time((time_t *)0x0);
  puts("Who goes there?");
  gets(local_58);
  printf("Welcome to my challenge, %s. No one has ever succeeded before. Will you be the first?\n",
         local_58);
  srand((uint)local_18);
  local_c = 0;
  while( true ) {
    if (99 < local_c) {
      puts("You\'ve guessed all of my numbers. Here is your reward.");
      local_28 = fopen("flag.txt","r");
      if (local_28 != (FILE *)0x0) {
        fgets(local_98,0x40,local_28);
        puts(local_98);
      }
      puts("Goodbye.");
      return 0;
    }
    iVar1 = rand();
    local_1c = iVar1 % 100000 + 1;
    puts("I am thinking of a number from 1-100000. What is it?");
    __isoc99_scanf(&DAT_001020a5,&local_2c);
    if (local_1c != local_2c) break;
    puts("Impressive.");
    local_c = local_c + 1;
  }
  puts("You have failed. Goodbye.");
  return 0;
}
```
```
$ python3 exploit.py
<snip>

I am thinking of a number from 1-100000. What is it?
Impressive.
I am thinking of a number from 1-100000. What is it?
Impressive.
I am thinking of a number from 1-100000. What is it?
Impressive.
I am thinking of a number from 1-100000. What is it?
Impressive.
You've guessed all of my numbers. Here is your reward.
gigem{Y0uve_g0ne_4nD_!D3fe4t3d_th3_tr01L!}

Goodbye.
```
