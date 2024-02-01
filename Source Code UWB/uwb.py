import time
import turtle
import cmath
import socket
import json
import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import least_squares



hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
print("***Local ip:" + str(UDP_IP) + "***")
UDP_PORT = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((UDP_IP, UDP_PORT))
sock.listen(1)  # 接收的连接数
data, addr = sock.accept()

distance_a1_a2 = 9
meter2pixel = 350
range_offset = 0.9


def screen_init(width=1200, height=1200, t=turtle):
    t.setup(width, height)
    t.tracer(False)
    t.hideturtle()
    t.speed(0)


def turtle_init(t=turtle):
    t.hideturtle()
    t.speed(0)


def draw_line(x0, y0, x1, y1, color="black", t=turtle):
    t.pencolor(color)

    t.up()
    t.goto(x0, y0)
    t.down()
    t.goto(x1, y1)
    t.up()


def draw_fastU(x, y, length, color="black", t=turtle):
    draw_line(x, y, x, y + length, color, t)


def draw_fastV(x, y, length, color="black", t=turtle):
    draw_line(x, y, x + length, y, color, t)


def draw_cycle(x, y, r, color="black", t=turtle):
    t.pencolor(color)

    t.up()
    t.goto(x, y - r)
    t.setheading(0)
    t.down()
    t.circle(r)
    t.up()


def fill_cycle(x, y, r, color="black", t=turtle):
    t.up()
    t.goto(x, y)
    t.down()
    t.dot(r, color)
    t.up()


def write_txt(x, y, txt, color="black", t=turtle, f=('Arial', 12, 'normal')):

    t.pencolor(color)
    t.up()
    t.goto(x, y)
    t.down()
    t.write(txt, move=False, align='left', font=f)
    t.up()


def draw_rect(x, y, w, h, color="black", t=turtle):
    t.pencolor(color)

    t.up()
    t.goto(x, y)
    t.down()
    t.goto(x + w, y)
    t.goto(x + w, y + h)
    t.goto(x, y + h)
    t.goto(x, y)
    t.up()


def fill_rect(x, y, w, h, color=("black", "black"), t=turtle):
    t.begin_fill()
    draw_rect(x, y, w, h, color, t)
    t.end_fill()
    pass


def clean(t=turtle):
    t.clear()


def draw_ui(t):
    write_txt(-300, 250, "UWB Positon", "black",  t, f=('Arial', 32, 'normal'))
    fill_rect(-400, 200, 800, 40, "black", t)
    write_txt(-50, 205, "WALL", "yellow",  t, f=('Arial', 24, 'normal'))


def draw_uwb_anchor(x, y, txt, range, t):
    r = 20
    fill_cycle(x, y, r, "green", t)
    write_txt(x + r, y, txt + ": " + str(range) + "M",
              "black",  t, f=('Arial', 16, 'normal'))


def draw_uwb_tag(x, y, txt, t):
    pos_x =   int(x ) 
    pos_y =   int(y ) 
    # pos_x= int(x)
    # pos_y =int(y)
    r = 20
    fill_cycle(pos_x, pos_y, r, "blue", t)
    write_txt(pos_x, pos_y, txt + ": (" + str(x) + "," + str(y) + ")",
              "black",  t, f=('Arial', 16, 'normal'))


def read_data():

    line = data.recv(1024).decode('UTF-8')

    uwb_list = []

    try:
        uwb_data = json.loads(line)
        print(uwb_data)

        uwb_list = uwb_data["links"]
        for uwb_archor in uwb_list:
            print(uwb_archor)

    except:
        print(line)
    print("")

    return uwb_list


def tag_pos(a, b, c):
    # p = (a + b + c) / 2.0
    # s = cmath.sqrt(p * (p - a) * (p - b) * (p - c))
    # y = 2.0 * s / c
    # x = cmath.sqrt(b * b - y * y)
    cos_a = (b * b + c*c - a * a) / (2 * b * c)
    x = b * cos_a
    y = b * cmath.sqrt(1 - cos_a * cos_a)

    return round(x.real, 1), round(y.real, 1)


def uwb_range_offset(uwb_range):

    temp = uwb_range
    return temp


# def tag_pos_4_anchors(a1_range, a2_range, a3_range, a4_range, anchor_positions):
#     # Modify this function to calculate the tag's position based on the distances to the anchors and anchor positions.
#     # You can use a different positioning algorithm here.

#     # Example: Calculate the tag's position as the centroid of the anchor positions weighted by distances.
#     x = (a1_range * anchor_positions[0][0] + a2_range * anchor_positions[1][0] + a3_range * anchor_positions[2][0] + a4_range * anchor_positions[3][0]) / (a1_range + a2_range + a3_range + a4_range)
#     y = (a1_range * anchor_positions[0][1] + a2_range * anchor_positions[1][1] + a3_range * anchor_positions[2][1] + a4_range * anchor_positions[3][1]) / (a1_range + a2_range + a3_range + a4_range)

#     return x, y



def tag_pos_4_anchors(a1_range, a2_range, a3_range, a4_range, anchor_positions):
    # This function will now use trilateration to calculate the tag's position
    def equations(p):
        x, y = p
        return (
            (x - anchor_positions[0][0])**2 + (y - anchor_positions[0][1])**2 - a1_range**2,
            (x - anchor_positions[1][0])**2 + (y - anchor_positions[1][1])**2 - a2_range**2,
            (x - anchor_positions[2][0])**2 + (y - anchor_positions[2][1])**2 - a3_range**2,
            (x - anchor_positions[3][0])**2 + (y - anchor_positions[3][1])**2 - a4_range**2,
        )

    # Initial guess for the positions (can be improved based on your setup)
    x0, y0 = 0, 0

    result = least_squares(equations, (x0, y0))

    # Extract the solution
    x, y = result.x

    return x, y



def main():

    t_ui = turtle.Turtle()
    t_a1 = turtle.Turtle()
    t_a2 = turtle.Turtle()
    t_a3 = turtle.Turtle()
    t_a4 = turtle.Turtle()
    t_a5 = turtle.Turtle()
    
    turtle_init(t_ui)
    turtle_init(t_a1)
    turtle_init(t_a2)
    turtle_init(t_a3)
    turtle_init(t_a4)
    turtle_init(t_a5)

    a1_range = 0.0
    a2_range = 0.0
    a3_range = 0.0
    a4_range = 0.0
    # draw_ui(t_ui)

    while True:
        node_count = 0
        list = read_data()

        for one in list:
            if one["A"] == "1710":#toplift
                clean(t_a1)
                a1_range = uwb_range_offset(float(one["R"]))
#                draw_uwb_anchor(-250, 150, "A1710(0,0)", a1_range, t_a1)
                draw_uwb_anchor(-200, 200, "A1710(0,0)", a1_range, t_a1)
                node_count += 1

            if one["A"] == "1720":#topright
                clean(t_a2)
                a2_range = uwb_range_offset(float(one["R"]))
                draw_uwb_anchor(200,200
                                , "A1720(" + str(distance_a1_a2)+")", a2_range, t_a2)
                node_count += 1
            if one["A"] == "30":#bottom left
                clean(t_a4)
                a3_range = uwb_range_offset(float(one["R"]))
                draw_uwb_anchor(-200, -200, "A30(0,0)", a3_range, t_a4)
                node_count += 1

            if one["A"] == "40":#bottom right
                clean(t_a5)
                a4_range = uwb_range_offset(float(one["R"]))
                draw_uwb_anchor(200,-200, "A40(" + str(distance_a1_a2)+")", a4_range, t_a5)
                node_count += 1                


                anchor_positions = [
                    (-200, 200),  # A1710 position
                    (200, 200),  # A1720 position
                    (-200, -200),  # A30 position
                    (200, -200)  # A40 position
                ]
        if node_count == 4:
            
            
            x, y = tag_pos_4_anchors((a1_range*(400))/9, (a2_range*(400))/9, (a3_range*(400))/9, (a4_range*(400))/9, anchor_positions)

            print(x, y)
            clean(t_a3)
           
            x_avg = [0] * 10
            y_avg = [0] * 10
            i_Avg = 0
            
            i_Avg=i_Avg+1
            i_Avg= i_Avg%10
            
            x_avg[i_Avg]=x
            y_avg[i_Avg]=y         
            
            x_value =sum (x_avg)/10 
            y_value =sum (y_avg)/10 
            
            
            
            draw_uwb_tag(int(x),int(y), "TAG", t_a3)


        time.sleep(0.1)

    turtle.mainloop()


if __name__ == '__main__':
    main()