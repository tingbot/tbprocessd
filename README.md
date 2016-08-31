# tbprocessd

This daemon launches apps on Tingbot. Because there's only one screen, there can be only one
app running at once. Tbprocessd also collects the log messages from the running app and makes
them available to stream over a ZMQ socket.

Commands are sent to the daemon via HTTP. Utilities `tbopen` and `tbtail` are supplied to simplify
this process.

Also included is `tbbuttonsd`, which monitors button presses on the Tingbot and calls tbprocessd
when the 'home' combo is pressed.

## Setup

Running in development mode:

    $ python tbprocessd.py

Installing (on Raspberry Pi):

    $ sudo python setup.py install
    $ sudo cp tbprocessd.service /etc/init.d

This installs the binary `tbprocessd` and the utility scripts (`tbopen` and `tbtail`). 

## What does it do?
                                                          
          1. “tbprocessd runs the home screen”            
    ------------------------------------------------      
                                                          
                                            Λ             
           ┌─────────────────┐             ╱ ╲            
           │                 │   logs     ╱   ╲           
           │   tbprocessd    │──────────▶╳ ZMQ ╳          
           │                 │            ╲   ╱           
           └─────────────────┘             ╲ ╱            
               │        ▲                   V             
               │        │                                 
               │        │                                 
        starts │        │ logs (stdout, stderr)           
               │        │                                 
               │        │                                 
               ▼        │                                 
           ┌─────────────────┐                            
           │                 │                            
           │   Home screen   │                            
           │                 │                            
           └─────────────────┘                            

On startup, tbprocessd starts the home screen, which is defined by the HOME_APP variable. This
is configured in the upstart.conf, the current value is `/apps/home`. If the home screen crashes,
tbprocessd will relaunch it.

    2. “Home screen tells tbprocessd to open an app”      
    -------------------------------------------------     
                                                          
                                                          
           ┌─────────────────┐                            
           │                 │                            
           │   tbprocessd    │                            
           │                 │                            
           └─────────────────┘                            
                    ▲                                     
                    │                                     
                    │          HTTP                       
                    └─────────────────────┐               
                                          │               
                                          │               
                                          │               
           ┌─────────────────┐            │               
           │                 │      ┌──────────┐          
           │   Home screen   │─────▶│//tbopen//│          
           │                 │      └──────────┘          
           └─────────────────┘                            

The home screen tells tbprocessd to start an app using the `tbopen` script. The command would be
something like `$ tbopen /apps/weather`.

           3. “tbprocessd starts the new app”             
    -------------------------------------------------     
                                                          
                                            Λ             
           ┌─────────────────┐             ╱ ╲            
           │                 │   logs     ╱   ╲           
           │   tbprocessd    │──────────▶╳ ZMQ ╳          
           │                 │            ╲   ╱           
           └─────────────────┘             ╲ ╱            
                    │   ▲                   V             
                    │   │                                 
                    │   └──────────┐                      
             starts │              │ logs (stdout, stderr)
                    └────────┐     │                      
                             │     │                      
           \     /           ▼     │                      
     ┌──────\───/──────┐  ┌─────────────────┐             
     │       \ /       │  │                 │             
     │   Home /creen   │  │   Weather app   │             
     │       / \       │  │                 │             
     └──────/───\──────┘  └─────────────────┘             
           /     \                                        

Home screen is killed and the new app is started. When tbprocessd is given a path to start, it will
try to launch `/apps/weather`, or if this is not a binary, it will try `/apps/weather/main`, and if
this does not exist, it will try `python /apps/weather/main.py`.

Logs from the new process can be accessed by running `tbtail`. This is going to be useful for Tide,
but might also be useful when testing the home screen.

When the weather app exits, Home Screen will be launched again.

## Running without installing

If you want to run without installing you just need to set the HOME_APP variable to whatever you
want tbprocessd to run by default. Example terminal session:

    $ export HOME_APP=../tbhome
    $ python tbprocessd.py &
    $ ./tbtail
    ...
    ^C
    $ ./tbopen ../example_app
    $ ./tbtail

This will run the app at ../tbhome, reboot it if it crashes, and run the example_app, if this
crashes or exits, return to the home screen.
