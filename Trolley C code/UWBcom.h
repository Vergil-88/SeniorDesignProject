// serial_reader.h
#ifndef SERIAL_READER_H
#define SERIAL_READER_H

extern float X;  // Use these variables to get the values in main.c
extern float Y;

void process_line(char *line);
int initialize_serial_port(const char* port_name);
void read_serial_data(int fd);

#endif // SERIAL_READER_H

