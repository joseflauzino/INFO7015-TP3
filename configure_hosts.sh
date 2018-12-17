#!/bin/bash

echo "*** Removing directories"
rm -r /tmp/h1
rm -r /tmp/h2
rm -r /tmp/h3

echo ""
echo "*** Creating an copyng new directories"
mkdir /tmp/h1
cp -r /etc /tmp/h1

mkdir /tmp/h2
mkdir /tmp/h2/var
mkdir /tmp/h2/var/www
cp -r pages/all/* /tmp/h2/var/www

mkdir /tmp/h3
mkdir /tmp/h3/var
mkdir /tmp/h3/var/www
cp -r pages/all/* /tmp/h3/var/www
cp -r /etc /tmp/h3
