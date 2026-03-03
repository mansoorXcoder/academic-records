#include <stdio.h>
#include <stdbool.h>
#define MAX_HOSTS 5

void broadcastTree(int graph[MAX_HOSTS][MAX_HOSTS], int hosts, int source) {
    bool visited[MAX_HOSTS] = {false};
    int queue[MAX_HOSTS];
    int front = 0, rear = 0;

    // Start with the source host
    visited[source] = true;
    queue[rear++] = source;

    printf("Broadcasting message from Host %d:\n", source + 1);

    while (front < rear) {
        int currentHost = queue[front++];
        
        for (int i = 0; i < hosts; i++) {
            if (graph[currentHost][i] == 1 && !visited[i]) {
                visited[i] = true;
                queue[rear++] = i;
                printf("Message sent to Host %d\n", i + 1);
            }
        }
    }
}

int main() {
    int graph[MAX_HOSTS][MAX_HOSTS] = {
        {0, 1, 1, 0, 0},
        {1, 0, 0, 1, 0},
        {1, 0, 0, 0, 1},
        {0, 1, 0, 0, 0},
        {0, 0, 1, 0, 0}
    };

    int sourceHost = 0; // Change this to any host you want to broadcast from
    broadcastTree(graph, MAX_HOSTS, sourceHost);

    return 0;
}