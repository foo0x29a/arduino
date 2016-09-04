#!/usr/bin/python

import subprocess as sub
import serial

def get_serial_port():
	cmd = 'dmesg | egrep ttyACM | cut -f3 -d: | tail -n1'
	p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE, shell=True)
	out, err = p.communicate()
	return '/dev/'+out.strip()

if __name__=='__main__':
	port = get_serial_port()
	ser = serial.Serial(port, 9600)
	ser.write('`Hello|')
