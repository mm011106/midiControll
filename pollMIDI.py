#!/usr/bin/python3
# -*- coding: utf8 -*-

#
#
#
#

import time
import rtmidi2
from polling import poll

def callback(msg, delta_time):
	# print(msg, delta_time)
	global pad
	global flag
	global pad_mode
	global xypad_begin_at, xypad_currentry_at, flag_xypad

# MIDI message difinition
	NOTE_ON=144
	NOTE_OFF=128
	CC=176 			#CC message ID = 176 = 0xB0   MIDI Channel:0
	CC_XYPAD_TOUCH=16
	CC_XYPAD_X_VALUE=1
	CC_XYPAD_Y_VALUE=2

	if msg[0]==NOTE_ON:
		note_number=msg[1]
		print("Pad On:",note_number)

		try:
			if pad_mode[pad[note_number]]==SW_ALT:
				flag[pad[note_number]]=not(flag[pad[note_number]])
			else: # Momentary mode
				flag[pad[note_number]]=True
		except KeyError as e:
				print('No function related on the pad',e)

	elif msg[0]==NOTE_OFF:
		note_number=msg[1]
		print("Pad off:",note_number)

		try:
			if pad_mode[pad[note_number]]==SW_MOMENTARY:
				flag[pad[note_number]]=False
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
				flag_xypad=False

		elif controll_number == CC_XYPAD_X_VALUE:
			# print('X value', cc_value)
			xypad_currentry_at['x']=cc_value

		elif controll_number == CC_XYPAD_Y_VALUE:
			# print('Y value', cc_value)
			xypad_currentry_at['y']=cc_value

		#	set start position and Now Touching-flag
		if xypad_currentry_at['x']>0 and xypad_currentry_at['y']>0 and not(flag_xypad):
			xypad_begin_at['x']=xypad_currentry_at['x']
			xypad_begin_at['y']=xypad_currentry_at['y']
			flag_xypad = not flag_xypad
			print('!!')




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

# switch mode difinition
SW_ALT=1
SW_MOMENTARY=0

#functions=('fine','offset','ib','reset','fb','int','8hz')
pad={36:'fine', 42:'offset',43:'ib', 44:'reset', 46:'fb', 48:'int', 50:'8hz'}
pad_mode={'fine':SW_MOMENTARY, 'offset':SW_ALT, 'ib':SW_ALT, 'reset':SW_MOMENTARY, 'fb':SW_ALT, 'int':SW_ALT, '8hz':SW_ALT}

flag={'fine':False, 'offset':False, 'ib':False, 'reset':False, 'fb':False, 'int':False, '8hz':False}


xypad_begin_at={}
xypad_currentry_at={'x':-1,'y':-1}
flag_xypad=False

while True:
	time.sleep(1)
	print(xypad_begin_at, xypad_currentry_at, flag_xypad)

	# print(flag)
