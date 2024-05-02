#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>
#include "gyroCom.C"
#include "TCP.c"
#include <ctype.h>  // For isdigit()

// #define PI 3.14159265358979323846



typedef struct {
    double dx;
    double dy;
} Point;

Point position_xy(double angle, double distance) {
    Point p;
    angle = (M_PI * angle) / 180;
    p.dx = distance * cos(angle);
    p.dy = distance * sin(angle);
    return p;
}

double encoder_Acalcs(int cntR, int cntL, int cntR_prev, int cntL_prev) {
    // Adjust cntR based on conditions
    if ((cntR - cntR_prev) > 4500 || cntR > 8000) {
        cntR -= 9000;
    }

    // Adjust cntL based on conditions
    if ((cntL - cntL_prev) > 4500 || cntL > 8000) {
        cntL -= 9000;
    }

    // Calculate dR and dL
    int dR = cntR - cntR_prev;
    int dL = cntL - cntL_prev;

    // Constant coefficient
    double k = -0.5;

    // Calculate the encoder angle
    double encoder_angle = k * (dR - dL);

    return encoder_angle;
}

double encoder_Dcalcs(int cntR, int cntL, int cntR_prev, int cntL_prev) {
    // Adjust cntR based on conditions
    if ((cntR - cntR_prev) > 4500 || cntR > 8000) {
        cntR -= 9000;
    }

    // Adjust cntL based on conditions
    if ((cntL - cntL_prev) > 4500 || cntL > 8000) {
        cntL -= 9000;
    }

    // Calculate dR and dL
    int dR = cntR - cntR_prev;
    int dL = cntL - cntL_prev;

    // Calculate average of dR and dL
    int dAvg = (dR + dL) / 2;

    // Calculate the encoder distance
    double encoder_distance = (double)dAvg / 166;

    return encoder_distance;
}

// Function to calculate distance and angle between two points
double calc_dis_ang(double x1, double y1, double x2, double y2) {
    // Calculate the distance
    double distance = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
    
    // Calculate the angle in radians
    double angle_radians = atan2(y2 - y1, x2 - x1);
    
    // Convert angle to degrees
    double angle_degrees = angle_radians * (180.0 / M_PI);

    return distance, angle_degrees;
}



int main(void) {

    int sockfd = TCP_init();
    if (sockfd < 0) {
        fprintf(stderr, "Failed to initialize TCP connection\n");
        return 1;
    }
    send_command(sockfd,0,0);


     receive(sockfd,0);

    // pthread_t recv_thread;
    //     if (pthread_create(&recv_thread, NULL, receive_thread_func, &sockfd) != 0) {
    //     fprintf(stderr, "Failed to create receive thread\n");
    //     return 1;
    //     }


    initCompass(); // Initialize and configure the compass serial port
    double value;

    send_command(sockfd,0,0);

    printf("/n befro the loop");
    while (1) {
        // send_command(sockfd,0,0);
        // pthread_t recv_thread;
        // if (pthread_create(&recv_thread, NULL, receive_thread_func, &sockfd) != 0) {
        // fprintf(stderr, "Failed to create receive thread\n");
        // return 1;
        // }

        receive(sockfd,0);

        printf("\n while");

        char* line = readCompass();
        if (line && (isdigit(line[0]) || line[0] == '-')) {  // Check if the line starts with a digit or a minus sign
           // printf("Read line: %s\n", line);
            double value = strtod(line, NULL);
            printf("\n Converted value: %f\n", value);
        }
        printf("\n fuck C");
        printf("\n%d", value <= 45.00);
        if(value <= 45.00){
            send_command(sockfd,0,10);

            printf("\n hello");
        }
        else{
            send_command(sockfd,0,0);
            
            printf("\n else");
            break;
        }

        
    }

    
}



