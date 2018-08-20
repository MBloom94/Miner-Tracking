import Miner1Stats as Stats


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

    def read_log(self):
        # Open file to read, for each line add it to stats.
        # add_stat will format it as a Claymore log and add data
        # to a hash rates list.
        with open(self.file_name, 'r') as f:
            for f_line in f:
                f_line = f.readline()
                if f_line.strip():
                    self.stats.add_stat(f_line)
                    # print(f_line, end='')

    def update_stats(self):
        '''Update current stats with read_log.'''
        self.read_log()

    def print_hash_rates(self):
        for hr in self.stats.hash_rates:
            print('{} - {}'.format(hr[0], hr[1]))

    def print_total_shares(self):
        for ts in self.stats.tshares_list:
            print('{} Shares as of {}'.format(ts[1], ts[0]))

    @property
    def hash_rates(self):
        return self.stats.hash_rates

    @property
    def tshares(self):
        return self.stats.tshares


# If Miner1Reader.py is run individually...
if __name__ == '__main__':
    reader = Reader()
    reader.read_log()
    reader.print_hash_rates()
    reader.print_total_shares()
    # reader.print_hash_rate()
