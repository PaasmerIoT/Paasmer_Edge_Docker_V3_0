# Paasmer Edge 3.0 
**Paasmer Edge Docker 3.0** for SBC Running any Linux flavoured OS.

## Overview

The **Paasmer Edge 3.0 (Paasmer_Edge_Docker_V3_0)** for SBC running any Linux flavoured OS, is a collection of Docker containers that enables you to do Analytics on edge and connect to the Paasmer IoT Platform. The **Paasmer Edge Versoin 3.0** also consists of Paasmer Python library and Python SDK to connect to the Paasmer Gateway. Python Library now simplifies the Subscribing and publishing and is capable to handle various feed types in a single function call. It also has a Generic framework of **Machine Learning Docker** which allows the user to perform Machine Learning feature to predict the result with a trained set of the database.

The new **Edge Rules Engine** feature can empower customers to automate control functions on the Edge based on the precondition performed on various types data that includes sensor data, Edge Analytics output data and Machine Learning output data.
 

## Paasmer Edge Analytics 
**Paasmer Edge Analytics** is the key feature in Paasmer Edge which provides you to do analytics on the sensor data. Presently we are providing Filter, Aggregate, Average and Feed monitoring algorithms, where you can analyze your sensor data based on your Analytics condition. Edge Analytics configuration can be done using the easy to use Paasmer Cloud UI released along with the Edge Rules Engine

### Analytics and Features
* **Filter** - Can be used to Filter the sensor data based on Analytics conditions.
* **Aggregate** - Can be used to Find the Minimum, Maximum, Mean and Standard Deviation on the last n number of feed inputs. Where n is an integer given in the Analytics condition. 
* **Average** - Can be used to Find the Average of the last n number of feed inputs. Where n is an integer given in the Analytics condition.
* **Feed Monitoring** - Can be used to monitor the value changes in the feed by continuously monitoring the feeds. 


## Paasmer Machine Learning
**Paasmer Machine Learning** is another key feature in Paasmer-Docker which provides the user with a generic Machine Learning framework that allows the user to perform Machine Learning with his own dataset and train & test the Machine Learning module using few sets of commonly used Machine Learning algorithms. 

* The Machine Learning in Paasmer is of two steps. Cloud initialization and Edge configuration. Please Find below for **Cloud Initialization and Edge configuration**.

* Machine Learning configuration can also be done using the easy to use Paasmer Cloud UI released along with the Edge Rules Engine 

## Paasmer Edge Rules Engine
**Paasmer Edge Rules Engine** will empower customers to automate control functions on the Edge based on various conditions. Automation can be done based on the precondition performed on other data that includes the sensor data and the data from the enhanced version of Edge Analytics and Machine learning services 

## Paasmer Python Library
**Paasmer Library** is set of functions that can be used to connect, subscribe and publish to the Paasmer gateway easily and more efficiently in a single function call. It can also support Edge Analytics and Machine Learning on any feed while publishing. It has separate CallBack for each feed and thus making the connection simple. It can also support WiFi, Bluetooth and Zigbee Protocol support to control specific wireless devices.

## Pre Requisites
* Registration on the [PAASMER portal](http://developers.paasmer.co) is necessary to connect the devices to the **Paasmer IoT Platform**. 
* An SBC board with any Linux flavoured OS installed on it.

## Device Creation
The device creation can be done by two ways. Either from Web UI or from the Device side.
#### Web UI
* Click on `Docker Devices` tab in the menu and select ` Add Dockerdevice` option.
* Enter the desired device name and select license, then click `create`.
* When it asks for the device creation in the `Paasmer-3.0` script, select `no` and provide the device name which you have created in the Web UI. This will establish a connection between the physical device and the UI created device.
* License Activation- The License activation will be done automatically in the `Paasmer-3.0` script. 

#### Device Side
* On running the `Paasmer-3.0` script and successfully login with your Paasmer credentials, it will ask for creating a new device. Select `yes` and enter the desired device name and give a unique DeviceName for your device and that must be alphanumeric without any spaces[a-z A-Z 0-9].
* License Activation- The Licence Activation will be done automatically in the `Paasmer-3.0` script. 

**Note: From the device side you can create only Free Licensed Devices.**
# Installation
* Download the SDK or clone it using the command below.
```
$ git clone github.com/PaasmerIoT/Paasmer_Edge_Docker_V3_0.git
$ cd Paasmer_Edge_Docker_V3_0
```

* Run the file using the command.
```
$ sudo ./Paasmer-3.0
```
This script will install the required packages, Paasmer containers(Paasmer Features) and also build the dockers. 

* Enter your developers.paasmer.co login credentials to login to Paasmer platform

* After successful log-in, It will ask for creating a new device. 

* Wohooo! That's all. You device is now expected to be connected with Paasmer platform and you can manage the Device from Paasmer WEBUI

#### Machine Learning Cloud Initialization
* After successfully activating the license, You can find `Machine Learning` tab on the Device page in Web UI. 

* Click on `Create` button, Enter a unique Model name for your model and that must be alphanumeric without any spaces[a-z A-Z 0-9].
* Then Upload the sample dataset (any .csv format file) and click on `upload` button. 
* After the file is uploaded successfully, other option will be displayed. 
* Please select the Algorithm, X-train and Y-train and click `create`. 
* Once the model is created successfully click on the model, it will open another window where you see the selected details.
* Now click on the `Train` button, this will train the model based on the selected algorithm and it may take some time. Once it is trained successfully you can see a message `The Model trained Successfully` in the text box below the Train and Test buttons.
* Now you can click on `Test` button and enter sample values and click `Submit` button. You can see the Predicted output in the text box below the buttons.
* If you feel that the predicted value is accurate you can go ahead and proceed with the device side configuration. Else you can edit the algorithm in the model from the edit option given in the model page.

**Note - Few algorithms supports only single Y-train values. X-train and Y-train fields cannot be same.**

#### Machine Learning Edge Configuration
* Use the Python library at `PaasmerLibrary` directory for Machine Learning prediction and monitoring.

The syntax for calling Machine Learning is,
```
test.ML_config(feedName = "mlfeedname",modelName = "modulename")
```

**Note - A sample code is provided in `PaasmerLibrary` directory**

#### Rule Creation
* Log in to [Paasmer platform](developers.paasmer.co) and select a device in the docker devices tab. Click on `Edge Rules tab` and select Create, enter the required Rule name and Click `Submit`. Decide on the details of the rule to be created with what feeds, what services, what conditions, what needs to be achieved and how can be achieved. drag and drop feeds, actuators and services according to the plan follow the use cases to create a rule.

##### Use Cases for Edge Rules
* Creating Rule With Edge Analytics and Machine Learning
* Creating Rule With Only Edge Analytics
* Creating Rule With Only Machine Learning
* Creating Rule With only Sensors and Actuators

**A brief explanation on how to create rule with various modes is explained [here](https://github.com/PaasmerIoT/Paasmer_Edge_Docker_V3_0/blob/master/How%20to%20use%20Paasmer%20Edge%20Rules%20Engine.pdf) with image representation under the appropriate topics**

#### Rule Deployment
* After successfully creating a rule, Check the `Features` tab if the **Edge Rules** feature is Running. If the Status is `running`, get back to the `Edge Rules` page and click `Deploy` button. 
* Once it is successfully deployed,You will receive a success message. Now we have to configure the Edge.

#### Edge Configuration
* On successful completetion of above, we have to configure the Edge to accomplish Edge rules function. 
* The steps are similar to the Paasmer Library, except the `publish` function. 
* The publish function is given below,
```
    test.publish_Rule("feedname",feedValue = 9)
```
* Wohooo! That's it. Now follow the steps in the Readme file to run the `PaasmerLibrary`.

## Getting started with Paasmer Python Library
Here is a very simple example that connects to the Paasmer Gateway, subscribes and Publishes to Paasmer platform enabling the user to access and read the feeds.

### Importing Paasmer Library
Open `paasmerLibrary` directory and start building the script.

```
from Paasmer import *
```
### Connecting to the Paasmer Edge docker device
```
test = Paasmer()
test.host = "localhost"   #IP address of the Paasmer Edge docker device.
test.connect()
```


### Subscribing 

```
#Callback functions for subscribed feeds
def feed1_CB(name):
    print("This is in feed1")
    print(name)

#subscribing to the feeds with callback functions
test.subscribe("feed1",feed1_CB)

```
The Subscribe functions need the following as parameters,
```
subscribe(feedname,callback function name)
```
- Feedname
- Call back Function name 

### Protocol Usage 
#### Zigbee 
Initializing Zigbee port
```
test.Xbee_connect("/dev/ttyUSB0") # Enter the Port to which the Co-ordinartor zigbee is connected to the device (eg - /dev/ttyUSB0)
```
Controlling via Zigbee
```
test.Xbee_write(8,"off") 
```

Xbee_write functions needs the following as parameters,
```
Xbee_write(pin,state) 
```
- pin : Pin to conrol in Arduino
- state : on (or) off 

Reading via Zigbee
```
test.Xbee_read(5)
```
Xbee_read functions needs the following as parameters,
```
Xbee_read(pin) 
```
- pin : Pin to read in Arduino

#### WiFi 
Installing Wifi Protocol dependencies 
```
test.InstallWiFi()
```
Discovering WiFi devices
```
test.DiscoverWifi()
```

#### Bluetooth
Installing  Bluetooth Protocol dependencies 
```
test.InstallBLE()
```
Discovering Bluetooth devices
```
test.DiscoverBlue()
```

### Loop start
```
test.loop_start()
```

### Publishing the feed details 
The Publish functions need the following as parameters,
```
    test.publish("feed2",feedValue = 9,feedType = "sensor")
```
- Feedname
- Feedvalue
- Feedtype (The Feedtype is to be sensor or actuator)

You can use the Analytics in the following way,
- Filter - provide the analytics condition like "function(x) x < 5.0"
- Aggregate - provide the number of values you want to do aggregate
- FeedMonitoring
- Average - provide the number of values you want to do average

You can control following devices for wifi and BLE protocol support with autodiscover functionality.

With WiFi
* Philips Hue
* Belkin Wemo
        
With BLE
* Magicblue bulbs

The syntax for Publishing Analytics are,

```
#publishing the feed details with filter analytics 
    test.publish("feed4",feedValue = 5,analytics = "filter",analyticsCondition="function(x) x > 3.0")

#publishing the feed details with aggregate analytics
    test.publish("feed6",feedValue = 22,analytics = "aggregate",analyticsCondition = "10")

#publishing the feed details with average analytics
    test.publish("feed8",feedValue = 28,analytics = "average",analyticsCondition = "10")

#publishing the feed details with feedMonitoring
    test.publish("feed7",feedValue = 22,analytics = "feedMonitoring")
```

**Note - A sample code is provided in `paasmerLibrary` directory**

## Support

The support forum is hosted on the GitHub, issues can be identified by users and the Team from Paasmer would be taking up requests and resolving them. You could also send a mail to support@paasmer.co with the issue details for a quick resolution.

## Note

* The Paasmer Edge utilizes the features provided by Docker engine.




