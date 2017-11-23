import piplates.DAQCplate as DAQC
import time
from decimal import Decimal
DAQC.setDOUTbit(0,0) 
#thermistor reading function
def compressor(state=None):
    if state==None:
        return DAQC.getDOUTbyte(0)
    if state==True:
        DAQC.setDOUTbit(0,0) 
    if state==False:
        DAQC.clrDOUTbit(0,0) 

def temp_get(volts,supply_voltage=5):
    divider_resistor=10000
    ohms = Decimal(divider_resistor*supply_voltage/volts-divider_resistor) #calculate the ohms of the thermisttor
    #IVT oem NTC
    a = Decimal(1.298022762e-3)
    b = Decimal(2.365068126e-4)
    c = Decimal(0.9305914923e-7)
    #Steinhart Hart Equation
    # T = 1/(a + b[ln(ohm)] + c[ln(ohm)]^3)
    temp = 1/(a + b*ohms.ln() + c*ohms.ln()**3) 
    tempc = temp - Decimal(273.15) #K to C
    return tempc

while(True):
    vv_retur=temp_get(DAQC.getADC(0,0),DAQC.getADC(0,8))
    hetgas=temp_get(DAQC.getADC(0,1),DAQC.getADC(0,8))
    print("VV retur:",vv_retur)
    print("Hetgas:",hetgas)
    print("Kompressor:",compressor())
    if vv_retur < 35:
        compressor(True)
        print("Returtemp under 35. Startar kompressor")
    if vv_retur > 45:
        compressor(False)
        print("Returtemp över 45. Stänger av kompressor")
#    import pdb;pdb.set_trace()
    time.sleep(1)

