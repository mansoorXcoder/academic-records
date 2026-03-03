#include <stdio.h>

int main() {
    int windowsize, sent = 0, ack, i;

    printf("Enter window size:\n");
    scanf("%d", &windowsize);

    while (sent < windowsize) {
        for (i = 0; i < windowsize && sent < windowsize; i++) {
            printf("Frame %d has been transmitted.\n", sent);
            sent++;
        }

        printf("\nEnter the last Acknowledgement received:\n");
        scanf("%d", &ack);

        if (ack < sent - 1) {
            sent = ack + 1;
            printf("Resending from Frame %d\n", sent);
        }
    }

    printf("\nAll frames transmitted successfully.\n");
    return 0;
}
