import os
import csv
import re
import pickle
#import json
#import requests
import paramiko
import getpass
import time

BIGIP = []

class F5_performance_issues():


        def __init__(self,server_ip,user,passwd,virtual_server,VIP,incident):
                self.server_ip = input("Enter the IP of the device: " )
                self.user = input("What is the username? " )
                self.passwd = getpass.getpass("Enter password: ")
                self.virtual_server = input("What is the virtual server name? " )
                self.VIP = input("What is the VIP address? " )
                self.incident = input("What is the incident number? " )

                BIGIP.append(self.server_ip)
        def connect(self):
                for f5 in BIGIP:
                        self.ssh = paramiko.SSHClient()
                        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        self.ssh.connect(f5, username=self.user, password=self.passwd, allow_agent=False,look_for_keys=False)
                        return self.ssh

        def get_shell(self):
                print('Connecting to F5')
                print(self.server_ip)
                self.shell = self.ssh.invoke_shell()
                return self.shell

        def send_command(self,timeout=5):
                #self.shell.send('terminal length 0\n')
                self.shell.send('ls -latr /shared/core\n')
                time.sleep(0.5)
                self.shell.send('cat /var/log/kern.log | grep "failure"\n')
                time.sleep(0.5)
                self.shell.send('tmctl -d blade tmm/if_shaper\n')
                time.sleep(0.5)
                self.shell.send('tmsh show /net interface all-properties\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys log ltm | grep -i "bandwidth utilization"\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys traffic\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i Dropped\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i Dropped\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i Dropped\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i Errors\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i Errors\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i Errors\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i "Maximum Connections"\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i "Maximum Connections"\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i "Maximum Connections"\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i "Virtual Server Limit"\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i "Virtual Server Limit"\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys tmm-traffic | grep -i "Virtual Server Limit"\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys ip-stat | grep Dropped\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys ip-stat | grep Dropped\n')
                time.sleep(0.5)
                self.shell.send('tmsh show sys ip-stat | grep Dropped\n')
                time.sleep(0.5)
                self.shell.send(f"tmsh show sys connection cs-server-addr {self.VIP}\n")
                time.sleep(0.5)
                self.shell.send(f"tmsh show ltm persistence persist-records virtual {self.virtual_server}\n")
                time.sleep(0.5)
                self.shell.send(f"tmsh show ltm virtual {self.virtual_server} detail\n")
                time.sleep(0.5)
                self.shell.send(f"tmsh list ltm virtual {self.virtual_server}\n")
                time.sleep(timeout)

        def show(self,n=100000):
                output = self.shell.recv(99999)
                output = output.decode('utf-8')
                with open("self.incident.txt", "a") as f:
                        f.write(output)


        def close_server(self):
                if self.ssh.get_transport().is_active():
                        print("Closing connection")
                        self.ssh.close()

k = F5_performance_issues("server_ip","user","passwd","virtual_server","VIP","incident")
k.connect()
k.get_shell()
k.send_command()
k.show()
k.close_server()
