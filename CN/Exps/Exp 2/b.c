#include <stdio.h>
#include <string.h>
#include <conio.h>   // for getch()

int main() {
    int i = 0, count = 0;
    char databits[80];

    printf("Enter Data Bits: ");
    scanf("%s", databits);

    printf("\nData Bits After Bit Stuffing: ");

    for (i = 0; i < strlen(databits); i++) {
        if (databits[i] == '1')
            count++;
        else
            count = 0;

        printf("%c", databits[i]);

        if (count == 5) {
            printf("0");   // Stuff a '0' after five consecutive '1's
            count = 0;
        }
    }

    getch();   // Wait for a key press before exiting
    return 0;
}
