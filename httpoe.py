#!/usr/bin/env python
import asyncore
from email.mime.text import MIMEText
import smtpd
import urllib2

import settings

class HTTPOE(smtpd.PureProxy):
    def process_message(self, peer, mailfrom, rcpttos, data):
        for x in rcpttos:
            if x in settings.services:
                self.dispatch(settings.services[x], peer,
                              mailfrom, rcpttos, data)
            if settings.server['forward']['on'] == settings.ALL:
                super(smtpd.PureProxy, self).process_message(peer, mailfrom, rcpttos, data)
    def dispatch(self, service, peer, mailfrom, rcpttos, data):
        headers, body = data.split('\n\n', 1)
        headers = [header.split(': ', 1) for header in headers.split('\n')]
        headers = dict([(k.lower(), v) for k, v in headers])
        subject = headers['subject']
        request_type = 'GET'
        if ' ' in subject:
            request_type, subject = subject.split(' ', 1)
        request = urllib2.urlopen(service['url'] + subject, body if request_type == 'POST' else None)
        message = request.read()
        mes = MIMEText(message)
        mes['Subject'] = subject
        mes['From'] = service['response']['from_email']
        mes['To'] = mailfrom
        service['resp'].sendmail(mes['From'], [mailfrom], mes.as_string())
        

def run_server():
    if settings.server['forward']['on'] == settings.UNKNOWN_ADDRESS:
        raise NotImplementedError('Unknown address functionality is reserved' 
            ' but unimplemented')
    server = HTTPOE(settings.server['address'],
                    settings.server['forward']['address'])
    asyncore.loop()

if __name__ == '__main__':
    run_server()
