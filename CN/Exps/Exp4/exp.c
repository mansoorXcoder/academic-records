#include <stdio.h>

int main() {
    int data[7], rec[7], i, c1, c2, c3, c;

    printf("This works for message of 4 bits in size\nEnter message bits one by one: ");
    scanf("%d %d %d %d", &data[0], &data[1], &data[2], &data[4]);

    // Calculate parity bits
    data[6] = data[0] ^ data[2] ^ data[4];
    data[5] = data[0] ^ data[1] ^ data[4];
    data[3] = data[0] ^ data[1] ^ data[2];

    printf("\nThe encoded bits are:\n");
    for (i = 0; i < 7; i++) {
        printf("%d ", data[i]);
    }

    printf("\nEnter the received data bits one by one: ");
    for (i = 0; i < 7; i++) {
        scanf("%d", &rec[i]);
    }

    // Syndrome calculation
    c1 = rec[6] ^ rec[4] ^ rec[2] ^ rec[0];
    c2 = rec[5] ^ rec[4] ^ rec[1] ^ rec[0];
    c3 = rec[3] ^ rec[2] ^ rec[1] ^ rec[0];
    c = c3 * 4 + c2 * 2 + c1;

    if (c == 0) {
        printf("\nCongratulations, there is no error.\n");
    } else {
        printf("\nError at position: %d\n", c);
        // Correct the error
        rec[7 - c] = !rec[7 - c];

        printf("The corrected message is:\n");
        for (i = 0; i < 7; i++) {
            printf("%d ", rec[i]);
        }
        printf("\n");
    }

    return 0;
}