Setup:

- install socat (used by tbtail): `$ sudo apt-get install socat`

Might remove this dependency by writing a simple UDP receiver in python but it's okay for now.

Running:

    $ PYTHONUNBUFFERED=1 python main.py

The `PYTHONUNBUFFERED` bit is a workaround for a bug that I'm planning to fix.

Installing (on Raspberry Pi):

    $ make build
    $ sudo make install
