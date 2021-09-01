
def proxyHandling():
    ip = []
    port = []
    username = []
    password = []

    with open('proxies.txt') as line:
        proxy = line.readlines()
        ip.append(proxy.split(':')[0])
        port.append(proxy.split(':')[1])
        username.append(proxy.split(':')[2])
        password.append(proxy.split(':')[3])

        print(ip)
        print(port)
        print(username)
        print(password)


proxyHandling()