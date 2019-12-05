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
	if msg: print(msg)
	time.sleep(0.01)

