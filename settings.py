import smtplib
# Forwarding Constants
ALL, UNKNOWN_ADDRESS, NONE = range(3)

server = {
    'address': ('localhost', 25),
    'forward': {
        'on': NONE,
        'address': ('localhost', 25),
    },
}

services = {
    'example@localhost': {
        'url': 'http://localhost/api/',
        'response': {
            'address': ('localhost', 587),
            'username': '',
            'password': '',
            'from_email': 'testing@localhost',
        }
    },
}


# Set up the mail servers. Probably needs to be moved out of settings
for _k in services.keys():
    _rs = services[_k]['response']
    _server = smtplib.SMTP(*_rs['address'])
    _server.login(_rs['username'], _rs['password'])
    services[_k]['resp'] = _server