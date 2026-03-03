#include <stdio.h>
#define MAX_NODES 4
#define INFINITY 9999

void distanceVector(int costMatrix[MAX_NODES][MAX_NODES], int nodes) {
    int distance[MAX_NODES][MAX_NODES], nextHop[MAX_NODES][MAX_NODES];
    int i, j, k;

    // Initialize distance and nextHop
    for (i = 0; i < nodes; i++) {
        for (j = 0; j < nodes; j++) {
            distance[i][j] = costMatrix[i][j];
            if (costMatrix[i][j] == INFINITY || i == j)
                nextHop[i][j] = -1;
            else
                nextHop[i][j] = j;
        }
    }

    // Distance Vector Algorithm (similar to Floyd-Warshall relaxation)
    for (k = 0; k < nodes; k++) {
        for (i = 0; i < nodes; i++) {
            for (j = 0; j < nodes; j++) {
                if (distance[i][j] > distance[i][k] + distance[k][j]) {
                    distance[i][j] = distance[i][k] + distance[k][j];
                    nextHop[i][j] = nextHop[i][k];
                }
            }
        }
    }

    // Print routing tables
    for (i = 0; i < nodes; i++) {
        printf("\nRouting table for node %d:\n", i + 1);
        printf("Destination\tCost\tNext Hop\n");
        for (j = 0; j < nodes; j++) {
            if (i != j) {
                printf("%d\t\t%d\t", j + 1, distance[i][j]);   
                if (nextHop[i][j] == -1)
                    printf("None\n");
                else
                    printf("%d\n", nextHop[i][j] + 1);
            }
        }
    }
}

int main() {
    int nodes = MAX_NODES;
    int costMatrix[MAX_NODES][MAX_NODES] = {
        {0, 2, 4, INFINITY},
        {2, 0, 1, 7},
        {4, 1, 0, 3},
        {INFINITY, 7, 3, 0}
    };

    distanceVector(costMatrix, nodes);
    return 0;
}