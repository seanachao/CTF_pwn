
 #include<stdio.h>
 FILE* fp;
 char *msg = "secret";
 char *buf = "fakesecret";
 struct _IO_FILE_fake {
     int _flags;
     char *_IO_read_ptr;
     char *_IO_read_end;
     char *_IO_read_base;
     char *_IO_write_base;
 
     char *_IO_write_ptr;
     char *_IO_write_end;
     char *_IO_buf_base;
     char *_IO_buf_end;
     char *_IO_save_base;
     char *_IO_backup_base;
     char *_IO_save_end;
     struct _IO_marker *_markers;
     struct _IO_FILE *_chain;
     int _fileno;
 
     int _flags2;
     __off_t _old_offset;
     unsigned short _cur_column;
     signed char _vtable_offset;
     char _shortbuf[1];
     _IO_lock_t *_lock;
     __off64_t _offset;
     struct _IO_codecvt *_codecvt;
     struct _IO_wide_data *_wide_data;
     struct _IO_FILE *_freeres_list;
 
     void *_freeres_buf;
     size_t __pad5;
     int _mode;
     char _unused2[20];
 };
/*
pwndbg> p/x _IO_list_all
$12 = 0x7ffff7fc45e0
pwndbg> p (struct _IO_FILE)*0x7ffff7fc45e0
$13 = {
  _flags = -72540026,
  _IO_read_ptr = 0x0,
*/
 int main(){
        //setvbuf(stdin,NULL,_IONBF,0);
        //setvbuf(stdout,NULL,_IONBF,0);
        //setvbuf(stderr,NULL,_IONBF,0);
        //printf("hello world\n");
        struct _IO_FILE* fp = stdin;
    //  fp = fopen("test_read11.txt","rw");
     /*fp -> _flags  = (fp->_flags & (~8));
     fp -> _flags  = (fp->_flags| 0x800);
 
     fp -> _IO_write_base = msg;
     fp -> _IO_write_ptr = msg + 6;
     fp -> _IO_read_end = fp -> _IO_write_base;
     fp -> _fileno = 1;*/
    //  struct _IO_FILE_fake* fp_pr = NULL;
     
     struct _IO_FILE_fake fake_fp ={
         (fp->_flags & (~8)) |(fp->_flags| 0x800),
         fp->_IO_read_ptr,
         msg,
         fp->_IO_read_base,
         msg,
 
         msg + 6,
         fp->_IO_write_end,
         fp->_IO_buf_base,
         fp->_IO_buf_end,
         fp->_IO_save_base,
         fp->_IO_backup_base,
         fp->_IO_save_end,
         fp->_markers,
         0x0,
         1,
 
         fp->_flags2,
         fp->_old_offset,
         fp->_cur_column,
         fp->_vtable_offset,
         *fp->_shortbuf,
         fp->_lock,
         fp->_offset,
         fp->_codecvt,
         fp->_wide_data,
         fp->_freeres_list,
 
         fp->_freeres_buf,
         fp->__pad5,
         fp->_mode,
         *fp->_unused2,
     
     };
     fp->_chain = (struct _IO_FILE *)&fake_fp;
     
     //fp_pr = &fake_fp;
    //  //fp->_chain = fp_pr;
    //  //fwrite(buf,1,0x100,fp);*/
    //  fclose(fp);
 }
