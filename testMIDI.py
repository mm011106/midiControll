#!/usr/bin/python3
# -*- coding: utf8 -*-

import time
import rtmidi2

midi_in=rtmidi2.MidiIn()
print(midi_in.ports)

device_name="nanoPAD2"

try:
	index = midi_in.ports_matching(device_name+"*")[0]
	input_port=midi_in.open_port(index)
	print(index)
except indexError:
	raise(IOError("Input port not found."))

while True:
	msg=input_port.get_message()
	if msg:
		if msg[0]==144:
			print("Pad On:",msg[1])
		elif msg[0]==128:
			print("Pad off:",msg[1])
		elif msg[0]==176:
			if msg[1]==16:
				print('XY-pad Touched:', msg[2]==127)
			elif msg[1]==1:
				print('X value', msg[2])
			elif msg[1]==2:
				print('Y value', msg[2])


	time.sleep(0.01)
