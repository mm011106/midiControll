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
	global xypad
	global PAD_FLAG, PAD_MODE

# MIDI message difinition
	NOTE_ON=144
	NOTE_OFF=128
	CC=176 			#CC message ID = 176 = 0xB0   MIDI Channel:0
	CC_XYPAD_TOUCH=16
	CC_XYPAD_X_VALUE=1
	CC_XYPAD_Y_VALUE=2

# read keypads and xy-pads
	if msg[0]==NOTE_ON:
		note_number=msg[1]

		try:
			# print("Pad On:",pad[note_number][PAD_NAME])
			if pad[note_number][PAD_MODE]==SW_ALT:
				pad[note_number][PAD_FLAG]=not(pad[note_number][PAD_FLAG])
			else: # Momentary mode
				pad[note_number][PAD_FLAG]=True
		except KeyError as e:
			print('No function related on the pad',e)

		#  things to do at the onset of the note on
		note_on_triggered_function(pad )

	elif msg[0]==NOTE_OFF:
		note_number=msg[1]

		try:
			# print("Pad off:",pad[note_number][PAD_NAME])
			if pad[note_number][PAD_MODE]==SW_MOMENTARY:
				pad[note_number][PAD_FLAG]=False
		except KeyError as e:
			print('No function related on the pad',e)

	elif msg[0]==CC:
		controll_number=msg[1]
		cc_value=msg[2]

		if controll_number == CC_XYPAD_TOUCH:
			# print('XY-pad Touched:', cc_value==127)
			if cc_value != 127:  # XYpad released : clear flag and position
				xypad['begin']={}
				xypad['current']={'x':-1,'y':-1}
				xypad['flag']=False

		elif controll_number == CC_XYPAD_X_VALUE:
			# print('X value', cc_value)
			xypad['current']['x']=cc_value

		elif controll_number == CC_XYPAD_Y_VALUE:
			# print('Y value', cc_value)
			xypad['current']['y']=cc_value

		#	set start position and Now-Touching flag

	midi_receive_triggered_function(pad, xypad)



def midi_receive_triggered_function(pad, xypad):

	global fll_ib_begin_at, fll_ofs_begin_at
	global speed_factor

	global fll_parameter

# xypad is ready to use? (need intial positon)
	if xypad['current']['x']>0 and xypad['current']['y']>0 and not(xypad['flag']):
		xypad['begin']['x']=xypad['current']['x']
		xypad['begin']['y']=xypad['current']['y']
		xypad['flag'] = not xypad['flag']
		# print(fll_ib, fll_ofs , '!!')

		fll_ofs_begin_at = fll_parameter['ofs']
		fll_ib_begin_at = fll_parameter['ib']

# fine-coarse adjustment settings  Normally:Coarse, with Pad:Fine
	if read_pad_state(pad)['fine']:
		speed_factor=1
	else:
		speed_factor=8

# Read XY-Pad
	if xypad['flag']:
		dist = measure_distance(xypad)

		fll_parameter['ofs'] = dist[1]*speed_factor + fll_ofs_begin_at
		#limitter range of 12bit
		if fll_parameter['ofs']>2047:
			fll_parameter['ofs']=2047
		elif fll_parameter['ofs']<-2048:
			fll_parameter['ofs']=-2048

		fll_parameter['ib']  = dist[0]*speed_factor + fll_ib_begin_at
	#limitter range of 12bit
		if fll_parameter['ib']>4095:
			fll_parameter['ib']=4095
		elif fll_parameter['ib']<0:
			fll_parameter['ib']=0



# Reset feedback loop
	if read_pad_state(pad)['reset']:
		set_pad_state_by_function_name(pad, 'int', False)
		set_pad_state_by_function_name(pad, 'fb', False)
		# set_pad_state_by_function_name(pad, '8hz', False)



def note_on_triggered_function(pad):
	global fll_parameter
	global squid_parameter

	ch   = fll_parameter['ch']
	unit = fll_parameter['unit']

	ib, ofs = [fll_parameter['ib'],fll_parameter['ofs']]

	print(squid_parameter[unit*16+ch])
	squid_parameter[unit*16+ch]=[ib,ofs]

	if read_pad_state(pad)['ch_up']:
		ch+=1 if ch<15 else 0
		ib,ofs =squid_parameter[unit*16+ch]

	if read_pad_state(pad)['ch_down']:
		ch-=1 if ch>0 else 0

	if read_pad_state(pad)['unit_up']:
		unit+=1 if unit<15 else 0

	if read_pad_state(pad)['unit_down']:
		unit-=1 if unit>0 else 0

	[ib, ofs] = squid_parameter[unit*16+ch]

	#reset ib, ofs value by user
	if read_pad_state(pad)['zero'] and read_pad_state(pad)['reset']:
		ib  = 0
		ofs = 0

	fll_parameter['ch'] = ch
	fll_parameter['unit'] = unit

	fll_parameter['ib'] = ib
	fll_parameter['ofs'] = ofs



def read_pad_state(pads):
	global PAD_NAME, PAD_MODE, PAD_FLAG
	pad_state={}
	for value in pads.values():
		pad_state[value[PAD_NAME]]=value[PAD_FLAG]

	return pad_state  # returns Dic type value


def set_pad_state_by_function_name(pad, func_name, state):
	global PAD_NAME, PAD_MODE, PAD_FLAG

	for note_number in pad.keys():
		if pad[note_number][PAD_NAME]==func_name:
			pad[note_number][PAD_FLAG]=state

	return


def measure_distance(xypad):  # args must be contain {'x': x_value, 'y': y:value}
	dx=0
	dy=0

	if xypad['flag']:
		# print(start, now)
		dx=xypad['current']['x']-xypad['begin']['x']
		dy=xypad['current']['y']-xypad['begin']['y']

	return dx,dy

# switch mode difinition
SW_ALT=1
SW_MOMENTARY=0

# difinition of the pads functionality: NoteNumber:['name', swtch mode, initial vaule(boolean)]
pad={
36:['fine', SW_MOMENTARY, False],
37:['zero', SW_MOMENTARY, False],
38:['ch_down', SW_MOMENTARY, False],
39:['ch_up', SW_MOMENTARY, False],
40:['unit_down', SW_MOMENTARY, False],
41:['unit_up', SW_MOMENTARY, False],
42:['offset', SW_ALT, False],
43:['ib', SW_ALT, False],
44:['reset', SW_MOMENTARY, False],
46:['fb', SW_ALT, False],
48:['int', SW_ALT, False],
50:['8hz', SW_ALT, False]
}

# index num of the values of 'pad'
PAD_NAME=0
PAD_MODE=1
PAD_FLAG=2

# def values

xypad={
'begin':{},
'current':{'x':-1,'y':-1},
'flag':False
}

fll_parameter={
'ch':0,
'unit':0,
'ofs':0,
'ib':0,
'en_ofs':False,
'en_ib':False,
'fb':False,
'int':False,
'8hz':False,
'out_hi':False,
'out_mid':False,
'out_hi':False
}

squid_parameter={}
for i in range(256):
	squid_parameter[i]=[0,0]


speed_factor=1
fll_ofs_begin_at=0
fll_ib_begin_at=0




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
		time.sleep(0.2)
		# print(measure_distance(xypad_begin_at,xypad_currentry_at))
		print(fll_parameter['ib'], fll_parameter['ofs'])
		print('unit:',fll_parameter['unit'],'   ','ch:',fll_parameter['ch'])
		pad_state = read_pad_state(pad)
		print(pad_state)

		# print(flag)
