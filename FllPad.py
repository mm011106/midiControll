#!/usr/bin/python3
# -*- coding: utf8 -*-

#
#
#
#

import time
import rtmidi2

def callback(msg, delta_time):
	# print(msg, delta_time)
	global pad
	global pad_flag
	global pad_mode
	global xypad_begin_at, xypad_currentry_at, xypad_flag

# MIDI message difinition
	NOTE_ON=144
	NOTE_OFF=128
	CC=176 			#CC message ID = 176 = 0xB0   MIDI Channel:0
	CC_XYPAD_TOUCH=16
	CC_XYPAD_X_VALUE=1
	CC_XYPAD_Y_VALUE=2

	if msg[0]==NOTE_ON:
		note_number=msg[1]

		try:
			# print("Pad On:",pad[note_number][pad_name])
			if pad[note_number][pad_mode]==SW_ALT:
				pad[note_number][pad_flag]=not(pad[note_number][pad_flag])
			else: # Momentary mode
				pad[note_number][pad_flag]=True
		except KeyError as e:
			print('No function related on the pad',e)

	elif msg[0]==NOTE_OFF:
		note_number=msg[1]

		try:
			# print("Pad off:",pad[note_number][pad_name])
			if pad[note_number][pad_mode]==SW_MOMENTARY:
				pad[note_number][pad_flag]=False
		except KeyError as e:
			print('No function related on the pad',e)

	elif msg[0]==CC:
		controll_number=msg[1]
		cc_value=msg[2]

		if controll_number == CC_XYPAD_TOUCH:
			# print('XY-pad Touched:', cc_value==127)
			if cc_value != 127:  # XYpad released : clear flag and position
				xypad_begin_at={}
				xypad_currentry_at={'x':-1,'y':-1}
				xypad_flag=False

		elif controll_number == CC_XYPAD_X_VALUE:
			# print('X value', cc_value)
			xypad_currentry_at['x']=cc_value

		elif controll_number == CC_XYPAD_Y_VALUE:
			# print('Y value', cc_value)
			xypad_currentry_at['y']=cc_value

		#	set start position and Now-Touching flag
		if xypad_currentry_at['x']>0 and xypad_currentry_at['y']>0 and not(xypad_flag):
			xypad_begin_at['x']=xypad_currentry_at['x']
			xypad_begin_at['y']=xypad_currentry_at['y']
			xypad_flag = not xypad_flag
			print('!!')


def make_pad_state(pads):
	global pad_name, pad_flag
	pad_state={}
	for value in pads.values():
		pad_state[value[pad_name]]=value[pad_flag]

	return pad_state  # returns Dic type value

def measure_distance(start, now):  # args must be contain {'x': x_value, 'y': y:value}
	global xypad_flag
	dx=0
	dy=0

	if xypad_flag:
		# print(start, now)
		dx=now['x']-start['x']
		dy=now['y']-start['y']

	return dx,dy

# switch mode difinition
SW_ALT=1
SW_MOMENTARY=0

# difinition of the pads functionality: NoteNumber:['name', swtch mode, initial vaule(boolean)]
pad={
36:['fine', SW_MOMENTARY, False],
42:['offset', SW_ALT, False],
43:['ib', SW_ALT, False],
44:['reset', SW_MOMENTARY, False],
46:['fb', SW_ALT, False],
48:['int', SW_ALT, False],
50:['8hz', SW_ALT, False]
}

# index num of the values of 'pad'
pad_name=0
pad_mode=1
pad_flag=2

xypad_begin_at={}
xypad_currentry_at={'x':-1,'y':-1}
xypad_flag=False

if __name__=='__main__':

	midi_in=rtmidi2.MidiIn()
	print(midi_in.ports)

	midi_in.callback=callback

	device_name="nanoPAD2"

	try:
		index = midi_in.ports_matching(device_name+"*")[0]
		input_port=midi_in.open_port(index)
		print(index)
	except indexError:
		raise(IOError("Input port not found."))

	while True:
		time.sleep(0.5)
		print(measure_distance(xypad_begin_at,xypad_currentry_at))
		pad_state = make_pad_state(pad)
		print(pad_state)

		# print(flag)
