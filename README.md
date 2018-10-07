# Miner-Tracking

Miner Tracking is a program to locally monitor my Ethereum node and mining rig.

The mining software running is Claymore's Ethereum AMD+NVIDIA GPU Miner, and Geth. Claymore responds to json requests via raw TCP/IP sockets.

Miner Tracker's purpose is to show statistics, from a miner (using Claymore) in a local network, over a given interval in a more readable format.

Features include:

* Parse log files and present them in a graph.

  * The default function of Tracker is to find the most recent log file and plot it. Path is either read from the config.ini file, or passed in by the user with --path/-p.

* Present current statistics in a live animated graph.

  * Tracker will update the graph at a configurable interval (with config.ini or --interval/-i) using json requests to Claymore. If --read_log/-r is also included, Tracker will first graph the most recent log, then update the graph by checking the log. This uses the Reader class instead of the Watcher class.


# CLI use cases

Show live hashrate of local miner.

* python Tracker -l

* Creates a Watcher, checks config for default miner host & port, & interval to poll miner. If these are not in config the user is prompted for them. Values are saved.

Show live hashrate of multiple miners on the local network.

* python Tracker -l --miners INT

* Tedious plan for telling Tracker how many miners on the network we want to watch. Once we know how many we will check config for multiple [Miner#] sections for hosts and ports.
Then, when Plotter asks Watcher for stats, Watcher will add its stats objs together and return the sum.

Show log file.

* python Tracker

* First config is checked for path. If it isn't found, user is prompted to run python Tracker --path/-p STRING. Once a path is saved/given it finds the newest log file and plots it. If a specific log file is desired, use python Tracker --file/-f STRING.
