import paho.mqtt.client as mqtt
import time
import json
client = mqtt.Client()
import serial
import os
import re
import time
#from magicblue import MagicBlue

interfaceList = os.popen("route | grep '^default' | grep -o '[^ ]*$'").readlines()
print interfaceList
#interfaceList = ""

file = os.path.exists("./wireless.py")
if file :
        from wireless import *


class Paasmer:
	host = ""
	feedSubscription = {}
	feedMonitorCB = {}
	#wifi = {}
	#philips_list = []
	#belkin_list = []
	#if wireLess:
	if 'wireLesss' in globals():
		global wireLess
		wireLess = wireLesss
	else:
		global wireLess
		wireLess = {}
	def connect(self):
		client.on_connect = self.on_connect
        	client.on_message = self.on_message
		client.connect(self.host, 1883, 60)
	def on_connect(self,client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		# Subscribing in on_connect() means that if we lose the connection and
		# reconnect then subscriptions will be renewed.
		client.subscribe("toSensor")
	def on_message(self,client, userdata, msg):
		subscribeMsg = (msg.payload)
		print(subscribeMsg)
		message = json.loads(subscribeMsg)
		if "feedControl" in message.keys():
			myFeed = message["feedControl"]["feedName"]
			myStatus = message["feedControl"]["value"]
			if myFeed in self.feedSubscription:
				self.feedSubscription[myFeed](myStatus)
				self.publish(myFeed,myStatus)
			if "philips" in wireLess.keys():
				philipsfeed = [bulbid for bulbid, feed in wireLess["philips"].items() if feed == myFeed]
				if philipsfeed:
        				print("The feed is" + str(philipsfeed[0]))
					print "The Status value is " + str(myStatus)
					self.Philips_write(philipsfeed[0], myStatus)
					philipsState = self. Philips_read(philipsfeed[0])
					print ("the Philips State is = " + str(philipsState))
					self.publish(myFeed,philipsState)
						
			if "belkin" in wireLess.keys():
                                belkinip = [belkinid for belkinid, feed in wireLess["belkin"].items() if feed == myFeed]
				if belkinip:
        				print(belkinip[0])
					if myStatus == "1" or myStatus == 1 :
						self.Belkin_Write(belkinip[0],"on")
						belkinState = self.Belkin_Read(belkinip[0])
						print ("The Belkin state is = " + str(belkinState))
						if belkinState == 1 :
							self.publish(myFeed,belkinState)
						else :
							print("Failed to control Belkin Wemo")
					elif myStatus == 0 :
						self.Belkin_Write(belkinip[0],"off")
						belkinState = self.Belkin_Read(belkinip[0])
                                                print ("The Belkin state is = " + str(belkinState))
						if belkinState == 0 :
							self.publish(myFeed,belkinState)
						else :
							print("Failed to control Belkin Wemo")

			if "BLE" in wireLess.keys():
				bluefeed=[blueid for blueid, feed in wireLess["BLE"].items() if feed == myFeed]
				if bluefeed:
					print("BLUETOOTH MAC-ID:")
					print(bluefeed[0])
					self.WriteBlue(bluefeed[0],myStatus)
					self.publish(myFeed,myStatus)
			else:
				print("not in feeds")

	def loop_start(self):
		client.loop_start()
	def subscribe(self,feed,cb):
		if feed not in self.feedSubscription:
			self.feedSubscription[feed] = cb
			self.publish(feed,0)
	def publish(self,feedName,feedValue,analytics = "none",analyticsCondition = "10",minValue = 0,maxValue = 0,feedType = "none"):
			feedDetails = {}
			feedDetails["feedname"] = feedName
			feedDetails["feedvalue"] = str(feedValue)
			feedDetails["analytics"] = analytics
			feedDetails["analyticsCondition"] = analyticsCondition
			if feedType != "none" :
				feedDetails["minValue"] = minValue
				feedDetails["maxValue"] = maxValue
				feedDetails["feedType"] = feedType
			

			feedDetails["readings"] = "NULL"
			finalData = {}
			finalData["feeds"] = feedDetails
			message = json.dumps(finalData)
			print("Hi this is normal function")
			print message
			if analytics == "none":
				client.publish("toAWS",message)

			else:
				client.publish("fromSensor",message)
	def publish_Rule(self,feedName,feedValue):
			feedDetails = {}
			feedDetails["feedname"] = feedName
			feedDetails["feedvalue"] = str(feedValue)
			feedDetails["readings"] = "NULL"
			finalData = {}
			finalData["feeds"] = feedDetails
			message = json.dumps(finalData)
			print("Hi this is rules function")
			print message
			client.publish("toRules",message)

	def ML_config(self,feedName,modelName):
		mlData = {}
		mlData["feedname"] = feedName
		mlData["name"] = modelName
		mlData["action"] = "config"
		message = json.dumps(mlData)
		client.publish("toMLnew",message)
	def ML_predict(self,feedName,modelName,data = {}):
		mlData = {}
                mlData["feedname"] = feedName
                mlData["name"] = modelName
                mlData["action"] = "predict"
		mldata = {}
		for i in data.keys():
			mlValue = []
			mlValue.append(data[i])
			mldata[i] = mlValue
		mlData["data"] = mldata
                message = json.dumps(mlData)
                client.publish("toMLnew",message)

# ................For Belkin ................
	BelkinIP = []
	BelkinCount = 0

	def getBelkinIP(self):
		global BelkinCount
		find = 0
		ip_new = []
		grep = "Location"
		if interfaceList :
			for interface in interfaceList :
				command = "gssdp-discover -t urn:Belkin:device:1 -n 3 -i " + interface.strip() + " | grep " + grep
				data = os.popen(command).readlines()
				if data:
					i=0
					ip= re.sub('[^0-9]','', data[0])
					while i < 12:
						ip_new.append(ip[i])
						i = i + 1
						if i % 3 == 0:
							if i <12:
								ip_new.append('.')
					Belkin_ip = ''.join(ip_new)
					print "Belkin ip = " + Belkin_ip
					if "belkin" not in wireLess.keys():
						print("bekin is not there and adding")
						wireLess["belkin"] = {}
					if Belkin_ip not in wireLess["belkin"].keys():
						print("belkin ip" + Belkin_ip + "not there and adding")
						belkinName = "Belkin" + str(len(wireLess["belkin"]) + 1)
						wireLess["belkin"][Belkin_ip] = belkinName
						self.publish(belkinName,0,feedType = "Button") 
						
					print(wireLess)
					file = os.path.exists("./wireless.py")
					if file :
						os.system ("rm wireless.py")
		                        f = open("wireless.py","a+")
                		        f.write ("wireLesss = " + str(wireLess))
		                        f.close
					return Belkin_ip
				else:
					print(wireLess)
					file = os.path.exists("./wireless.py")
					if file :
		                        	os.system ("rm wireless.py")
                		        f = open("wireless.py","a+")
		                        f.write ("wireLesss = " + str(wireLess))
		                        f.close
					return 0
	
	def Belkin_Write(self,belkinIP,message):
		command = "wemo -h " + belkinIP + " -a " + message
		print "Belkin " + message
		os.system(command)
	
	def Belkin_Read(self,belkinIP) :
		grep = "Location"
		if interfaceList :
			for interface in interfaceList :
				command = "gssdp-discover -t urn:Belkin:device:1 -n 3 -i " + interface.strip() + " | grep " + grep
				data = os.popen(command).readlines()
				if data :
					command = "wemo -h " + belkinIP + " -a GETSTATE"
					belkindata = os.popen(command).readlines()
					if "8" in belkindata[0] :
						return 1
					else :
						return 0
				else :
					print "Belkin Not connected"
		else:
			print "network intrface is not there"
#..................end of Belkin...........#

#..................Philips device..........#
	def getPhilipsIP(self,interface) :
		ip_new = []
		grep = "Location"
		command = "gssdp-discover -t urn:schemas-upnp-org:device:basic:1 -n 3 -i " + interface.strip() + " | grep " + grep
		data = os.popen (command).readlines()
		if data :
			i = 0 
			ip = re.sub('[^0-9]','',data[0])
			while i < 12:
				ip_new.append(ip[i])
				i = i + 1
				if i % 3 == 0 :
					if i < 12 :
						ip_new.append('.')
			Philips_ip = ''.join(ip_new)
			print "Philips ip = " + Philips_ip
			return Philips_ip

	def Philips_config(self) :
		grep = "Location"
		data = ""
		if interfaceList:
			for interface in interfaceList :
				command = "gssdp-discover -t urn:schemas-upnp-org:device:basic:1 -n 3 -i " + interface.strip() + " | grep " + grep
				data = os.popen (command).readlines()
				if data :
					philips_ip = self.getPhilipsIP(interface.strip())
					if philips_ip :
						os.system("hue -H " + philips_ip + " register")
						return 1
				#else:
				#	print "The Philips Hue is OFF or not available in the network"
		print "The Philips Hue is OFF or not available in the network"
	
	def Philips_write(self,number,value) :
		grep = "Location"
		if interfaceList:
			for interface in interfaceList :
				command = "gssdp-discover -t urn:schemas-upnp-org:device:basic:1 -n 3 -i " + interface.strip() + " | grep " + grep
		                data = os.popen (command).readlines()
				if data :
					if value != 0 :
						print "The Brightness is " + str(value)
						incoming = "hue lights " + str(number) + " on"
						os.system(incoming)
						incoming = "hue lights " + str(number) + " =" + str(value) 
						os.system(incoming)
					else :
						incoming = "hue lights " + str(number) + " off" 
						os.system(incoming)
						
					print "Controlling philips"
					break
				else :
					print("Philips is not connected in " + interface)
		else:
			print "there is no network interface"

	def Philips_read(self,number) :
		grep = "Location"
		if interfaceList :
			for interface in interfaceList :
				command = "gssdp-discover -t urn:schemas-upnp-org:device:basic:1 -n 3 -i " + interface.strip() + " | grep " + grep
                		data = os.popen (command).readlines()
				if data :
					incoming = "hue lights " + str(number) 
					read = os.popen(incoming).readlines()
					if "on" in read[0] :
						print("Philips is ON")
						philipsVal = read[0][11]+read[0][12]+read[0][13]
						print ("The Philips value is " + philipsVal)
						return philipsVal
					else :
						print("Philips is OFF")
						return 0
				else :
					print("Philips is not connected in " + interface)

#.................End of Philips ................#

#................ WiFi Initialization.............#
	def wifi_setup(self) :
		#os.system("./wifiDiscover.sh")
		grep = "Location"
		command = "gssdp-discover -t urn:schemas-upnp-org:device:basic:1 -n 3 -i wlan0 | grep " + grep
		philips = os.popen(command).readlines()
		if philips :
			value = self.Philips_config()
			return value
		command = "gssdp-discover -t urn:Belkin:device:1 -n 3 -i wlan0 | grep " + grep
	
	def read_wifi(self) :
		for key,value in wireLesss.items() :
			if key == "philips" :
				data = value
				for key,value in data.items() :
					light = "hue -j lights" + str(key)
					data=os.popen(light).read()
					#reach=
					get_philips = self.Philips_read(key)
					self.publish(value,get_philips)
			if key == "belkin" :
				data = value
				for key,value in data.items() :
					get_belkin = self.Belkin_Read(key)
					self.publish(value,get_belkin)
	
	
	def DiscoverWifi(self) :
		status = self.Philips_config()
        	if status == 1:
                	bulbs = os.popen("hue lights").readlines()
                	print "Number of bulbs connected via HUE = " +  str(len(bulbs))
                	i = 0
                	for i in range(0,len (bulbs)):
				print("Discovered Philips bulbs in your network")
				if "philips" not in wireLess.keys():
					wireLess["philips"] = {}
				if bulbs[i][3] not in wireLess["philips"].keys():
					philipsbulbname = "philips" + str(bulbs[i][3])
					wireLess["philips"][bulbs[i][3]] = philipsbulbname
					
					self.publish(philipsbulbname,feedValue = 0,feedType = "Slider",minValue = 0,maxValue = 254) 

				
		self.getBelkinIP()	
		#self.read_wifi()
		#read_BLE()

	def create(self) :
		file = os.path.exists("./wireless.py")
		print file
		print self.philips_list
		print ("is it the file status")
		if file :
			os.system ("rm wireless.py")
			f = open("wireless.py","a+")
			f.write ("philips_bulbs = " + str(self.philips_list) + "\n")
			f.write ("Belkin = " + str(self.belkin_list) + "\n")
			f.write("Belkin_Ip = " + str(self.BelkinIP) + "\n")
			f.close
		else :
			f = open("wireless.py","a+")
                        f.write ("philips_bulbs = " + str(self.philips_list) + "\n")
                        f.write ("Belkin = " + str(self.belkin_list) + "\n")
			f.write("Belkin_Ip = " + str(self.BelkinIP) + "\n")

                        f.close
					
		
#...............End of WiFi..............#

#...............Zigbee ...............
	port = 0
	def Xbee_init(self,ser) :
		print ser
		self.port = ser
		if ser :
			ser.isOpen()
		else :
			print "Serial Port is not open or enabled"
	def Xbee_write(self,pinNum, state) :
		print ("the port is self.port ")
		print (self.port)
		xBee = "GPIO " + str(pinNum) + " " + state + "*"
		self.port.write(xBee)

	def Xbee_read(self,pinNum) :
		n = "Read pin " + str(pinNum) + "*"
		self.port.write(n)
		time.sleep(.5)
		incoming = self.port.read()
		return int(incoming)
#..................End of Zigbee.............#

#..................bluetooth........#
	BlueIP = []
	BlueStatus = []
	bulb = 0
	blue = 1
	def DiscoverBlue(self):
		global bulb
		find = 0
		data = os.popen("sudo sh PaasmerDiscoverBlue.sh LEDBlue").readlines()
		if data:
			for blue_ip in enumerate(data):
				print ("The Bluetooth Bulb MAC-ID is " + blue_ip[1].strip("\n"))
				print self.BlueIP
				if "BLE" not in wireLess.keys() :
					print("BLE bulb is not in the wireless able, so inserting")
					wireLess["BLE"] = {}
				if data[0].strip("\n") not in wireLess["BLE"].keys() :
					print("Blue IP " + str(data[0].strip("\n")) + " not in the dict so adding")
					blueName = "magicblue" + str(len(wireLess["BLE"]) + 1)
					wireLess["BLE"][data[0].strip("\n")] = blueName
					self.publish(blueName,0,feedType = "Slider",minValue = 0, maxValue = 10) 
					
					print (wireLess)
					file = os.path.exists("./wireless.py")
					if file :
						os.system("rm wireless.py")
					f = open("wireless.py", "a+")
					f.write("wireLesss = " + str(wireLess))
					f.close
				else :
					print ("No Data available")

	def ConnectBlue(self,mac):
		from magicblue import MagicBlue
		if mac:
			self.blue = MagicBlue(mac, 9)
			status = self.blue.connect()
			print("status="+str(status))
			return status
		else:
			return false

	def WriteBlue(self,mac,brightness):
		global blue
		try:
			print("mac:"+str(mac))
			status = self.ConnectBlue(mac)
                        if status:
                                if brightness > 0 :
					brightness = brightness * 0.1
                                        print ("BLE Bulb ON")
                                        self.blue.turn_on(brightness)
                                        self.blue.disconnect()
					print ("Disconnected")
                                else:
                                        print ("BLE Bulb OFF")
                                        self.blue.turn_off()
                                        time.sleep(1)
                                        self.blue.disconnect()
					print ("Disconnected")
                except Exception as e:
                        print("could not connect to MagicBlue"+str(mac))
                        pass
#..................End of Bluetooth...........#
	def InstallBLE(self):
		print ("Installing dependencies for Bluetooth")
        	os.system("sudo sh PaasmerBLEinstall.sh")
	def InstallWiFi(self):
		os.system("sudo ./wifiDiscover.sh")
	        print "Installing dependencies for Wifi"
	def Xbee_connect(self,serialport):
		ser =  serial.Serial(serialport, 9600) # Enter the Port to which the Co-ordinartor zigbee is connected to the device (eg - /dev/ttyUSB0)
        	self.Xbee_init(ser)
		

