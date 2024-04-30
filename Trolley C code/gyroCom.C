#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>

float angle_values = 0;

void process_line(char *line) {
    char *ptr;
    if ((ptr = strstr(line, "Angle:")) != NULL) {
        ptr += strlen("Angle:");  // Move past "Angle:"
        angle_values = strtof(ptr, NULL);
        if (angle_values == 0 && errno == EINVAL) {
            printf("Could not convert angle value to float: '%s'\n", line);
        }
    }
}

int setup_serial() {
    int fd;
    struct termios tty;

    fd = open("/dev/tty.usbmodem11301", O_RDWR | O_NOCTTY | O_SYNC);
    if (fd < 0) {
        printf("Error opening serial port: %s\n", strerror(errno));
        return -1;
    }

    memset(&tty, 0, sizeof(tty));
    if (tcgetattr(fd, &tty) != 0) {
        printf("Error from tcgetattr: %s\n", strerror(errno));
        close(fd);
        return -1;
    }

    cfsetospeed(&tty, B115200);
    cfsetispeed(&tty, B115200);

    tty.c_cflag |= (CLOCAL | CREAD);  // Enable the receiver and set local mode
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;               // 8-bit characters
    tty.c_cflag &= ~PARENB;           // No parity bit
    tty.c_cflag &= ~CSTOPB;           // 1 stop bit
    tty.c_cflag &= ~CRTSCTS;          // No hardware flow control

    tty.c_iflag &= ~(IXON | IXOFF | IXANY); // Turn off software flow control
    tty.c_iflag &= ~(ICANON | ECHO | ECHOE | ISIG); // Raw input

    tty.c_oflag &= ~OPOST; // Raw output

    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        printf("Error from tcsetattr: %s\n", strerror(errno));
        close(fd);
        return -1;
    }

    return fd;
}

int main() {
    int serial_fd = setup_serial();
    if (serial_fd < 0) return -1;

    char read_buf[256];
    int n;

    while (1) {
        n = read(serial_fd, read_buf, sizeof(read_buf) - 1);
        if (n > 0) {
            read_buf[n] = '\0';
            printf("Received: %s\n", read_buf);
            process_line(read_buf);
            printf("Extracted angle values: %f\n", angle_values);
        }
    }

    close(serial_fd);
    return 0;
}
