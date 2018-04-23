#coding=utf-8
import subprocess as sp
import os
import time
import SimpleHTTPServer
import SocketServer
import BaseHTTPServer  
import urllib
import shutil
import commands
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    server_version = "SimpleHTTP/TINC"

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def send_head(self):
        """Send a HEAD."""
        query = urllib.splitquery(self.path)
        # Read configs from the request
        if self.path.split("?")[0]!="/tincconf":
            self.send_error(404, "Request not legal. Connection refused.")
            return None
        else:
            CONNECTTO=[]
            VPNIP=[]
            NODENAME=None
            NODEIP=None
            for i in query[1].split("&"):
                param=i.split("=")
                if param[0]=="CONNECTTO":
                    CONNECTTO.append(param[1])
                elif param[0]=="NODENAME":
                    NODENAME=param[1]
                elif param[0]=="VPNIP":
                    VPNIP.append(param[1])
                elif param[0]=="NODEIP":
                    NODEIP=param[1]

            # Check if all necessary parameters are provided
            if not NODENAME or not NODEIP:
                self.send_error(500, "Loss of input parameters. Connection refused.")
                return None
            # generatetar(NODENAME,CONNECTTO,VPNIP,NODEIP)
            os.environ['NODENAME']=NODENAME
            os.environ['CONNECTTO']=','.join(CONNECTTO)
            os.environ['NODEIP']=NODEIP
            os.environ['VPNIP']=','.join(VPNIP)
            status=sp.call(['bash','generate.sh'])
            if status != 0:
                self.send_error(status, "Error occurred while generating.")
                return None
            try:
                f = open('sendlist/'+NODENAME+'.tar', 'rb')
            except IOError:
                self.send_error(404, "File not found")
                return None
            self.send_response(200)
            self.end_headers()
            return f

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

def start_server(HandlerClass = SimpleHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


# def generatetar(NODENAME,CONNECTTO,VPNIP,NODEIP):

#     print NODENAME,NODEIP,VPNIP,CONNECTTO

#     # Generate the path
#     sp.call(['mkdir','-p','tx/hosts'])
#     sp.call(['mkdir','sendlist'])

#     # Generate tinc.conf
#     file = open('tx/tinc.conf','w')
#     file.write('Name = '+NODENAME+'\nAddressFamily = ipv4\nMode = Switch\n')
#     for i in CONNECTTO:
#         file.write('ConnectTo = '+i+'\n')
#     file.close()

#     # Generate tinc-up
#     file = open('tx/tinc-up','w')
#     file.write('#!/bin/sh\nifconfig $INTERFACE '+NODEIP+' netmask 255.255.255.0\n')
#     file.close()

#     # Generate tinc-down
#     file = open('tx/tinc-down','w')
#     file.write('#!/bin/sh\nifconfig $INTERFACE down\n')
#     file.close()

#     # Chmod for tinc-up and tinc-down
#     sp.call(['chmod','755','tx/tinc-up','tx/tinc-down'])

#     # Generate client information in hosts 
#     file = open('tx/hosts/'+NODENAME,'w')
#     for i in VPNIP:
#         file.write("Address = "+i+"\n")
#     file.close()

#     # Generate server information in hosts
#     for i in CONNECTTO:
#             sp.call(['cp','repo/'+i+'/'+i,'tx/hosts/'])

#     # Check if config already exists
#     if os.path.exists('repo/'+NODENAME):
#         print "It seems that it exists"
#         sp.call(['cp','repo/'+NODENAME+'/'+NODENAME,'tx/hosts/'])
#         sp.call(['cp','repo/'+NODENAME+'/rsa_key.priv','tx/'])
#     else:
#         # Generate tinc key for client
#         genkey=sp.Popen(['tincd','-c','./tx','-n','tx','-K4096'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE)
#         genkey.stdin.write('\n')
#         genkey.stdin.write('\n')
#         genkey.stdin.close()
#         time.sleep(5)
#         sp.call(['mkdir','-p','repo/'+NODENAME])
#         sp.call(['cp','./tx/rsa_key.priv','repo/'+NODENAME+'/'])
#         sp.call(['cp','./tx/hosts/'+NODENAME,'repo/'+NODENAME])

#     # Zip the files and copy to the sendlist
#     sp.call(['tar','czf',"sendlist/"+NODENAME+".tar",'tx'])

#     # Delete the content
#     sp.call(['rm','-r','tx'])

#     # Complete
#     print "Tar is generated!"

if __name__ == '__main__':
    # PORT = 3000
    # Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    # TCPServer = SocketServer.TCPServer(("",PORT),Handler)
    # TCPServer.serve_forever()
    start_server()