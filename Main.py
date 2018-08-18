import Miner1Stats
import Miner1Reader
import Miner1Watcher
import Miner1Plotter

watcher = Miner1Watcher.Watcher()
plotter = Miner1Plotter.Plotter()

plotter.plot_live(watcher)
