Twitter Notify
==============

This application provides a simple command line interface to the Twitter API
to print out replies and DMs as they come in every 90 seconds.

Why bother writing this application? Well, in its current state, its not very
useful. However, I rely on Twitter for networking, and find it distracting.
Instead of wandering to Twitter every 10 minutes hoping for a reply to a
*previous* message I sent during downtime, I figured I might as well have a
user daemon do it for me asynchronously.

Right now, all the application does is print to a console using various colors
to disambiguate each time new replies/DMs come in. In the future, I will
add a callback mechanism so one can be notified in a less intrusive manner,
such as lighting an LED on a Raspberry Pi.

Installation
------------

| To install Twitter Notify, simply run setup.py:
| ``python3 setup.py install`` or ``python3 setup.py develop``

| To invoke a Twitter Notify, use the following command:
| ``python3 -m tnotify``

No input arguments for now! A file named ``auth.json`` must exist in the
current directory that is accepted by the following schema:

::

    {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "type": "object",
      "properties": {
        "consumer_token": {
          "type": "string"
        },
        "consumer_secret": {
          "type": "string"
        },
        "auth_token": {
          "type": "string"
        },
        "auth_secret": {
          "type": "string"
        }
      },
      "required": [
        "consumer_token",
        "consumer_secret"
      ]
    }

This file provides OAuth credentials to talk to the Twitter API. If ``auth_token``
and ``auth_secret`` are not provided, they will be created and written to ``auth.json``
when the application runs. A web browser window will be spawned and will display
a PIN for verification. AFAIK, Twitter does not invalidate OAuth tokens, so
on subsequent runs of this program, the previously-generated token and secret
will be used.
