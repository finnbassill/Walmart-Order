import os
import sys
import zipfile
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


#Handles list of proxies
def proxyHandling():

    ip = []
    port = []
    username = []
    password = []

    with open(os.path.join(sys.path[0],'proxies.txt'), 'r') as proxies:
        for line in proxies:
            ip.append(line.split(':')[0])
            port.append(line.split(':')[1])
            username.append(line.split(':')[2])
            if '\n' in line.split(':')[3]:
                password.append(line.split(':')[3].replace('\n', ''))
            else:
                password.append(line.split(':')[3])

    return ip, port, username, password

<<<<<<< HEAD
#Proxy Auth, reference: https://botproxy.net/docs/how-to/setting-chromedriver-proxy-auth-with-selenium-using-python/
=======
#Proxy Auth, refrence: https://botproxy.net/docs/how-to/setting-chromedriver-proxy-auth-with-selenium-using-python/
>>>>>>> eae94e90624d1a715520b71ff10918dcabaaed34
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

    pluginfile = 'proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return pluginfile

<<<<<<< HEAD
#Rotate proxy and user agent on px fail
used_ip = []
def rotate():
    ph = proxyHandling()
    ip = ph[0]
    port = ph[1]
    user = ph[2]
    pw = ph[3]

    #Rewriting pluginfile to rotate proxy
    index = 0
    used = True
    while used:
        index = random.randint(0, len(ip))
        if ip[index] not in used_ip:
            used_ip.append(ip[index])
            used = False
    
    plugin = proxyAuth(ip[index], port[index], user[index], pw[index])

    #Generating random user-agent
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.MAC.value, OperatingSystem.MAC_OS_X.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()

    return plugin, user_agent, ip[index]
            
=======
def rotateProxy(num):
    pass
>>>>>>> eae94e90624d1a715520b71ff10918dcabaaed34
