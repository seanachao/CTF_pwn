a.out: main.c note.c note.h
	gcc main.c  note.h  note.c  -o a.out
	strip a.out
	patchelf --set-interpreter /glibc/x64/2.24/lib/ld-linux-x86-64.so.2 ./a.out
	cp a.out stand/a.out
test: note_test.c note.c note.h
	gcc note.h note.c note_test.c -lcmocka -o note_test
