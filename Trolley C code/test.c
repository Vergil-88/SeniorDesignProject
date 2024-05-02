// main.c
#include "UWBcom.c"

int main() {
    int fd = initUWB();
    float* arr = malloc(2 * sizeof(float));
    if (arr == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    while (1) {
        readUWB(fd, arr);
        printf("Current values: X = %f, Y = %f\n", arr[0], arr[1]);
        // Implement any condition to break the loop if needed
    }

    close(fd);
    return 0;
}