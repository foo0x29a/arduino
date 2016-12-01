#!/usr/bin/python

import matplotlib.pyplot as plt
import subprocess as sub
import serial

def get_serial_port():
	cmd = 'dmesg | egrep ttyACM | cut -f3 -d: | tail -n1'
	p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
	out, err = p.communicate()
	return '/dev/' + out.strip()
	#return '/dev/ttyUSB0'

def serial_write(ser, string):
	print string
	ser.write(string + '\n')

# Plotting algorithms from: http://members.chello.at/easyfilter/bresenham.html

def draw_circle(xm, ym, r):
	x = - r
	y = 0
	err = 2 - 2 * r
	p1 = []
	p2 = []
	p3 = []
	p4 = []
	while True:
		p1.append((xm - x, ym + y)) # 1st quadrant
		p2.append((xm - y, ym - x)) # 2nd quadrant
		p3.append((xm + x, ym - y)) # 3rd quadrant
		p4.append((xm + y, ym + x)) # 4th quadrant
		r = err
		if(r <= y):
			y += 1
			err += y * 2 + 1
		if(r > x or err > y):
			x += 1
			err += x * 2 + 1
		if(x >= 0):
			#return p1 + p2 + p3 + p4
			p1.reverse()
			p2.reverse()
			p3.reverse()
			p4.reverse()
			return p4 + p3 + p2 + p1

def draw_ellipse(xm, ym, a, b):
	x0 = xm - a
	x1 = xm + a
	y0 = ym - b
	y1 = ym + b
	b1 = b & 1
	dx = 4 * (1 - a) * b * b
	dy = 4 * (b1 + 1) * a * a
	err = dx + dy + b1 * a * a
	e2 = 0 # Dumb value
	#""" Starting pixels
	y0 += (b + 1) / 2
	y1 = y0 - b1
	#"""
	#"""
	a *= 8 * a
	b1 = 8 * b * b
	#"""
	p1 = []
	p2 = []
	p3 = []
	p4 = []
	while True:
		p1.append((x1, y0)) # 1st quadrant
		p2.append((x0, y0)) # 2nd quadrant
		p3.append((x0, y1)) # 3rd quadrant
		p4.append((x1, y1)) # 4th quadrant
		e2 = 2 * err
		if e2 <= dy:
			y0 += 1
			y1 -= 1
			#err += dy += a
			dy += a
			err += dy
		if e2 >= dx or 2 * err > dy:
			x0 += 1
			x1 -= 1
			#err += dx += b1
			dx += b1
			err += dx
		if x0 > x1:
			break

	while y0 - y1 < b: # In too early break
		p1.append((x0 - 1, y0))
		p2.append((x1 + 1, y0))
		y0 += 1
		p3.append((x0 - 1, y1))
		p4.append((x1 + 1, y1))
		y1 -= 1
	return p1 + p2 + p3 + p4

def draw_line(x0, y0, x1, y1):
	dx = abs(x1 - x0)
	sx = 1 if x0 < x1 else -1
	dy = -abs(y1 - y0)
	sy = 1 if y0 < y1 else -1
	err = dx + dy
	e2 = 0 # Dumb value
	points = []
	while True:
		points.append((x0, y0))
		if x0 == x1 or y0 == y1:
			return points
		e2 = 2 * err
		if e2 >= dy:
			err += dy
			x0 += sx
		if e2 <= dx:
			err += dx
			y0 += sy

def draw(ser, t):
	import time
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

		time.sleep(0.3)

def plot_twitter(p, name):
	x = []
	y = []

	plt.ylabel(name)
	for i in p:
		x.append(i[0])
		y.append(i[1])

	plt.plot(x,y)
	plt.show()

def plot_twister_carpado(p, name):

	plt.ylabel(name)

	for i in p:
		plt.plot(i)

	plt.show()

def init():
	port = get_serial_port()
	ser = serial.Serial(port, 9600)
	return ser


import sys,tty,termios
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k=='\x1b[A':
		serial_write(ser, "INC_Y")
                print "up"
        elif k=='\x1b[B':
		serial_write(ser, "DEC_Y")
                print "down"
        elif k=='\x1b[C':
		serial_write(ser, "INC_X")
                print "right"
        elif k=='\x1b[D':
		serial_write(ser, "DEC_X")
                print "left"
        elif k=='\x40':
		serial_write(ser, "Z_DOWN")
                print "Z_DOWN"        
        elif k=='\x32':
		serial_write(ser, "Z_UP")
                print "Z_UP"
        else:
                exit(1)

if __name__=='__main__':

	ser = init()
	while(1):
		get()
