# Miner-Tracking

Miner Tracking is a program to locally monitor my Ethereum node and mining rig.

The mining software running is Claymore's Ethereum AMD+NVIDIA GPU Miner, and Geth. Claymore responds to json requests via raw TCP/IP sockets.

Miner Tracker's purpose is to show statistics, from a miner (using Claymore) in a local network, over a given interval in a more readable format.

Features include:

* Parse log files and present them in a graph.

  * The default function of Tracker is to find the most recent log file and plot it. Path is either read from the config.ini file, or passed in by the user with --path/-p.

* Present current statistics in a live animated graph.

  * Tracker will update the graph at a configurable interval (with config.ini or --interval/-i) using json requests to Claymore. If --read_log/-r is also included, Tracker will first graph the most recent log, then update the graph by checking the log. This uses the Reader class instead of the Watcher class.
