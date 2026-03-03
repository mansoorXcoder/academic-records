#include <stdio.h>
#include <math.h>

int main() {
    int ip[4], cidr;
    int mask[4] = {0}, network[4], broadcast[4];
    int i, host_bits;
    int temp_cidr;

    printf("Enter IP address (e.g., 192.168.10.25): ");
    scanf("%d.%d.%d.%d", &ip[0], &ip[1], &ip[2], &ip[3]);

    printf("Enter CIDR value (0-32): ");
    scanf("%d", &cidr);

    if (cidr < 0 || cidr > 32) {
        printf("Invalid CIDR value!\n");
        return 0;
    }

    host_bits = 32 - cidr;
    int total_hosts = (1 << host_bits) - 2;

    temp_cidr = cidr;

    // Calculate subnet mask
    for (i = 0; i < 4; i++) {
        if (temp_cidr >= 8) {
            mask[i] = 255;
            temp_cidr -= 8;
        } 
        else if (temp_cidr > 0) {
            mask[i] = (256 - (1 << (8 - temp_cidr)));
            temp_cidr = 0;
        } 
        else {
            mask[i] = 0;
        }
    }

    // Calculate network address
    for (i = 0; i < 4; i++) {
        network[i] = ip[i] & mask[i];
    }

    // Calculate broadcast address
    for (i = 0; i < 4; i++) {
        broadcast[i] = network[i] | (~mask[i] & 255);
    }

    printf("\nSubnet Mask: %d.%d.%d.%d", mask[0], mask[1], mask[2], mask[3]);
    printf("\nNetwork Address: %d.%d.%d.%d", network[0], network[1], network[2], network[3]);
    printf("\nBroadcast Address: %d.%d.%d.%d", broadcast[0], broadcast[1], broadcast[2], broadcast[3]);
    printf("\nTotal Hosts per Subnet: %d\n", total_hosts);

    return 0;
}