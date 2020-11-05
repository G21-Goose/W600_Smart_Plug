# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal
import network
import easyw600
import utime
import machine

machine.Pin(machine.Pin.PB_15,machine.Pin.OUT,machine.Pin.PULL_DOWN)

print("")
print("    WinnerMicro W600")
print("")
SSID="ssid"
PSK="psk"
help()
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect(SSID,PSK)
print("")
print("Connecting")
blueLED=machine.Pin(machine.Pin.PB_08,machine.Pin.OUT,machine.Pin.PULL_DOWN)
blueLED.value(1)
attempts=0
retry=0
while(sta_if.isconnected()==False):
	attempts=attempts+1
	print(".",end="")
	utime.sleep(1)
	blueLED.value(1-blueLED.value())
	if(attempts>10):
		sta_if.connect(SSID,PSK)
		attempts=0
		retry=retry+1
		print("Trying Again")
	if(retry>4):
		print("Launching soft ap")
		easyw600.createap(ssid="softap") #Open Network
		break
		
print("")
print("IP:",sta_if.ifconfig()[0])
easyw600.ftpserver()#User root Password root