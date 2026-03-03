#include <stdio.h>

// Function prototypes
int add(int, int);
int com(int);

int main() {
    int i, dl;
    int data1[10], data2[10], newdata[10], comp[10], checksum[10];

    // Input data length
    printf("\nEnter the data length = ");
    scanf("%d", &dl);

    // Input frame1 (data1)
    printf("\nEnter the frame1 or data1 in the form of 0's and 1's:\n");
    for (i = 0; i < dl; i++)
        scanf("%d", &data1[i]);

    // Input frame2 (data2)
    printf("\nEnter the frame2 or data2 in the form of 0's and 1's:\n");
    for (i = 0; i < dl; i++)
        scanf("%d", &data2[i]);

    // Addition of data1 and data2
    for (i = dl - 1; i >= 0; i--) {
        newdata[i] = add(data1[i], data2[i]);
    }

    // Display data1 and data2
    printf("\n\nData 1 : ");
    for (i = 0; i < dl; i++)
        printf("%d", data1[i]);

    printf("\nData 2 : ");
    for (i = 0; i < dl; i++)
        printf("%d", data2[i]);

    // Display new data
    printf("\n\nThe new data is: ");
    for (i = 0; i < dl; i++)
        printf("%d", newdata[i]);

    // Generate checksum
    printf("\nChecksum : ");
    for (i = 0; i < dl; i++) {
        checksum[i] = com(newdata[i]);
        printf("%d", checksum[i]);
    }

    // Receiver side
    printf("\n\nReceiver Side : \n");
    printf("\nData : ");
    for (i = 0; i < dl; i++)
        printf("%d", data1[i]);
    printf(" ");
    for (i = 0; i < dl; i++)
        printf("%d", data2[i]);
    printf(" ");
    for (i = 0; i < dl; i++)
        printf("%d", checksum[i]);

    // Addition at receiver
    printf("\nAddition : ");
    for (i = dl - 1; i >= 0; i--) {
        newdata[i] = add(newdata[i], checksum[i]);
    }
    for (i = 0; i < dl; i++)
        printf("%d", newdata[i]);

    // Complement at receiver
    printf("\nComplement : ");
    for (i = 0; i < dl; i++) {
        comp[i] = com(newdata[i]);
        printf("%d", comp[i]);
    }

    printf("\n");
    return 0;
}

// Function to add bits with carry
int add(int x, int y) {
    static int carry = 0;

    if (x == 1 && y == 1 && carry == 0) {
        carry = 1; return 0;
    } else if (x == 1 && y == 1 && carry == 1) {
        carry = 1; return 1;
    } else if (x == 1 && y == 0 && carry == 0) {
        carry = 0; return 1;
    } else if (x == 1 && y == 0 && carry == 1) {
        carry = 1; return 0;
    } else if (x == 0 && y == 1 && carry == 0) {
        carry = 0; return 1;
    } else if (x == 0 && y == 1 && carry == 1) {
        carry = 1; return 0;
    } else if (x == 0 && y == 0 && carry == 0) {
        carry = 0; return 0;
    } else {
        carry = 0; return 1;
    }
}

// Function to compute complement
int com(int a) {
    if (a == 0)
        return 1;
    else
        return 0;
}