import piplates.DAQCplate as DAQC
import time
from decimal import Decimal
import os
import paho.mqtt.client as mqtt #import the client1
from prometheus_client import start_http_server, Summary, Gauge

#DAQC.setDOUTbit(0,0) 
#thermistor reading function
def compressor(state=None):
    if state==None:
        return DAQC.getDOUTbyte(0)
    if state==True:
        DAQC.setDOUTbit(0,0) 
    if state==False:
        DAQC.clrDOUTbit(0,0) 

def temp_get(volts,supply_voltage=5):
    divider_resistor=1500
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

def log(fp, data):
    print(*data,sep=',', file=fp)
    fp.flush()

fp = open("/var/tmp/heatpump.csv","w+")
start_http_server(8000)
running_g = Gauge('heatpump_running', 'Is the compressor running?')
top_g = Gauge('heatpump_toptemp', 'Temperature at top of tank.')
return_g = Gauge('heatpump_returntemp', 'Temperature at inlet sensor.')
gas_g = Gauge('heatpump_hottemp', 'Temperature at Hot Gas side sensor.')
while(True):
    vv_retur=temp_get(DAQC.getADC(0,0),DAQC.getADC(0,8))
    vv_top=temp_get(DAQC.getADC(0,2),DAQC.getADC(0,8))
    hetgas=temp_get(DAQC.getADC(0,1),DAQC.getADC(0,8))
    print("VV retur:",vv_retur)
    print("VV top:",vv_top)
    print("Hetgas:",hetgas)
    print("Kompressor:",compressor())
    log(fp, [vv_retur,vv_top,hetgas,str(compressor()[0])])
    broker_address="monitor.tranquillity.se" 
    client = mqtt.Client("P1") #create new instance
    client.connect(broker_address) #connect to broker
    client.publish("heatpump/running",str(compressor()[0]), retain=True)#publish
    client.publish("heatpump/toptemp",str(vv_top), retain=True)#publish
    client.publish("heatpump/returntemp",str(vv_retur), retain=True)#publish
    client.publish("heatpump/hottemp",str(hetgas), retain=True)#publish
    running_g.set(compressor()[0])
    top_g.set(vv_top)
    return_g.set(vv_retur)
    gas_g.set(hetgas)
    if vv_top < 47:
        compressor(True)
        print("Toptemp under 47. Startar kompressor")
    if vv_top > 51:
        compressor(False)
        print("Toptemp över 51. Stänger av kompressor")
#    import pdb;pdb.set_trace()
    time.sleep(1)

