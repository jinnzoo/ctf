# Solution
## leak libc
By using tcache-poisoning, overwrites tcache_perthread_structure.      
tcache_perthread_structure is on the top of heap region.      
        
Leak heap_base(for overwrite tcache_perthread_structure) =>          
Overwrites tcache_perthread_structure for making it appear as array of specific size tcache chunks is full. (7 chunks in same size.) =>       
Free overwrite_tcache_perthread structure as fake chunk which will be inserted to the array which is full. =>          
The array is full and overwrite_tcache_perthread fake chunk is not bottom chunk (chunks are allocated next address of it), so the chunk is inserted to unsortedbin.       
        
Use show for freed overwrite_tcache_perthread fake chunk and get libc base.        

## get shell
overwrite freehook and run free("/bin/sh") => run shell!

# Reference
+ https://www.willsroot.io/2020/06/redpwnctf-2020-pwn-writeups-four.html
+ https://ctf-wiki.github.io/ctf-wiki/pwn/linux/glibc-heap/implementation/tcache/
