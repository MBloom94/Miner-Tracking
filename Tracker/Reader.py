import Stats
import time
import datetime
import sys
import os


class Reader():
    '''Read, parse, and save a log from Claymore's Miner.'''

    default_path = 'sample logs/'
    default_file_name = '1533156394_log.txt'

    def __init__(self, path=None, file_name=None):
        '''Initialize Reader, prep file for reading.'''
        if path is None:
            self.path = self.default_path
        else:
            self.path = path
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
        print('{}: Reading file: {}'.format(__name__, self.file_name))
        # loading = '\|/-\|/-'
        points = 0  # Number of '.'s to print
        tstamp = datetime.datetime.now()
        delta = datetime.timedelta(seconds=.2)
        cols, rows = os.get_terminal_size(0)
        # Explicitly setting encoding to ISO-8859-1
        with open(self.path + self.file_name,
                  encoding='ISO-8859-1', mode='r') as f:
            for f_line in f:
                f_line = f.readline()
                if f_line.strip():
                    self.stats.add_stat(f_line)
                    # print(f_line, end='')
                # Loading animation
                # If it has been .2s
                if datetime.datetime.now() - tstamp > delta:
                    if points <= cols:
                        sys.stdout.write('.')
                        sys.stdout.flush()
                        points += 1
                    else:
                        print()
                    tstamp = datetime.datetime.now()
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
