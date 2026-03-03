#include <stdio.h>
#include <string.h>
#include <conio.h>   // for getche(), instead of <process.h>

int main() {
    int i = 0, j = 0, n, pos;
    char a[20], b[50], ch;

    printf("Enter string: ");
    scanf("%s", a);

    n = strlen(a);

    printf("Enter position: ");
    scanf("%d", &pos);

    if (pos > n) {
        printf("Invalid position, enter again: ");
        scanf("%d", &pos);
    }

    printf("Enter the character: ");
    ch = getche();

    // Start frame with "dlestx"
    b[0] = 'd';
    b[1] = 'l';
    b[2] = 'e';
    b[3] = 's';
    b[4] = 't';
    b[5] = 'x';
    j = 6;

    while (i < n) {
        // Insert character with stuffing at given position
        if (i == pos - 1) {
            b[j]   = 'd';
            b[j+1] = 'l';
            b[j+2] = 'e';
            b[j+3] = ch;
            b[j+4] = 'd';
            b[j+5] = 'l';
            b[j+6] = 'e';
            j += 7;
        }

        // Handle "dle" sequence in input
        if (a[i] == 'd' && a[i+1] == 'l' && a[i+2] == 'e') {
            b[j]   = 'd';
            b[j+1] = 'l';
            b[j+2] = 'e';
            j += 3;
        }

        b[j] = a[i];
        i++;
        j++;
    }

    // End frame with "dleetx"
    b[j]   = 'd';
    b[j+1] = 'l';
    b[j+2] = 'e';
    b[j+3] = 'e';
    b[j+4] = 't';
    b[j+5] = 'x';
    b[j+6] = '\0';

    printf("\nFrame after stuffing:\n");
    printf("%s\n", b);

    return 0;
}
