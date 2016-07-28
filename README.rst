omechat
=======

Purpose
-------

I was interested in becoming familiar with Flask-SocketIO.  The quintessential
demo for socket.io is a chat app.  However, I decided to create something less
typical (although certainly not completely original) and significantly less
useful.  As such, this is a chat app that exclusively uses emojis.

Installation
------------

*I plan to add a DockerFile soon*

**Note:** Testing so far has only been done with **Python 3.5.1**

From the root of the cloned repo::

  pip install -r ./requirements.txt

Usage
-----

To run the server, from the root of the cloned repo::

  python -m omechat eventlet

Then, browse to `<http://0.0.0.0:5000>`_.  Open a second tab at the same
location, and you can have a conversation with yourself.
