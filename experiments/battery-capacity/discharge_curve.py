import pyvisa
import time
import pandas as pd

iMax = 125E-3
iMin = iMax/10
vMax = 2.85
vMin = 1.5

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

inst.write('OUTP:STATE OFF')

inst.write('SOURCE:CURR -{};'.format(str(iMax)))
inst.write('OUTP:STATE ON')

data = []

while(1):
    t = time.time()
    current = float(inst.query('MEAS:CURR?'))
    voltage = float(inst.query('MEAS:VOLT?'))
    print(t, current, voltage)
    data.append([t, voltage, current])
    if (voltage <= vMin):
        break;
    time.sleep(1)

inst.write('OUTP:STATE OFF')

db = pd.DataFrame(data, columns=['Time', 'Voltage', 'Current'], dtype = float)
db.set_index('Time', inplace=True)
db.to_csv("discharge_curve.csv")
