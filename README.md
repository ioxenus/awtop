## awtop ##

A really simple cross-platform network/process monitor. `lsof -i` isn't that good :P

#### how to install? ####

It's tested on OS X with Python 2.7 and uses a third-party `psutil` module.
You can install it via either pip or easy_install:

    pip install psutil

#### how to use? ####

You can search for the nasty process that's connecting to some site just like that:

    $ python awtop.py -s "*github*"
     41398 | + Google Chrome
           | |-- ESTABLISHED     | ip1b-lb3-prd.iad.github.com:443
           | |-- ESTABLISHED     | ip1b-lb3-prd.iad.github.com:443
     54981 | + ssh
           | |-- ESTABLISHED     | ip1b-lb3-prd.iad.github.com:22
     54985 | + ssh
           | |-- ESTABLISHED     | ip1b-lb3-prd.iad.github.com:22

By default, it shows connections of the proccesses that user has permissions to access to.
If you have problem with that, feel free to run it with `sudo`.

It shows the least bit of information - for example, it doesn't bother to show you the source IP. Or connections marked as `CLOSE`. Or `localhost <-> localhost` connections.

There's some options, though, to satisfy your curiosity. Feel free to run it with `--help` to see something like that:

      -n          don't resolve hostnames
      -l          show connections that go to localhost
      -p          show incoming hostnames (it doesn't filter the connection list;
                  just suppresses a bit of output)
      -c          show closed connections
      -s SEARCH   search in outgoing hosts by wildcard
