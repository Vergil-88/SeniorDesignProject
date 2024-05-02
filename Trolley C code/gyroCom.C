#include <stdio.h>      // Standard input/output definitions
#include <stdlib.h>     // Standard library for using exit function
#include <string.h>     // String function definitions
#include <unistd.h>     // UNIX standard function definitions
#include <fcntl.h>      // File control definitions
#include <errno.h>      // Error number definitions
#include <termios.h>    // POSIX terminal control definitions
#include <signal.h>     // Signal handling definitions

int fd; // File descriptor for the port, make it global for signal handler

void signal_handler(int sig) {
    printf("\nTerminating...\n");
    close(fd);
    exit(EXIT_SUCCESS);
}

int open_port(void) {
    // Open the serial port read/write, with no controlling terminal, and don't wait for a connection
    fd = open("/dev/tty.usbmodem1101", O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1) {
        perror("open_port: Unable to open /dev/tty.usbmodem1101 - ");
    } else {
        fcntl(fd, F_SETFL, 0); // Clear all flags on descriptor, enable direct I/O
    }
    return (fd);
}

void configure_port(int fd) {
    struct termios options;

    // Get the current options for the port
    tcgetattr(fd, &options);

    // Set the baud rates to 115200
    cfsetispeed(&options, B115200);
    cfsetospeed(&options, B115200);

    // Enable the receiver and set local mode
    options.c_cflag |= (CLOCAL | CREAD);

    // Set 8N1 (no parity bit, 1 stop bit, 8 data bits)
    options.c_cflag &= ~PARENB;
    options.c_cflag &= ~CSTOPB;
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;

    // Disable hardware flow control
    options.c_cflag &= ~CRTSCTS;

    // Choose raw input
    options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);

    // Disable software flow control
    options.c_iflag &= ~(IXON | IXOFF | IXANY);

    // Set the new options for the port
    tcsetattr(fd, TCSANOW, &options);
}

void initCompass(void){
    signal(SIGINT, signal_handler); // Setup the signal handler for SIGINT

    fd = open_port();
    if (fd == -1) {
        fprintf(stderr, "Failed to open serial port\n");
        exit(EXIT_FAILURE);
    }

    configure_port(fd);
}

char* readCompass(void) {
    static char compassbuffer[256];
    memset(compassbuffer, 0, sizeof(compassbuffer)); // Clear the buffer

    char tempChar;
    int i = 0;
    while (read(fd, &tempChar, 1) > 0 && tempChar != '\n' && i < sizeof(compassbuffer) - 1) {
        compassbuffer[i++] = tempChar;
    }
    compassbuffer[i] = '\0'; // Ensure the buffer is null-terminated

    if (i == 0) { // Check if no data was read
        return NULL;
    }
    return compassbuffer;
}


//     configure_port(fd);

//     while (1) {
//         char buffer[256];  // Buffer for where to store the data
//         int n = read(fd, buffer, sizeof(buffer));  // Read up to 255 characters from the port if they are there
//         if (n < 0) {
//             perror("Read failed - ");
//             continue;
//         } else if (n == 0) {
//             printf("No data on port\n");
//         } else {
//             buffer[n] = '\0';  // Null terminate the string
//             printf("%s\n",buffer);
//         }
//     }

//     close(fd);
//     return EXIT_SUCCESS;
// }
