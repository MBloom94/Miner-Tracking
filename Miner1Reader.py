import Miner1Stats as Stats
import Miner1Watcher as Watcher


class Reader():
    '''Read, parse, and save a log from Claymore's Miner.'''
    # default_file_name = 'sample logs/1533940877_log.txt'
    default_file_name = 'sample logs/1533156394_log.txt'

    def __init__(self, file_name=None):
        '''Initialize Reader, prep file for reading.'''
        if file_name is None:
            self.file_name = self.default_file_name
        else:
            self.file_name = file_name
        # Create stats object for Claymore log files.
        self.stats = Stats.Stats(type='Claymore log')
        # Open file to read, for each line add it to stats.
        # add_stat will format it as a Claymore log and add data
        # to a hash rates list.
        with open(self.file_name, 'r') as f:
            for f_line in f:
                f_line = f.readline()
                if f_line.strip():
                    self.stats.add_stat(f_line)
                    # print(f_line, end='')

        for hr in self.stats.hash_rates:
            print('{} - {}'.format(hr[0], hr[1]))

    # def print_hash_rate(self):
    #     Watcher.print_stats_pretty(self.stats.hash_rates)


# If Miner1Reader.py is run individually...
if __name__ == '__main__':
    reader = Reader()
    # reader.print_hash_rate()
