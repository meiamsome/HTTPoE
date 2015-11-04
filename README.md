# HTTPoE

This module provides a mail server that, when emailed a suitable request will respond with the HTTP request specified in the settings file. 

## Usage

In the settings file, place your services into the services dictionary:

```python
services = {
    '<Email to listen on>': {
        'url': '<URL to query>',
        'response': {
            'address': ('<SMTP Host to use for replies>', <SMTP PORT>),
            'username': '<SMTP Username>',
            'password': '<SMTP Password>',
            'from_email': '<Email to respond from>',
        }
    },
}
```

There can be any number of services in the dictionary.

Then launch the httpoe daemon:
```
$ ./httpoe.py
```

The server should then respond to an email sent to it.