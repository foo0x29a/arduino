#!/usr/bin/python

import subprocess as sub
import serial

def get_serial_port():
	cmd = 'dmesg | egrep ttyACM | cut -f3 -d: | tail -n1'
	p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
	out, err = p.communicate()
	return '/dev/' + out.strip()

def serial_write(ser, string):
	print string
	ser.write(string + '\n')


# Based on: http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
def draw_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

def draw(ser, t):
	x0 = t[0][0]
	serial_write(ser, "MOV_X " + str(x0))
	y0 = t[0][1]
	serial_write(ser, "MOV_Y " + str(y0))
	for x1, y1 in t:
		if(x1 > x0):
			serial_write(ser, "INC_X")
		elif(x1 < x0):
			serial_write(ser, "DEC_X")
		if(y1 > y0):
			serial_write(ser, "INC_Y")
		elif(y1 < y0):
			serial_write(ser, "DEC_Y")
		x0 = x1
		y0 = y1

def init():
	port = get_serial_port()
	ser = serial.Serial(port, 9600)
	return ser

if __name__=='__main__':
	ser = init()
	p = draw_line(100, 100, 200, 400)
	draw(ser, p)
