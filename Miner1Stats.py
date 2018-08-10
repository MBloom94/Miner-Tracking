from datetime import datetime


class Stats():
    '''Stats object to hold list of stats from Miner1's logs.'''
    default_stat_type = 'Claymore log'

    def __init__(self):
        self.stats = []

    @property
    def stats_list(self):
        return self.stats

    def add_stat(self, new_stat=None, format=True,
                 type=None, add_timestamp=False):
        '''Append a new stat to the list of stats.'''

        '''Receive a string: new_stat, bool: format,
        string: type of log, bool: add_timestamp.
        A new stat should always be received. Format by
        default is true. Type is either received or is
        set to Stats class var default_stat_type.
        Adding a timestamp is default false but is passed
        to the formatter either way.
        '''
        if new_stat is None:
            print('No new stat given, none added.')
            return False  # Allow testing if stat was added or not.
        else:
            if type is None:
                type = self.default_stat_type
            if format:
                self.stats.append(self.format_stat(
                    new_stat, type, add_timestamp))
            else:
                self.stats.append(new_stat)
            return True  # Add testing if the stat was actually added correctly.

    def format_csv(self, unf_stat, add_timestamp=False):
        '''Take a string line and return it split it by ','.'''
        f_stat = unf_stat.split(',')  # Mostly for testing purposes.
        if add_timestamp:
            f_stat.insert(0, datetime.now())
        return f_stat

    def format_claymore_log(self, unf_stat):
        '''Take an unformatted line from a Claymore log and return its items.'''

        '''Example unf_stat:
        07:03:53:554	3654	Check and remove old log files...
        '''
        f_stat = []
        f_stat.append(unf_stat[:12])  # 07:03:53:554
        f_stat.append(unf_stat[13:17])  # 3654
        f_stat.append(unf_stat[18:])  # Check and... -> end of string

        '''Here, the unformatted Claymore log line is split in 3.
        f_stat[0] is the timestamp (currently string form...)
        f_stat[1] is something... not sure yet. Messaged Claymore.
        f_stat[2] is the message written to the log.
        '''
        return f_stat

    def format_stat(self, unf_stat, type=None, add_timestamp=False):
        '''Take an unformatted string and return a list of parsed items.'''

        '''Make a dict of functions to be executed depending on
        the type received. Then, return its result.

        This allows for different formatters to be used based on
        the given stat type. Makes it easier to add other log types
        in the future, maybe from other miners than Claymore.
        CSV is included for testing purposes.
        '''
        if type is None:
            type = self.default_stat_type

        stat_types = {
            'Claymore log': self.format_claymore_log,
            'csv': self.format_csv
        }
        formatter = stat_types.get(type, lambda: 'Invalid type')
        if add_timestamp:
            return formatter(unf_stat, add_timestamp=True)
        else:
            return formatter(unf_stat)


# If Miner1Stats.py is run individually...
if __name__ == '__main__':
    stats = Stats()
    stats.add_stat('testing,this,function', type='csv')
    print(stats.stats_list)
    stats.add_stat('testing,this,function,again', type='csv', add_timestamp=True)
    print(stats.stats_list)
    stats.add_stat('07:03:53:554	3654	Check and remove old log files...')
    print(stats.stats_list)
