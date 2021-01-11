from pwn import *



ELF_name = 'a.out'


bin_elf = ELF(ELF_name)
read_got = bin_elf.got['read']
print(hex(read_got))
