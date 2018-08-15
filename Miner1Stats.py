from datetime import datetime


class Stats():
    '''Stats object to hold list of stats from Miner1's logs.'''

    def __init__(self, type=None):
        '''Initialize generic and specific stats lists.'''
        self.type = type  # e.g. 'Claymore log'
        # Stats is used by Watcher, since all stats share a timestamp.
        self.stats = []
        # Reader however, has different stats at different timestamps.
        # Thus, it makes more sense to put specific stats in their own list
        # instead of mashing everything into a generic stats list.
        self.hash_rate_list = []  # [Timestamp, ##.###] (Mh/s)
        self.tshares_list = []  # Total shares as of timestamp.

    @property
    def stats_list(self):
        return self.stats

    @property
    def hash_rates(self):
        '''Get current hash rate list [[timestamp, hash_rate],
            [timestamp, hash_rate], etc...]
        '''
        return self.hash_rate_list

    def add_stat(self, new_stat=None, format=True,
                 add_timestamp=False):
        '''Append a new stat to the list of stats.'''

        '''Receive a string: new_stat, bool: format, bool: add_timestamp.
        A new stat should always be received. Format by
        default is true.
        Adding a timestamp is default false but is passed
        to the formatter either way.
        '''
        if new_stat is None:
            print('No new stat given, none added.')
            return False  # Allow testing if stat was added or not.
        else:
            if format:
                n = self.format_stat(new_stat, add_timestamp)
                if n is not None:
                    self.stats.append(n)
            else:
                self.stats.append(new_stat)
            # print('New stat added:')
            # print('--> {}'.format(new_stat))
            # return True
            # Add testing if the stat was actually added correctly.

    def format_csv(self, unf_stat, add_timestamp=False):
        '''Take a string line and return it split it by ','.'''
        f_stat = unf_stat.split(',')  # Mostly for testing purposes.
        if add_timestamp:
            f_stat.insert(0, datetime.now())
        return f_stat

    def format_claymore_log(self, unf_stat, add_timestamp=None):
        '''Take unformatted line from a Claymore log and return its items.'''

        '''Example unf_stat:
        07:03:53:554	3654	Check and remove old log files...
                     ^^      ^^
        The spaces  here &  here are \t s.
        '''
        f_stat = []
        # Try formatting
        try:
            # unf_stat should have 'data\tdata\tdata'
            f_stat = unf_stat.split('\t')
            # stat[2] should have log data and end in a newline
            f_stat[2] = f_stat[2].rstrip('\n')
        except IndexError as err:
            print('Abnormal unf_stat. Raised {}'.format(err))
            print(f_stat)
            return None

        '''Here, the unformatted Claymore log line is split in 3.
        f_stat[0] is the timestamp (currently string form...)
        f_stat[1] is something... not sure yet. Messaged Claymore.
        f_stat[2] is the message written to the log.
        '''
        if 'ETH - Total Speed:' in f_stat[2]:
            eth_stats = f_stat[2].split(',')
            # Mh/s
            speed = eth_stats[0]
            mhs = speed[-11:-5]
            self.hash_rate_list.append([f_stat[0], mhs])
            # Total shares as of timestamp
            unf_tshares = eth_stats[1]
            tshares = ''.join(filter(str.isdigit, unf_tshares))  # only digits
            total_shares = int(tshares)
            self.tshares_list.append([f_stat[0], total_shares])

        # We want other formatters to be able to return a value to append
        # to self.stats, so this function will return None so that stats does
        # not get extra empty data.
        return None

    def format_stat(self, unf_stat, add_timestamp=False):
        '''Take an unformatted string and return a list of parsed items.'''

        '''Make a dict of functions to be executed depending on
        the type of stats. Then, return its result.

        This allows for different formatters to be used based on
        the set stat type. Makes it easier to add other log types
        in the future, maybe from other miners than Claymore.
        CSV is included for testing purposes.
        '''
        if self.type is None:
            print('Stats created with no type. Stat not formatted.')
            return unf_stat

        stat_types = {
            'Claymore log': self.format_claymore_log,
            'csv': self.format_csv
        }
        formatter = stat_types.get(self.type, lambda: 'Invalid type')
        if add_timestamp:
            return formatter(unf_stat, add_timestamp=True)
        else:
            return formatter(unf_stat)


# If Miner1Stats.py is run individually...
if __name__ == '__main__':
    csv_stats = Stats('csv')
    csv_stats.add_stat('testing,this,function')
    print(csv_stats.stats_list)
    csv_stats.add_stat('testing,this,function,again', add_timestamp=True)
    print(csv_stats.stats_list)
    clay_stats = Stats('Claymore log')
    clay_stats.add_stat('07:03:53:554	3654	Check and remove old log files...')
    print(clay_stats.stats_list)
