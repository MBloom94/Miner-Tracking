# Miner-Tracking

Miner Tracking is a project to locally monitor my full Etherem node and mining rig. 

The mining software running is Claymore's Ethereum AMD+NVIDIA GPU Miner, and Geth. It responds to json requests via raw TCP/IP sockets. 

Miner Tracker's purpose is to show statistics, from one or more miners (using Claymore) in a local network, over a given interval in a more readable format. 

Goals include:

Current statistics in a command line format.

Miner1Watcher.py works, but i have yet to move network settings to a config file or make it very pretty.
    
Current statistics in an animated graph format

Miner1Plotter.py shows live Mh/s every 1s and shows a minute of uptime. Plan to make those command line variables or config files.
    
Past statistics from open-able log text files

Currently building new Miner1Stats.py Stats obj to progress and make a better Miner1Reader.py, will rebuild Watcher and Plotter
with Stats()
