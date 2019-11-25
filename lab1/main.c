#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE 1024
#define MODULE 26

void usage(){
    printf("Pass a number between 1 and 26 as a KEY! \n");
    exit(1);
}

void error(int n){
    printf("Error fopen! %d \n", n);
    exit(1);    
}

int main(int argc, char *argv[] ){
    if(argc != 2) usage();
    //argv[0] = program name
    //argv[1] = input KEY
    FILE *txt;
    txt = fopen("cifrado.txt", "r");
    if(txt == NULL) error(1);
    
    char str[LINE];
    int key = atoi(argv[1]);
    if(key > 26 || key < 0) usage();
    
    FILE *out = fopen("result.txt", "w"); //Open output file for given Key
    if(out == NULL) error(2);
    
    while (fgets(str, LINE, txt) != NULL){
        printf("%s", str); //CIPHERED TEXT
        
        //FOR EACH LINE TAKE THE CHARS AND APPLY THE +KEY VALUE TO TRY DECIPHER
        int aux;
        char decipherChar[strlen(str)];
        
        //GREEK ALPH IN ASCII STARTS AT 161 and ends at 186!
        for(aux = 0; aux < strlen(str); ++aux){
            char dec;
            if(str[aux]+(key+'0') > 186) dec = (str[aux]+(key+'0')- (186-'0'));
            else if(str[aux] + (key+'0') < 161) dec = (str[aux]+(key+'0'));
            decipherChar[aux] = dec;
        }
        
        
        
        fputs(decipherChar, out);
    }
    
    fclose(out);
    printf("%d \n",key); //KEY 
    
    fclose(txt);
    
    exit(0);
}

