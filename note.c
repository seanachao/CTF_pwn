#include "note.h"
#include<stdio.h>
#include<stdlib.h>
struct note notes[20] ={{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1},{-1}};

struct note note_head =  {
    0,
    NULL,
    NULL,
    NULL,
};
int notes_total = 0;
struct note* notes_pr = &note_head;
struct note* cur_pr = NULL;
int add(int a,int b){
    return a + b;
}
void safe_flush()
{
    char c;
    while((c = getchar()) != '\n' && c != EOF);
}
void show_notes_func(){
    printf("Welcome use the notes\n");
    printf("1. add your note\n");
    printf("2. del your note\n");
    printf("3. modify the tips\n");
    printf("4. show the notes\n");
    printf("5. show all tips\n");
    printf("6. exit the note manager\n");
}
void del_note(){
    printf("Please input the del note id\n");
    int id = -1;
    scanf("%d",&id);
    cur_pr = notes_pr;
    while(cur_pr -> next != NULL){
        if(cur_pr ->next ->num == id){    
            free(cur_pr->next->context);
            free(cur_pr->next->tips);
            cur_pr->next->num = -1;
            if(cur_pr -> next -> next != NULL)
                cur_pr -> next = cur_pr -> next -> next;
            else{
                cur_pr -> next = NULL;
                break;
            }
        }
        cur_pr = cur_pr -> next;
    }
    // the last of the list
    //if(cur_ptr -> num == id)
}
void edit_tips(){
    cur_pr = notes_pr;
    printf("Please input which id you edit its tip\n");
    int id = 0;
    int size = 0;
    scanf("%d %d",&id,&size);
    if(size < 0x400) size += 0x400;
    while(cur_pr->next != NULL){
        if(cur_pr -> next -> num == id){
            if(cur_pr->next->tips == NULL){
                cur_pr -> next -> tips = malloc(size);
            }
            printf("Please input your tips for its tip\n");
            //read(0,cur_pr->tips,100);
            scanf("%s",cur_pr->next->tips);
        }
        cur_pr = cur_pr-> next;
    }

}
void show_all_tips(){
    cur_pr = notes_pr;
    while (cur_pr -> next != NULL)
    {
        /* code */
        printf("%p %s\n",cur_pr->next->num,cur_pr -> next->tips);
        cur_pr = cur_pr -> next;
    }
    
}
void show_note(){
    cur_pr = notes_pr;
    int id = 0;
    printf("Please input the notes_id\n");
    //printf("Please input")
   
    scanf("%d",&id);
    while(cur_pr -> next != NULL){
        if(cur_pr -> next ->num == id ){
            printf("show the context\n");
            printf("%s\n",cur_pr ->next->context);
            break;
        }
        cur_pr = cur_pr -> next;
    }
}
void add_note(){
    int id = -1;
    //static
    printf("Please input the note id\n");
    int size = 0;
    scanf("%d",&id);
    size = 0x60;
    if(id  < 0){
        id = (- id);
    }
    cur_pr = notes_pr;
    while(cur_pr->next != NULL){
        if(cur_pr ->next -> num != id)
            cur_pr = cur_pr -> next;
        else{
            printf("The note id exist\n");
            return ;
        }
        //cur_pr = cur_pr -> next;
    }
    for(int i=0;i<20;i++){
        if(notes[i].num < 0) {
            notes[i].num = id;
            notes[i].context  = malloc(size);   
            printf("Please input the notes\n");
            scanf("%s",notes[i].context);
            notes[i].next = NULL;
            cur_pr->next = &notes[i];     
            break;
        
        }
        if(i==19) {
            printf("Not enough space to record the notes\n");
            return;
        }
    }

    //write(1,"Please input the notes\n",30);
    //printf("")

    return;

}
// void leak_address(){
//     //write_bytes();
//    // printf("Enter");

//     printf("%p ppp \n",&notes);
//     printf("%x nnn\n",notes);
// }
// void read_byte(){
//     char a[100]="";
//     read(0,a,100);
// }
// void write_bytes(){
//     char a[100]="";
//     write(1,a,100);

// }