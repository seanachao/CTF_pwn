#include<stdio.h>
#include "note.h"


int main(){
    setvbuf(stdin,NULL,_IONBF,0);
    setvbuf(stdout,NULL,_IONBF,0);
    setvbuf(stderr,NULL,_IONBF,0);
    int choose  = 4;
    do {
        show_notes_func();
        if(1!= scanf("%d",&choose)){
            printf("your input wrong,you can input only a number,try again\n");
            safe_flush();
            continue;
        }
        
        switch (choose)
        {
        case 1:
            /* code */
            add_note();
            break;
        
        case 2:
            del_note();
            break;
        
        case 3:
            edit_tips();
            break;
        
        case 4:
            show_note();
            break;
        case 5:
            show_all_tips();
            break;
        case 6:
            exit(-1);
            break;
        default:
            choose = 0;
        }
        //printf("%d",choose);
    } while (choose != 6);
    return 0;

}