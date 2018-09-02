# Miner-Tracking

Miner Tracking is a project to locally monitor my full Ethereum node and mining rig.

The mining software running is Claymore's Ethereum AMD+NVIDIA GPU Miner, and Geth. Claymore responds to json requests via raw TCP/IP sockets.

Miner Tracker's purpose is to show statistics, from one or more miners (using Claymore) in a local network, over a given interval in a more readable format.

Goals include:

* Current statistics in a command line format.

  * Miner1Watcher.py if run independently will check for stats every 4 seconds and print them to the console. Interval is changeable but I wont be putting more into running Watcher directly. It should be instantiated then run with Plotter.

* Current statistics in an animated graph format.

  * Miner1Plotter.py shows live hash rate and effective hash rate. Default interval is 60 seconds but can be passed an interval parameter in seconds. Again, should be instantiated and run from Main.py.

* Past statistics from open-able log text files.

  * Miner1Plotter.py can plot a Reader statically with hash rate and effective hash rate. This is the default action when Main.py is run.

* Command line arguments for different options.

  * Main.py has multiple options. By default it uses Plotter to plot the most recent log file in the default path directory. If --live is given, it will instead plot using Watcher. If both --live and --read_log are given, it will plot the log using Reader and continue checking the log and updating the plot on the default interval. Other options include --path, --file, and --interval for those settings.
