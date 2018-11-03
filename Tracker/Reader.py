import Stats
import time
import datetime


class Reader():
    '''Read, parse, and save a log from Claymore's Miner.'''

    def __init__(self, path, file_name):
        '''Initialize Reader, prep file for reading.'''
        self.path = path
        # Check if path ends in / or \
        if path.endswith('/') or path.endswith('\\'):
            # path is good
            pass
        else:
            self.path += '/'
        self.file_name = file_name
        # Create stats object for Claymore log files.
        self.stats = Stats.Stats(type='Claymore log')

    def read_log(self):
        '''Open file to read, for each line add it to stats.'''
        points = 0  # Loading bar num of .s

        # add_stat will format it as a Claymore log and add data
        # to a hash rates list.
        print('{}: Reading file: {}'.format(__name__, self.file_name))
        # Explicitly setting encoding to ISO-8859-1
        with open(self.path + self.file_name,
                  encoding='ISO-8859-1', mode='r') as f:
            for f_line in f:
                f_line = f.readline()
                if f_line.strip():
                    self.stats.add_stat(f_line)
                    # print(f_line, end='')
                # Loading animation
                print('{}: Reading line: {}'.format(__name__, points), end="\r")
                points += 1
            print()
            f.close()

    def update_stats(self):
        '''Update current stats with read_log.'''
        self.read_log()

    def print_hash_rates(self):
        for hr in self.stats.hash_rates:
            print('{}: {} - {}'.format(__name__, hr[0], hr[1]))

    def print_total_shares(self):
        for ts in self.stats.tshares_list:
            print('{}: {} Shares as of {}'.format(__name__, ts[1], ts[0]))

    @property
    def timestamps(self):
        return self.stats.hash_rates #  This is used with timestamps[-1][0]

    @property
    def hash_rates(self):
        return self.stats.hash_rates

    @property
    def tshares(self):
        return self.stats.tshares

    @property
    def ehrs(self):
        return self.stats.ehrs

    @property
    def avgs(self):
        return self.stats.avgs


# If Miner1Reader.py is run individually...
if __name__ == '__main__':
    reader = Reader()
    reader.read_log()
    reader.print_hash_rates()
    reader.print_total_shares()
