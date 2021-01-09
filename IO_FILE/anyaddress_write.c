#include<stdio.h>
FILE *fp;
char buf[0x100] = "fakesecret";
char msg[0x100] = "";


int main(){
    fp = fopen("test.txt","w");
    fp -> _IO_write_ptr = msg;
    fp -> _IO_write_end = fp -> _IO_write_ptr + 10;
    fwrite(buf,1,0x100,fp);
    puts(msg);
    fclose(fp);
}