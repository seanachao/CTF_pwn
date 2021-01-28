chunk_manage: source/chunk_manage.c source/main.c source/chunk_manage.h
	gcc source/*.c -lreadline -g2 -o bin/chunk_manage
	patchelf --set-interpreter /usr/local/glibc/glibc2.31/lib/ld-linux-x86-64.so.2 bin/chunk_manage