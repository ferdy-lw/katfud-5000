KatFud - 5000
=============

Automated kat feeder using RPi to control motor. 

## Fudware
The current feeder hardware is an old "catmate" circular pie feeder that used to be controled via an gear clock with manually configured "triggers" to switch to the next pie. The gear clock connection and swing arm have been removed and the pie top dish is directly connected to a 12v motor, which is driven at 5v to slow the turn speed down. The pie top plate side walls have been cut with small gaps that a simple snap-action roller switch uses to turn the motor off when the next pie is fully open. 

## Driver Board
A small board with a 5v regulator, and relay (with npn switch) is used to connect the RPi with the motor and pie switch. The board also has an led indicating the 5v regulator is powered, and an led the RPi blinks every second to indicate the RPi has booted and is running the KatFud software. The motor is driven from the 5v regulator, power from the RPi is used to drive the timing led and the npn relay trigger.

### Pins

RELAY_GPIO = 17
LED_GPIO = 22
BUTTON_GPIO = 27

## RPi

The RPi is configured on boot to run ntpd, and start the KatFud app. The KatFud app is a [Pyramid](http://docs.pylonsproject.org/projects/pyramid/en/1.0-branch/index.html) web app using [RPIO](http://pythonhosted.org/RPIO/) for the gpio and Coffee/Backbone/[Foundation](http://foundation.zurb.com/) for the UI.

To run the app on the RPi: ```pserve production.ini```. This starts pyramid using it's inbuilt waitress server on port 80. It also "scrapes" the ip address of the external modem so that the KatFud app can be access from the internet (if the firewall is configured to port forward).

The app can be also run not on RPi for testing purposes, but this disables any of the RPIO code so no GPIO is performed, but you can test the ui and timing logic: ```pserve development.ini --reload```, which along with running brunch in watch mode: ```brunch w``` lets you live reload both the python code and javascript.

Python is run in a virtual env, with [venvwrappers](http://virtualenvwrapper.readthedocs.org/en/latest/) for convenience.

## Install

KatFud is in two parts, KatFud is the main python webapp and katfud-ui is the UI side. 

### KatFud

The web app is a simply Python Pyramid app and runs just using the paster engine.

- Install virtualenv and virtualenv wrappers
- ```mkvirtualenv katfud```
- ```workon katfud```
- ```$ cd KatFud```
- ```python setup.py```

### katfud-ui

The UI is built with [brunch](http://brunch.io/).

- Install [node.js](http://nodejs.org)
- Install Brunch: `sudo npm install -g brunch`
- Install SASS and Compass: `gem install compass`
- Install Foundation CSS: `gem install zurb-foundation`
- ```$ cd katfud-ui```
- Run `npm install` to install the node dependencies listed in `package.json`.

## Building

To build the UI, compile the coffee and assemble the code into the KatFud pyramid "static" directory: ```brunch b```

After building the javascript assets into the pyramid static directory, package the webapp: ```python setup.py sdist```. Copy the dist ```KatFud-5000.tar.gz``` over to the RPi, activate the virtual env, and run setup.py.
