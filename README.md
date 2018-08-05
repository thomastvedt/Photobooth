# Photobooth
A simple raspberry pi python photobooth made for my wedding.

Based on this project: https://github.com/contractorwolf/RaspberryPiPhotobooth 
- uses RaspberryPi camera, raspistill command
- hard coded resolution on the screen I used: 1280x1024

## Setup Raspberry Pi
- install RaspberryPi camera
- install Raspberrian on Raspberry Pi
- sudo apt-get update
- sudo apt-get upgrade
- sudo apt install apt-file
- sudo apt file update
- sudo apt install libsdl1.2-dev
- sudo apt-get install git
- sudo pip install pygame (1.9.4, maybe already installed?)
- sudo apt-get install libjpeg-dev
- sudo pip install Pillow
- setup ssh and git
- git clone git@github.com:thomastvedt/Photobooth.git


## Dev setup on windows 10:
- http://www.pygame.org/download.shtml
- http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe
- cd folder
- python main.py (need to swap out raspistill command..)
- Copy files to raspberry pi using https://winscp.net/eng/download.php

## Dev setup mac
- xcode-select --install
- install Homebrew
- brew install python@2
- 