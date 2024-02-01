#include <gtk/gtk.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

#define TCP_IP "192.168.4.1"
#define TCP_PORT 8000
#define READ_BUFFER_SIZE 22
#define TIMEOUT 20

static int speed = 0;
static int steer = 0;
static int sockfd = -1;

///////////////////////////////TCP SOCKET///////////////////////////////
int TCP_init() {
    if (sockfd >= 0) {
        close(sockfd);
    }

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("Error creating socket");
        return -1;
    }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(TCP_PORT);

    if (inet_pton(AF_INET, TCP_IP, &server_addr.sin_addr) <= 0) {
        perror("Invalid address/ Address not supported");
        return -1;
    }

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection Failed");
        return -1;
    }

    printf("Connected successfully\n");

    struct timeval tv;
    tv.tv_sec = TIMEOUT;
    tv.tv_usec = 0;
    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv) < 0) {
        perror("Error setting timeout");
        return -1;
    }

    return sockfd;
}

///////////////////////////////SEND via TCP///////////////////////////////
void send_command(int s, int16_t speed, int16_t steer) {
    uint16_t start = 43981;
    if (steer < 0) {
        steer += 65536;
    }
    uint16_t steerp = (uint16_t)steer;

    if (speed < 0) {
        speed += 65536;
    }
    uint16_t speedp = (uint16_t)speed;

    uint16_t chkSum = (start ^ steerp) ^ speedp;

    uint16_t write_buffer[4] = {start, steerp, speedp, chkSum};
    char send_buffer[8];
    memcpy(send_buffer, write_buffer, 8);

    send(s, send_buffer, 8, 0);
}

uint16_t bytesToUint16(uint8_t highByte, uint8_t lowByte) {
    return (uint16_t)(highByte << 8 | lowByte);
}

///////////////////////////////receive ///////////////////////////////
int receive(int s, int debug) {
    uint8_t feedback[22];
    ssize_t bytes_received = recv(s, feedback, 22, 0);
    
    if (bytes_received < 0) {
        perror("recv failed");
        return -1;
    }

    if (bytes_received >= 22) {
        uint16_t header = bytesToUint16(feedback[1], feedback[0]);
        uint16_t cmd1 = bytesToUint16(feedback[3], feedback[2]);
        uint16_t cmd2 = bytesToUint16(feedback[5], feedback[4]);
        uint16_t spdR = bytesToUint16(feedback[7], feedback[6]);
        uint16_t spdL = bytesToUint16(feedback[9], feedback[8]);
        uint16_t cntR = bytesToUint16(feedback[11], feedback[10]);
        uint16_t cntL = bytesToUint16(feedback[13], feedback[12]);
        uint16_t batV = bytesToUint16(feedback[15], feedback[14]);
        uint16_t temp = bytesToUint16(feedback[17], feedback[16]);
        uint16_t cmdLED = bytesToUint16(feedback[19], feedback[18]);
        uint16_t chkSum = bytesToUint16(feedback[21], feedback[20]);

        if (debug) {
            printf("Speed: %d | Temp: %d | Voltage: %d\n", cmd2, temp, batV);
        }
    }

    return 0;
}

///////////////////////////////GUI method///////////////////////////////
static gboolean on_key_press(GtkWidget *widget, GdkEventKey *event, gpointer data) {
    switch (event->keyval) {
        case GDK_KEY_Left:
            steer -= 1;
            break;
        case GDK_KEY_Right:
            steer += 1;
            break;
        case GDK_KEY_Up:
            speed -= 1;
            break;
        case GDK_KEY_Down:
            speed += 1;
            break;
        case GDK_KEY_space:
            speed = 0;
            steer = 0;
            break;
    }

    if (steer < 0) steer += 65536;
    if (speed < 0) speed += 65536;

    g_print("Speed: %d, Steer: %d\n", speed, steer);

    send_command(sockfd, speed, steer);
    return TRUE;
}

///////////////////////////////THREAD///////////////////////////////
void *receive_thread_func(void *arg) {
    int s = *(int *)arg;
    while (1) {
        if (receive(s, 1) < 0) {
            printf("Attempting to reconnect...\n");
            close(s);
            s = TCP_init();
            if (s < 0) {
                fprintf(stderr, "Reconnection failed, retrying...\n");
                sleep(5);
                continue;
            }
            printf("Reconnected successfully\n");
        }
    }
    return NULL;
}

///////////////////////////////START OF MAIN///////////////////////////////
int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);

    sockfd = TCP_init();
    if (sockfd < 0) {
        fprintf(stderr, "Failed to initialize TCP connection\n");
        return 1;
    }

    pthread_t recv_thread;
    if (pthread_create(&recv_thread, NULL, receive_thread_func, &sockfd) != 0) {
        fprintf(stderr, "Failed to create receive thread\n");
        return 1;
    }

    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    g_signal_connect(window, "key_press_event", G_CALLBACK(on_key_press), NULL);

    gtk_widget_show_all(window);

    gtk_main();
    close(sockfd);

    return 0;
}
