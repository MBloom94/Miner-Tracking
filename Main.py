import argparse
import configparser
import os
import sys
import Miner1Stats
import Miner1Reader
import Miner1Watcher
import Miner1Plotter

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--live',
                    help=("Plot live data. By default uses Watcher with "
                          "default interval. Aditionally use -r / --read_log "
                          "to use Reader."),
                    action='store_true')
parser.add_argument('-r', '--read_log',
                    help=("If --live is set, --read_log will cause Reader to "
                          "be used instead of Watcher to plot log data and "
                          "then continue plotting live data."),
                    action='store_true')
parser.add_argument('-p', '--path', help='Path to file\'s directory.')
parser.add_argument('-f', '--file', help='File name.')
parser.add_argument('-i', '--interval', help='Stats interval in seconds.',
                    type=int)
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config.ini')

if args.path:
    path = args.path
    print('Main:Path set {}'.format(path))
else:
    # Default path to Claymore logs directory.
    if config['DEFAULT']['path']:
        path = config['DEFAULT']['path']
    else:
        path = ("C:/Claymore/Claymore Miner/"
                "Claymore's Dual Ethereum"
                "+Decred_Siacoin_Lbry_Pascal_Blake2s_Keccak "
                "AMD+NVIDIA GPU Miner v11.8/")

if args.file:
    f = args.file
    print('Main:File set {}'.format(f))
else:
    # Get most recent log in path.
    # Iterate files in order and the last one stays assigned to f
    try:
        for file in os.listdir(path):
            if file.endswith('_log.txt'):
                f = file
    except FileNotFoundError as exc:
        print('Main:File or direcory not found with path. Try using --path.')
        sys.exit('Path attempted: \n    {}'.format(path))

if args.interval:
    inter = args.interval
    print('Main:Interval set {}s'.format(inter))
else:
    if config['DEFAULT']['interval']:
        inter = int(config['DEFAULT']['interval'])
    else:
        inter = 60

plotter = Miner1Plotter.Plotter(inter)
reader = Miner1Reader.Reader(path, f)

# Plot Static or Live
if args.live:
    if args.read_log:
        print('Main:Plotting past and live stats with Reader.')
        plotter.plot_live(reader)
    else:
        print('Main:Plotting live stats with Watcher every {}s.'.format(inter))
        watcher = Miner1Watcher.Watcher()
        plotter.plot_live(watcher)
else:
    print('Main:Plotting {} with Reader.'.format(f))
    # plotter.plot_static(reader)
    # testing
    watcher = Miner1Watcher.Watcher()
    plotter.plot_live(watcher)
