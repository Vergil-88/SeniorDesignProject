#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>
#include <math.h>
#include <gsl/gsl_multifit_nlin.h>

// Define struct for positions
typedef struct {
    double x;
    double y;
} Position;

Position anchor_positions[4] = {
    {-4.5, 4.5},   // Anchor A1710 position
    {4.5, 4.5},    // Anchor A1720 position
    {-4.5, -4.5},  // Anchor A30 position
    {4.5, -4.5}    // Anchor A40 position
};

double ranges[4];  // To store range measurements

void process_line(char *line) {
    char *ptr, *endptr;
    double value;
    if ((ptr = strstr(line, "Range:")) != NULL) {
        value = strtod(ptr + 6, &endptr);  // Skip "Range:" and parse the number
        if (endptr != ptr) {  // Check for a valid conversion
            if (strstr(line, "from: 1710")) ranges[0] = fabs(value);
            if (strstr(line, "from: 1720")) ranges[1] = fabs(value);
            if (strstr(line, "from: 30"))   ranges[2] = fabs(value);
            if (strstr(line, "from: 40"))   ranges[3] = fabs(value);
        }
    }
}

int open_serial(const char *portname) {
    int fd = open(portname, O_RDWR | O_NOCTTY | O_SYNC);
    if (fd < 0) {
        perror("Error opening serial port");
        return -1;
    }

    struct termios tty;
    memset(&tty, 0, sizeof tty);
    if (tcgetattr(fd, &tty) != 0) {
        perror("Error from tcgetattr");
        close(fd);
        return -1;
    }

    cfsetospeed(&tty, B115200);
    cfsetispeed(&tty, B115200);

    tty.c_cflag |= (CLOCAL | CREAD);    // Enable reading
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;                 // 8-bit chars
    tty.c_iflag &= ~(IXON | IXOFF | IXANY); // Shut off xon/xoff ctrl
    tty.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG); // raw input
    tty.c_oflag &= ~OPOST;              // raw output

    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        perror("Error from tcsetattr");
        close(fd);
        return -1;
    }

    return fd;
}

int expb_f(const gsl_vector * x, void *data, gsl_vector * f) {
    double x_est = gsl_vector_get(x, 0);
    double y_est = gsl_vector_get(x, 1);
    double *d = (double *)data;

    for (int i = 0; i < 4; i++) {
        double dx = x_est - anchor_positions[i].x;
        double dy = y_est - anchor_positions[i].y;
        double dist = sqrt(dx * dx + dy * dy);
        gsl_vector_set(f, i, (dist - d[i]));
    }
    return GSL_SUCCESS;
}

void solve_position(double *x, double *y) {
    const gsl_multifit_nlinear_type *T = gsl_multifit_nlinear_trust;
    gsl_multifit_nlinear_parameters fdf_params = gsl_multifit_nlinear_default_parameters();
    const size_t n = 4;  // number of equations
    const size_t p = 2;  // number of unknowns (x, y)

    gsl_vector *f;
    gsl_matrix *covar = gsl_matrix_alloc(p, p);
    double x_init[2] = { 0.0, 0.0 };  // Initial guess
    gsl_vector_view x = gsl_vector_view_array(x_init, p);
    gsl_multifit_nlinear_workspace *w;
    gsl_multifit_nlinear_fdf fdf;
    int status, info;

    fdf.f = expb_f;
    fdf.df = NULL;   // Set to NULL for finite-difference Jacobian.
    fdf.fvv = NULL;  // Not using geodesic acceleration
    fdf.n = n;
    fdf.p = p;
    fdf.params = &ranges;

    w = gsl_multifit_nlinear_alloc(T, &fdf_params, n, p);
    gsl_multifit_nlinear_init(&x.vector, &fdf, w);
    gsl_multifit_nlinear_driver(20, 1e-8, 1e-8, 0, NULL, &info, w);

    f = gsl_multifit_nlinear_residual(w);
    gsl_vector_view xview = gsl_multifit_nlinear_position(w);
    *x = gsl_vector_get(&xview.vector, 0);
    *y = gsl_vector_get(&xview.vector, 1);

    gsl_multifit_nlinear_free(w);
    gsl_matrix_free(covar);
}

int main(void) {
    int fd = open_serial("/dev/tty.usbserial-02619786");
    if (fd < 0) return -1;

    char buf[1024];
    int n;
    double x, y;

    while (1) {
        n = read(fd, buf, sizeof(buf) - 1);
        if (n > 0) {
            buf[n] = '\0';
            process_line(buf);
            solve_position(&x, &y);  // Call function to solve position
            printf("Estimated Position: (%.2f, %.2f)\n", x, y);
        }
    }
    close(fd);
    return 0;
}
