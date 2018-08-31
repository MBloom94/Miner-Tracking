import sys
import Miner1Stats
import Miner1Reader
import Miner1Watcher
import Miner1Plotter

path = "C:\Claymore\Claymore Miner\Claymore's Dual Ethereum+Decred_Siacoin_Lbry_Pascal_Blake2s_Keccak AMD+NVIDIA GPU Miner v11.8/"
f = "1534729180_log.txt"
inter = 60  # Second interval to update

watcher = Miner1Watcher.Watcher()
reader = Miner1Reader.Reader(path, f)
plotter = Miner1Plotter.Plotter(inter)

# plotter.plot_live(watcher)
plotter.plot_static(reader)
# plotter.plot_live(reader)
