if [ -d "firstrun" ] ; then
	firstrun=1
	echo "WiFi Libraries are already installed"
else
	echo "Installing dependencies for WiFi Device Support....Please wait untill the Packages are downloaded"
	sudo apt-get install -y libgssdp-1.0-3
	sudo apt-get install -y gupnp-tools
	sudo apt-get install -y node.js
	sudo apt-get install -y nodejs
	sudo apt-get install -y npm
	sudo npm install -g hue-cli@0.2.0
	sudo npm install -g belkin-wemo-command-line-tools
	sudo npm i -g npm
	sudo mkdir firstrun
	sudo chmod 777 firstrun
	echo "Wifi Libraries installed successfully"
fi
