import machine
import utime
from umqtt.simple import MQTTClient
import ubinascii
import ujson

#Unique Switch Number
SWITCH=1 ##### Change (Used for MQTT topic)

#BL0937 Constants-Not Implemented
'''
Vk=1
Ik=0.00677
Pk=1.422
'''
#BL0937 Pins
'''
SEL_Pin=machine.Pin(machine.Pin.PB_16,machine.Pin.OUT,machine.Pin.PULL_DOWN)
CF1=machine.Pin(machine.Pin.PB_13,machine.Pin.IN,machine.Pin.PULL_UP) #SEL=0 Current, SEL=1 Voltage
CF=machine.Pin(machine.Pin.PB_18,machine.Pin.IN,machine.Pin.PULL_UP) #Active Power
'''

machine.freq(80000000)

#MQTT Configuration
SERVER="x.x.x.x" ##### Change
USERNAME="username" ##### Change
PASSWORD="password" ##### Change
CLIENT_ID=ubinascii.hexlify(machine.unique_id())
TOPIC=b"switch/LSPA7/%s/cmd"%(str(SWITCH))
STATE_TOPIC=b"switch/LSPA7/%s/state"%(str(SWITCH))
c=MQTTClient(CLIENT_ID,SERVER,user=USERNAME,password=PASSWORD)

#Pins Configuration
relay=machine.Pin(machine.Pin.PB_15,machine.Pin.OUT,machine.Pin.PULL_DOWN)
relay.value(0)

blueLED=machine.Pin(machine.Pin.PB_08,machine.Pin.OUT,machine.Pin.PULL_DOWN)
blueLED.value(1)

#Button Stops Rx Pin from working

def switchPower(p):
	count=0
	while(p.value()==0):
		count=count+1
		utime.sleep_ms(10)
		if(count>2):
			relay.value(1-relay.value())
			c.publish(STATE_TOPIC,'{"power":"%s"}'%("on" if relay.value()==1 else "off"))
			count=0
			while(p.value()==0):
				utime.sleep_ms(10)
	utime.sleep_ms(500)

button=machine.Pin(machine.Pin.PA_05,machine.Pin.IN,machine.Pin.PULL_UP)
button.irq(handler=switchPower,trigger=machine.Pin.IRQ_FALLING)


def sub_cb(topic,msg):
	global c
	decoded=str(msg.decode('UTF-8'))
	try:
		parsed=ujson.loads(decoded)
	except:
		c.publish(STATE_TOPIC,'{"error":%s}'%("Malformed JSON"))
		return;

	if(str(parsed['power'])=="on"):
		relay.value(1)
		c.publish(STATE_TOPIC,'{"power":"%s"}'%("on"))
	elif(str(parsed['power'])=="off"):
		relay.value(0)
		c.publish(STATE_TOPIC,'{"power":"%s"}'%("off"))

def main():
	global c
	c.set_callback(sub_cb)
	c.connect()
	c.subscribe(TOPIC)
	c.publish(STATE_TOPIC,'{"power":"%s"}'%("off"))
	try:
		while 1:
			c.check_msg()
			utime.sleep(1)
	finally:
		c.disconnect()
		print("Disconnected")
main()