import pyvisa
import time
import pandas as pd

iMax = 70E-3
iMin = iMax/10
vMax = 3.5
vMin = 2.0

rm = pyvisa.ResourceManager()
print(rm.list_resources())
inst = rm.open_resource('TCPIP::192.168.0.224::INSTR')
print(inst.query('*IDN?'))
inst.write('SOURCE:FUNC:MODE CURR')
inst.write('SOURCE:CURR {};'.format(str(iMax/2)))
inst.write('SENSE:VOLT:PROT {};'.format(str(vMax)))
inst.write('OUTP:STATE ON')

while(1):
    current = float(inst.query('MEAS:CURR?'))
    voltage = float(inst.query('MEAS:VOLT?'))
    print(current, voltage)
    if (current > 0 and current <= iMin):
        break;
    time.sleep(1)
