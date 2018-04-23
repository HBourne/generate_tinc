## README

Create tinc configs locally through http.

### Locally
Run generate.sh directly with params at the top figured out and comment out the git part below.

------------------------------------------

### HTTP
#### Step 1
Run httpgenerator.py on the server.
> python httpgenerator.py [port]
> e.g. python httpgenerator.py 8888

#### Step 2
Modify params in sendrequest.py, including ip, nodename, nodeip, connectto, vpnip, etc.. Remember to preserve that '3000' after ip, which is used to judge whether the request is legal.

Run sendrequest.py.
> python sendrequest.py
