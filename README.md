# Setup

- install socat (used by tbtail): `$ sudo apt-get install socat`

Might remove this dependency by writing a simple UDP receiver in python but it's okay for now.

- install upstart (used to run tbprocessd): `$ sudo apt-get install upstart`

Didn't realise this wasn't standard on the Pi. It does keep-alive though, so maybe worth it?

Running in development mode:

    $ python main.py

Installing (on Raspberry Pi):

    $ make build
    $ sudo make install

This installs the binary `tbprocessd` and the utility scripts (`tbopen` and `tbtail`). Reboot to
start upstart and thus tbprocessd.

# What does it do?
                                                          
          1. “tbprocessd runs the home screen”            
    ------------------------------------------------      
                                                          
                                            Λ             
           ┌─────────────────┐             ╱ ╲            
           │                 │   logs     ╱   ╲           
           │   tbprocessd    │──────────▶╳ UDP ╳          
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
           │   tbprocessd    │──────────▶╳ UDP ╳          
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

# Running without installing

If you want to run without installing you just need to set the HOME_APP variable to whatever you
want tbprocessd to run by default. Example terminal session:

    $ export HOME_APP=../tbhome
    $ python main.py &
    $ ./tbtail
    ...
    ^C
    $ ./tbopen ../example_app
    $ ./tbtail

This will run the app at ../tbhome, reboot it if it crashes, and run the example_app, if this
crashes or exits, return to the home screen.
