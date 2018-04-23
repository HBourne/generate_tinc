import requests

GETADDRESS = "http://192.168.111.218:3000/sendlist/"

params = {
	'NODENAME' : ['BJCenter'],
	'CONNECTTO' : [],
	'VPNIP' : [],
	'NODEIP' : ['10.0.0.2']
}

NODENAME = params['NODENAME'][0]
request = requests.get(GETADDRESS+NODENAME+'.tar',params=params,timeout=10)

with open (NODENAME+'.tar','wb') as file:
	for content in request.iter_content():
		file.write(content)
