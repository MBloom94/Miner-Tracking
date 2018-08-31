import argparse
import os
import Miner1Stats
import Miner1Reader
import Miner1Watcher
import Miner1Plotter

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--live', help='Plot live data with defaults.',
                    action='store_true')
parser.add_argument('-r', '--read_log', help='Read default log file first.',
                    action='store_true')
parser.add_argument('-p', '--path', help='Path to file\'s directory.')
parser.add_argument('-f', '--file', help='File name. ')
parser.add_argument('-i', '--interval', help='Seconds between stats.',
                    type=int)
args = parser.parse_args()

if args.path:
    path = args.path
else:
    path = ("C:/Claymore/Claymore Miner/"
            "Claymore's Dual Ethereum"
            "+Decred_Siacoin_Lbry_Pascal_Blake2s_Keccak "
            "AMD+NVIDIA GPU Miner v11.8/")

if args.file:
    f = args.file
else:
    # Get most recent log in path.
    # Iterate files in order and the last one stays assigned to f
    for file in os.listdir(path):
        if file.endswith('_log.txt'):
            f = file

if args.interval:
    inter = args.interval
else:
    inter = 60

plotter = Miner1Plotter.Plotter(inter)
reader = Miner1Reader.Reader(path, f)

# Plot Static or Live
if args.live:
    if args.read_log:
        plotter.plot_live(reader)
    else:
        watcher = Miner1Watcher.Watcher()
        plotter.plot_live(watcher)
else:
    plotter.plot_static(reader)
