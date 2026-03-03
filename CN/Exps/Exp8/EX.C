#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define TOTAL_FRAMES 5

int sendFrame(int frameNumber) {
    printf("Sending Frame %d\n", frameNumber);
    sleep(1);

    if (rand() % 10 < 2) {
        printf("Frame %d lost or corrupted during transmission!\n", frameNumber);
        return 0;
    }
    return 1;
}

int receiveAck(int frameNumber) {
    sleep(1);

    if (rand() % 10 < 1) {
        printf("ACK for Frame %d lost!\n", frameNumber);
        return 0;
    }

    printf("ACK for Frame %d received.\n", frameNumber);
    return 1;
}

int main() {
    srand(time(NULL));
    int frameNumber = 1;

    while (frameNumber <= TOTAL_FRAMES) {
        if (sendFrame(frameNumber)) {
            if (receiveAck(frameNumber)) {
                frameNumber++;
            } else {
                printf("Timeout waiting for ACK for Frame %d. Resending...\n", frameNumber);
            }
        } else {
            printf("Resending Frame %d...\n", frameNumber);
        }
    }

    printf("All frames sent and acknowledged successfully.\n");
    return 0;
}
