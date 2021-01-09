test_read: test_read.c
	gcc test_read.c -g2 -o test_read
	patchelf --set-interpreter /usr/local/glibc/glibc2.32/lib/ld-linux-x86-64.so.2 test_read

test_fopen: test_fopen.c
	gcc test_fopen.c -g2 -o test_fopen
	patchelf --set-interpreter /usr/local/glibc/glibc2.32/lib/ld-linux-x86-64.so.2 test_fopen

test_fake: test_fopen.c
	gcc test_fake_read.c -g2 -o test_fake_read
	patchelf --set-interpreter /usr/local/glibc/glibc2.32/lib/ld-linux-x86-64.so.2 test_fake_read