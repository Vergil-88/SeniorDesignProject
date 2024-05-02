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
    initCompass(); // Initialize and configure the compass serial port

    while (1) {
        char* line = readCompass();
        if (line && (isdigit(line[0]) || line[0] == '-')) {  // Check if the line starts with a digit or a minus sign
           // printf("Read line: %s\n", line);
            double value = strtod(line, NULL);
            printf("Converted value: %f\n", value);
        } else if (line) {
           // printf("Line does not start with a number or minus sign: %s\n", line);
        } else {
            printf("No data read or only newline was read.\n");
        }
        //sleep(1); // Delay for a second to manage the loop timing
    }

    return 0;
}


