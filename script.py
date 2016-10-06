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

# Plotting algorithms from: http://members.chello.at/easyfilter/bresenham.html

def draw_circle(xm, ym, r):
	x = - r
	y = 0
	err = 2 - 2 * r
	points = []
	while True:
		points.append((xm - x, ym + y)) # 1st quadrant
		points.append((xm - y, ym - x)) # 2nd quadrant
		points.append((xm + x, ym - y)) # 3rd quadrant
		points.append((xm + y, ym + x)) # 4th quadrant
		r = err
		if(r <= y):
			y += 1
			err += y * 2 + 1
		if(r > x or err > y):
			x += 1
			err += x * 2 + 1
		if(x >= 0):
			return points

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
	points = []
	while True:
		points.append((x1, y0)) # 1st quadrant
		points.append((x0, y0)) # 2nd quadrant
		points.append((x0, y1)) # 3rd quadrant
		points.append((x1, y1)) # 4th quadrant
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
		points.append((x0 - 1, y0))
		points.append((x1 + 1, y0))
		y0 += 1
		points.append((x0 - 1, y1))
		points.append((x1 + 1, y1))
		y1 -= 1
	return points		

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

		time.sleep(0.1)

def init():
	port = get_serial_port()
	ser = serial.Serial(port, 9600)
	return ser

if __name__=='__main__':
	ser = init()
	p = draw_line(100, 100, 200, 400)
	draw(ser, p)
