import os
import sys

def proxyHandling():
    userInput = input('\n\nIf your would like to rotate proxies on px,\nOr run the program on a singular proxy,\nPlease enter the proxy/list in proxies.txt and restart.\nOtherwise, hit ENTER.')
    if userInput == '':

        ip = []
        port = []
        username = []
        password = []

        http = []
        https = []

        with open(os.path.join(sys.path[0],'proxies.txt'), 'r') as proxies:
            for line in proxies:
                ip.append(line.split(':')[0])
                port.append(line.split(':')[1])
                username.append(line.split(':')[2])
                if '\n' in line.split(':')[3]:
                    password.append(line.split(':')[3].replace('\n', ''))
                else:
                    password.append(line.split(':')[3])

        for i in range(len(ip)):
            http.append(f"'http://{username[i]}:{password[i]}@{ip[i]}:{port[i]}'")
            https.append(f"'http://{username[i]}:{password[i]}@{ip[i]}:{port[i]}'")

proxyHandling()