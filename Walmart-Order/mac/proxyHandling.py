import os
import sys
import zipfile

#Handles list of proxies
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
            http.append(f'http://{username[i]}:{password[i]}@{ip[i]}:{port[i]}')
            https.append(f'http://{username[i]}:{password[i]}@{ip[i]}:{port[i]}')

    return http, https, ip, port, username, password

def proxyAuth(host, port, user, pw):
    PROXY_HOST = host
    PROXY_PORT = port
    PROXY_USER = user
    PROXY_PASS = pw

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)





def rotateProxy(num):
    pass
