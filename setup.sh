#!/bin/bash

echo "Installing webserver and other binaries"
sudo apt update -qq
sudo apt install -y git htop nginx ufw

# install php7.1
sudo apt-get install software-properties-common
sudo add-apt-repository -y ppa:ondrej/php
sudo apt-get update -qq
sudo apt install -y php7.1 php7.1-fpm php7.1-mysql

echo "Installing python and dependancies"
sudo apt install -y python3 python3-pip python3-tk
pip3 install --upgrade nltk numpy

echo "Configuring python nltk"
python3 -m nltk.downloader all

echo "Setting up project"
cd ~
git clone https://github.com/Cyberzoid1/Database_Systems_Project.git
cd Database_Systems_Project
git fetch --all --prune
git pull

echo "Downloading adminer"
wget "https://www.adminer.org/latest.php"
mv -v latest.php adminer.php


echo "Setting up firewall"
ufw default deny incomming
ufw default allow outgoing
ufw allow ssh
ufw allow http
ufw allow https
ufw allow mysql
ufw enable
ufw status

