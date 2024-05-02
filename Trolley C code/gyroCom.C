#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>

int open_serial_port(const char* device) {
    int fd = open(device, O_RDWR | O_NOCTTY);
    if (fd == -1) {
        perror("open_serial_port: Unable to open serial port");
        return -1;
    }

    struct termios tty;
    if (tcgetattr(fd, &tty) != 0) {
        perror("open_serial_port: tcgetattr");
        close(fd);
        return -1;
    }

    cfsetospeed(&tty, B115200);
    cfsetispeed(&tty, B115200);

    tty.c_cflag &= ~PARENB; // Clear parity bit, disabling parity
    tty.c_cflag &= ~CSTOPB; // Clear stop field, only one stop bit used
    tty.c_cflag &= ~CSIZE; // Clear all the size bits
    tty.c_cflag |= CS8; // 8 bits per byte
    tty.c_cflag &= ~CRTSCTS; // Disable RTS/CTS hardware flow control
    tty.c_cflag |= CREAD | CLOCAL; // Turn on READ & ignore ctrl lines

    tty.c_lflag &= ~ICANON;
    tty.c_lflag &= ~ECHO; // Disable echo
    tty.c_lflag &= ~ECHOE; // Disable erasure
    tty.c_lflag &= ~ECHONL; // Disable new-line echo
    tty.c_lflag &= ~ISIG; // Disable interpretation of INTR, QUIT and SUSP
    tty.c_iflag &= ~(IXON | IXOFF | IXANY); // Turn off s/w flow ctrl
    tty.c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL); // Disable any special handling of received bytes

    tty.c_oflag &= ~OPOST; // Prevent special interpretation of output bytes
    tty.c_oflag &= ~ONLCR; // Prevent conversion of newline to carriage return/line feed

    tty.c_cc[VTIME] = 10; // Wait for up to 1s (10 deciseconds), returning as soon as any data is received.
    tty.c_cc[VMIN] = 0;

    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        perror("open_serial_port: tcsetattr");
        close(fd);
        return -1;
    }

    return fd;
}

void process_line(const char* line, double* latest_angle_value) {
    char* endptr;
    *latest_angle_value = strtod(line, &endptr);
    // if (line == endptr)
        // printf("Could not convert angle value to float: '%s'\n", line);
}

double readCompass(int sp){

    char read_buf[256];
    double latest_angle_value = 0.0;


    int num_bytes = read(sp, read_buf, sizeof(read_buf) - 1);
    if (num_bytes < 0) {
        perror("Error reading: ");
        return 1;
    }
    if (num_bytes > 0) {
        read_buf[num_bytes] = '\0';
        process_line(read_buf, &latest_angle_value);
    }
    return latest_angle_value;
    sleep(0.1); // Sleep for 100 milliseconds
}
