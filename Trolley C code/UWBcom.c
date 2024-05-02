#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>

float X = 0.0;
float Y = 0.0;

void process_line(char *line) {
    char *part;
    part = strtok(line, " ");
    while(part != NULL) {
        if(strstr(part, "X=") != NULL) {
            char *x_val = strchr(part, '=') + 1;
            X = atof(x_val);
        }
        else if(strstr(part, "Y=") != NULL) {
            char *y_val = strchr(part, '=') + 1;
            Y = atof(y_val);
        }
        part = strtok(NULL, " ");
    }
}

int initUWB(){
    int fd;
    struct termios options;
    char buffer[256];
    ssize_t bytes_read;

    // Open the serial port
    fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_NDELAY);
    if (fd == -1) {
        perror("open_port: Unable to open /dev/ttyUSB0 - ");
        return -1;
    }

    // Configure the serial port
    tcgetattr(fd, &options);
    cfsetispeed(&options, B115200);
    cfsetospeed(&options, B115200);
    options.c_cflag |= (CLOCAL | CREAD);
    options.c_cflag &= ~PARENB;
    options.c_cflag &= ~CSTOPB;
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;
    options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    options.c_iflag &= ~(IXON | IXOFF | IXANY);
    options.c_oflag &= ~OPOST;
    tcsetattr(fd, TCSANOW, &options);

    return fd;
}

float* readUWB(int fd, float* arr){
    
    char buffer[256];
    ssize_t bytes_read;

    memset(buffer, 0, 256);
        bytes_read = read(fd, buffer, 255);
        if (bytes_read > 0) {
            buffer[bytes_read - 1] = '\0'; // Replace the newline char with null char
            process_line(buffer);

            // printf("%f      %f \n", X, Y);
            arr[0] = X;
            arr[1] = Y;
        }
    return arr;
}

// int main() {
    

    
//     while (1) {
//         // Read a line from the serial port
        
//     }

//     // close(fd);
//     // return 0;
// }
