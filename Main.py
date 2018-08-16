import Miner1Stats
import Miner1Reader
import Miner1Watcher
import Miner1Plotter

csv_stats = Miner1Stats.Stats('csv')
csv_stats.add_stat('testing,this,function')
print(csv_stats.stats_list)
csv_stats.add_stat('testing,this,function,again', add_timestamp=True)
print(csv_stats.stats_list)
clay_stats = Miner1Stats.Stats('Claymore log')
clay_stats.add_stat('07:03:53:554	3654	Check and remove old log files...')
