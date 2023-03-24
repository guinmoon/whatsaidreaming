#!/bin/sh

echo "swap is (if empty then disabled): "
echo `sudo swapon --show`
echo "free"
free -h
echo "\ndf -h"
df -h
echo "allocating swap:"
sudo fallocate -l 2G /swapfile
echo "\nswap file:"
ls -lh /swapfile
echo "enabling swap..."
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo "\n swap enabled:"
sudo swapon --show