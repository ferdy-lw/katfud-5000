#!/bin/sh

echo -n "checking" > hostname.txt
curl -s 'http://192.168.1.1/htmlV/index.asp' | grep  DHCPState_DHCPIPAddress  | sed -E -n 's/.*\"(.*)".*/\1/p' > hostname.txt
