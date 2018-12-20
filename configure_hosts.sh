#!/bin/bash

echo "*** Removing directories"
if [ -e /tmp/h1 ] ; then
	rm -r /tmp/h1
fi
if [ -e /tmp/h2 ] ; then
	rm -r /tmp/h2
fi
if [ -e /tmp/h3 ] ; then
	rm -r /tmp/h3
fi

echo ""
echo "*** Creating an copyng new directories"
mkdir /tmp/h1
cp -r /etc /tmp/h1

mkdir /tmp/h2
mkdir /tmp/h2/var
mkdir /tmp/h2/var/www
cp -r pages/* /tmp/h2/var/www

mkdir /tmp/h3
mkdir /tmp/h3/var
mkdir /tmp/h3/var/www
cp -r pages/* /tmp/h3/var/www
cp -r /etc /tmp/h3
