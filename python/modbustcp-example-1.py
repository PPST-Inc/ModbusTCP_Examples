# PPST ModbusTCP python example 1
# Version: 1.0.0
# Date: 11/07/2022
# Dependences:
# - pip install pymodbus==3.0.2
# - pip install pyModbusTCP==0.2.0
# Last tested with:
# - Python 3.10.5
# - pymodbus 3.0.2
# - pyModbusTCP 0.2.0

import time
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pyModbusTCP.client import ModbusClient

# Function to read a float measurement
def read_float_measurement(address):
	registers = connection.read_input_registers(address, 2)
	decoder = BinaryPayloadDecoder.fromRegisters(registers, Endian.Big, wordorder=Endian.Little)
	return decoder.decode_32bit_float()

# Function to read a float setpoint
def read_float_setpoint(address):
	registers = connection.read_holding_registers(address, 2)
	decoder = BinaryPayloadDecoder.fromRegisters(registers, Endian.Big, wordorder=Endian.Little)
	return decoder.decode_32bit_float()
	
# Function to write a float setpoint
def write_float_setpoint(address, value):
	builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
	builder.add_32bit_float(value)
	registers = builder.to_registers()
	return connection.write_multiple_registers(address, registers)
	
# ModbusTCP connection
address = input("Enter the IP address of the unit: ")
print('Connecting')
connection = ModbusClient(host=address)
status = connection.open()
if status is False:
    print('Connection error')

print('Setting voltage AC to 0 Vrms')
write_float_setpoint(3008, 0.0)

print('Setting frequency to 50 Hz')
write_float_setpoint(3000, 50.0)

print('Turning output on...')
connection.write_multiple_coils(4000, [True])
time.sleep(6)

print('Setting voltage AC to 30 Vrms')
write_float_setpoint(3008, 30.0)
time.sleep(2)

print('Reading frequency measurement')
voltage = read_float_measurement(1000)
print('Frequency measurement: ' + str(round(voltage, 2)) + ' Hz')

print('Reading RMS voltage measurement')
voltage = read_float_measurement(1032)
print('Voltage RMS measurement: ' + str(round(voltage, 2)) + ' Vrms')

print('Reading RMS current measurement')
current = read_float_measurement(1056)
print('Current RMS measurement: ' + str(round(current, 2)) + ' Arms')

print('Turning output off')
connection.write_multiple_coils(4000, [False])

print('Disconnecting')
connection.close()

print('Done')