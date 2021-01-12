#include<stdio.h>
struct note
{
    /* data */
    int num;
    char* context;
    char* tips;
    struct note* next;
};
/*
UAF



*/
void safe_flush();
void show_notes_func();
void add_note();
void edit_tips();
void del_note();
void show_note();
void show_all_tips();
int add(int ,int);
void leak_address();