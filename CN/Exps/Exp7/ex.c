#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

int n, r;

struct frame {
    char ack;
    int data;
} frm[10];

void sender(void);
void recvack(void);
void resend(void);
void selective(void);

int main() {
    int c;
    srand(time(NULL));

    do {
        printf("\n\n1. Selective Repeat ARQ");
        printf("\n2. Exit");
        printf("\nEnter your choice: ");
        scanf("%d", &c);

        switch (c) {
            case 1:
                selective();
                break;
            case 2:
                exit(0);
            default:
                printf("\nInvalid choice!");
        }
    } while (c != 2);

    return 0;
}

void selective() {
    sender();
    recvack();
    resend();
    printf("\nAll packets sent successfully\n");
}

void sender() {
    int i;
    printf("\nEnter the number of packets to be sent: ");
    scanf("%d", &n);

    for (i = 0; i < n; i++) {
        printf("Enter data for packet[%d]: ", i);
        scanf("%d", &frm[i].data);
        frm[i].ack = 'y';
    }
}

void recvack() {
    int i;
    r = rand() % n;
    frm[r].ack = 'n';

    for (i = 0; i < n; i++) {
        if (frm[i].ack == 'n') {
            printf("\nPacket %d was not received", i);
        }
    }
}

void resend() {
    printf("\nResending packet %d", r);
    sleep(2);
    frm[r].ack = 'y';
    printf("\nPacket %d received successfully with data: %d\n", r, frm[r].data);
}
