import argparse
import Miner1Stats
import Miner1Reader
import Miner1Watcher
import Miner1Plotter

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--live', help='Plot live data with defaults.',
                    action='store_true')
parser.add_argument('-p', '--path', help='Path to file\'s directory.')
parser.add_argument('-f', '--file', help='File name. ')
parser.add_argument('-i', '--interval', help='Seconds between stats.',
                    type=int)
args = parser.parse_args()

if args.path:
    path = args.path
else:
    path = "C:\Claymore\Claymore Miner\Claymore's Dual Ethereum+Decred_Siacoin_Lbry_Pascal_Blake2s_Keccak AMD+NVIDIA GPU Miner v11.8/"

if args.file:
    f = args.file
else:
    f = "1534729180_log.txt"

if args.interval:
    inter = args.interval
else:
    inter = 60

watcher = Miner1Watcher.Watcher()
reader = Miner1Reader.Reader(path, f)
plotter = Miner1Plotter.Plotter(inter)

# Plot Static or Live
if args.live:
    plotter.plot_live(watcher)
    # TODO: Add option for using reader for live with history
    # plotter.plot_live(reader)
else:
    plotter.plot_static(reader)
