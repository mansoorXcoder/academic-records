#include <stdio.h>
#include <math.h>

/* Function to check prime */
int isPrime(long int num) {
    if (num <= 1)
        return 0;

    for (long int i = 2; i <= sqrt(num); i++) {
        if (num % i == 0)
            return 0;
    }
    return 1;
}

/* Function to find GCD */
long int gcd(long int a, long int b) {
    if (b == 0)
        return a;
    return gcd(b, a % b);
}

/* Function to find Modular Inverse */
long int modInverse(long int e, long int phi) {
    long int k = 1;
    while (1) {
        k = k + phi;
        if (k % e == 0)
            return (k / e);
    }
}

/* Function for Modular Exponentiation */
long int modPower(long int base, long int exp, long int mod) {
    long int result = 1;
    for (long int i = 0; i < exp; i++) {
        result = (result * base) % mod;
    }
    return result;
}

int main() {
    long int p, q, n, phi, e, d;
    long int msg, cipher, decrypted;

    printf("Enter two prime numbers (p and q): ");
    scanf("%ld %ld", &p, &q);

    if (!isPrime(p) || !isPrime(q)) {
        printf("Both numbers must be prime.\n");
        return 0;
    }

    n = p * q;
    phi = (p - 1) * (q - 1);

    printf("Enter public key e (coprime to %ld): ", phi);
    scanf("%ld", &e);

    if (gcd(e, phi) != 1) {
        printf("e is not coprime to %ld\n", phi);
        return 0;
    }

    d = modInverse(e, phi);

    printf("\nPublic Key: (%ld, %ld)", e, n);
    printf("\nPrivate Key: (%ld, %ld)\n", d, n);

    printf("\nEnter message (as integer less than %ld): ", n);
    scanf("%ld", &msg);

    cipher = modPower(msg, e, n);
    decrypted = modPower(cipher, d, n);

    printf("\nEncrypted Message: %ld", cipher);
    printf("\nDecrypted Message: %ld\n", decrypted);

    return 0;
}