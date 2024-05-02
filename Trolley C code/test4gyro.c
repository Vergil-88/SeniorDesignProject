#include "gyroCom.C"



int main(){
    int serial_port = open_serial_port("/dev/ttyACM0");

    if (serial_port < 0) return 1;
    while (1){
        double angle = readCompass(serial_port);

    //     printf("%f\n", angle);

    //    printf( "%d\n",angle >= 45 ); 
    }
    
}