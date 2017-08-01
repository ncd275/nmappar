# Nmappar
----------
A parser for nmap. This script provides multiple functions for parsing through nmap output that's in a grepable format. Example: nmap-results.gnmap - This output can be generated using the '-oG filename.gnmap' option on your nmap scan



# Usage
--------
Nmappar takes a file as an argument with the options of --options and --function.
```js
python nmappar.py nmap-results.gnmap --options hps --function search-services=http,ftp,Cisco
```



##Functions
You can use the --function option and then specify which one you would like to use. The functions are listed below:


####search-services
------------------
Example:
```js
python nmappar.py nmap-results.gnmap --function search-services=http
```

Description:
This funtion accepts keywords that will be used to search through all the services and return any matches. To specify multiple keywords, please separate by commas without any spaces.



####search-ports
------------------
Example:
```js
python nmappar.py nmap-results.gnmap --function search-ports=23
```

Description:
This funtion accepts port numbers that will be used to search through all the ports and return any matches. To specify multiple ports, please separate by commas without any spaces.



####search-hosts
------------------
Example:
```js
python nmappar.py nmap-results.gnmap --function search-hosts=10.8.8.15

python nmappar.py nmap-results.gnmap --function search-hosts=10.8.*.221

python nmappar.py nmap-results.gnmap --function search-hosts=10.*8.8.2*
```

Description:
This funtion will search for hosts. Multiple IPs can be given separated by commas. Note, in the example, wildcards are supported. The function will match the IP address and by default will return the IP, port and service. If you would like to change what is returned, you can use --options.



####live-hosts
------------------
Example:
```js
python nmappar.py nmap-results.gnmap --function live-hosts
```

Description:
This funtion does not accept any parameters and simply returns all hosts with the state of 'Up'. The example command above would return the IP address, port number and associated service.



####uniq-services
------------------
Example:
```js
python nmappar.py nmap-results.gnmap --function uniq-services
```

Description:
This funtion will return all the unique services in the scan output. Any '--options' applied to this function will not take effect because it will only return the port number and service name. Since it will only return one instance of a service name and port, does not make sense to return a single IP in the case there are multiple.



####dead-hosts
------------------
Example:
```js
python nmappar.py nmap-results.gnmap --function dead-hosts
```

Description:
This will just return any hosts with a status of 'Down'. Why would you need this? I don't know, I just put it in there.



##Options
-----------

You can use --options to specify what you would like to output. By default, if no options are specified the functions will return all three.
h=host column
p=port column
s=service column

The order of these should not matter.

Example:

```js
python nmappar.py nmap-results.gnmap --options hp --function live-hosts
```
Description:
This would return all live hosts and output only the IP address and the port numbers



# Dependencies
--------------
- Tested with Python 2.7.x
- Click (click should allow this to work with Python 3 as well, just haven't test)
```js
pip install click
```



# Future
---------
I might take out the dependency on Click and use argparse or optparse instead, Not sure. Looking to add a 'compare' function to compare two different nmap files. For example: A scan is ran on the network and two weeks later towards the end of the pentest, the same scan is ran again and the compare function would detect any changes.

Let me know how you use Nmap results and if you would like to see anything added.