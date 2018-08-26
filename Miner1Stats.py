import datetime
import logging


class Stats():
    '''Stats object to hold list of stats from Miner1's logs.'''

    logging.basicConfig(filename='Miner1Log.log', level=logging.DEBUG)

    def __init__(self, type=None):
        '''Initialize generic and specific stats lists.'''
        self.type = type  # e.g. 'Claymore log'
        # Stats is used by Watcher, since all stats share a timestamp.
        self.stats = []
        # Reader however, has different stats at different timestamps.
        # Thus, it makes more sense to put specific stats in their own list
        # instead of mashing everything into a generic stats list.
        self.hash_rates_list = []  # [Timestamp, #####] (Kh/s)
        self.tshares_list = []  # Total shares as of timestamp.
        self.rejects_list = []  # Rejected shares as of timestamp.
        self.uptime = datetime.timedelta(minutes=0)  # Most recent uptime from stats
        self.last_job_date = ''  # Most recent date from New job
        self.ehr_list = []  # Effective hash rate, [Timestamp, #####] (Kh/s)
        self.diff = None  # Int difficulty e.g. 4000

    @property
    def stats_list(self):
        return self.stats

    @property
    def hash_rates(self):
        '''Get current hash rate list [[timestamp, hash_rate],
            [timestamp, hash_rate], etc...]
        '''
        return self.hash_rates_list

    @property
    def tshares(self):
        return self.tshares_list

    @property
    def ehrs(self):
        return self.ehr_list

    def add_stat(self, new_stat=None, format=True,
                 add_timestamp=False):
        '''Append a new stat to the list of stats.'''
        # TODO: Somehow skip reading over the whole log to get to the
        # new stats at the end.

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

    def format_claymore_json(self, unf_stat, add_timestamp=False):
        '''Take a list of claymore stats and assign them to stats.'''
        # Example unf_stat:
        # datetime, Kh/s, total shares, rejects, temp, fans %
        # ['datetime obj', '26406', '1038', '0', '59', '38']
        hash_rates = int(unf_stat[1])
        tshares = int(unf_stat[2])
        self.hash_rates_list.append([unf_stat[0], hash_rates])
        self.tshares_list.append([unf_stat[0], tshares])
        # Returning original stat so that stats.stats_list also has data.
        return unf_stat

    def format_claymore_log(self, unf_stat, add_timestamp=None):
        '''Take unformatted line from a Claymore log and save its items.'''

        '''Example unf_stat:
        07:03:53:554	3654	Check and remove old log files...
                     ^^      ^^
        The spaces  here &  here are \t s.
        '''
        f_stat = []
        # Try splitting on tabs and assigning to f_stat
        try:
            # unf_stat should have 'data\tdata\tdata'
            f_stat = unf_stat.split('\t')
            # stat[2] should have log data and end in a newline
            f_stat[2] = f_stat[2].rstrip('\n')
        except IndexError as err:
            logging.warning('Abnormal unf_stat. Raised {}'.format(err))
            logging.warning('--> {}'.format(f_stat))
            return None

        '''Here, the unformatted Claymore log line is split in 3.
        f_stat[0] is the timestamp, string, H:M:S:f
        f_stat[1] is something... not sure yet. Messaged Claymore.
        f_stat[2] is the message written to the log.
        '''

        # Save most recent date from New job for datetimestamps
        if 'New job from' in f_stat[2]:
            # ETH: 08/05/18-21:39:14 - New job from us1.ethermine.org:4444
            # or...
            # DevFee: ETH: 08/05/18-21:56:43 - New job from...
            # Get just the MM/DD/YY from string.
            new_date = f_stat[2]
            if 'DevFee: ETH: ' in new_date:
                new_date = new_date[13:21]
            else:
                new_date = new_date[5:13]
            # If new_date is different than last_job_date, overwrite it
            if new_date != self.last_job_date:
                self.last_job_date = new_date

        # Save target difficulty.
        if 'target:' in f_stat[2]:
            # target: 0x0000000112e0be82 (diff: 4000MH), epoch 202(2.58GB)
            target = f_stat[2]
            diff = target.split('diff: ', 1)[1]  # 4000MH), epoch 202(2.58GB)
            diff = diff.split('MH)', 1)[0]  # 4000
            diff = int(diff)  # string to int
            self.diff = diff

        # Split stats and add them to their lists.
        if 'ETH - Total Speed:' in f_stat[2]:
            # Add most recent date and current timestamp
            time_w_date = self.last_job_date + ' ' + f_stat[0]
            # Convert str to datetime. e.g. 16:46:34:398
            timestamp = datetime.datetime.strptime(time_w_date, '%m/%d/%y %H:%M:%S:%f')

            # ETH - Total Speed: 26.570 Mh/s, Total Shares: 11,
            # Rejected: 0, Time: 00:00
            eth_stats = f_stat[2].split(', ')

            # Assign Kh/s
            speed = eth_stats[0]  # 'ETH - Total Speed: 26.570 Mh/s'
            speed = speed.split('Speed: ', 1)[1]  # '26.570 Mh/s'
            speed = speed.split(' Mh/s', 1)[0]  # '26.570'
            khs = int(float(speed) * 1000)  # 26570
            # If this timestamp is not already there...
            # Necessary because we are rereading logs when animating plot_live
            if [timestamp, khs] not in self.hash_rates_list:
                self.hash_rates_list.append([timestamp, khs])

            # Assign total shares as of timestamp
            unf_tshares = eth_stats[1]
            tshares = ''.join(filter(str.isdigit, unf_tshares))  # only digits
            total_shares = int(tshares)
            try:
                # If total shares greater than the last entry...
                if total_shares > self.tshares_list[-1][1]:
                    self.tshares_list.append([timestamp, total_shares])
            except IndexError as err:
                if len(self.tshares_list) == 0:
                    self.tshares_list.append([timestamp, total_shares])

            # Assign rejected shares
            rejects = eth_stats[2]  # Rejected: 0
            rejects = rejects.split('Rejected: ', 1)[1]  # 0
            self.rejects_list.append([timestamp, rejects])

            # Assing uptime
            uptime = eth_stats[3]  # Time: 00:00
            uptime = uptime.split('Time: ', 1)[1]  # 00:00 (hours:minutes)
            # Hours goes past 24 instead of incrementing days
            uptime = uptime.split(':')  # 00, 00
            uptime = datetime.timedelta(hours=int(uptime[0]),
                                        minutes=int(uptime[1]))
            self.uptime = uptime

        def shares_last_hour():
            '''Calculate and return number of shares in the last hour.'''
            result = None
            cur_shares = self.tshares_list[-1]  # Newest [timestamp, int] share
            # Find share with timestamp 1hr less than cur_shares timestamp
            for share in self.tshares_list:
                delta = cur_shares[0] - share[0]  # timedelta
                # If in hour range from current
                if delta <= datetime.timedelta(minutes=60):
                    # Current total shares - shares as of 1hr ago
                    result = cur_shares[1] - share[1]
                    return result

        # Update ehr_list every 10 minutes
        # If uptime is an hour or more...
        # Because ehr can not be calculated with less than an hour of data.
        hour_delta = datetime.timedelta(minutes=60)
        ten_delta = datetime.timedelta(minutes=10)
        if self.uptime >= hour_delta:
            # Create timestamp for ehr_list
            time_w_date = self.last_job_date + ' ' + f_stat[0]
            # Convert str to datetime. e.g. 16:46:34:398
            timestamp = datetime.datetime.strptime(time_w_date,
                                          '%m/%d/%y %H:%M:%S:%f')
            # If ehr_list is empty
            if not self.ehr_list:
                # Calculate and add ehr
                # Get number of shares in last hour
                shares = shares_last_hour()
                # Calculate effective hash rate.
                ehr = round(self.diff * shares / 3600) * 1000
                # Append new ehr stats
                self.ehr_list.append([timestamp, ehr])
            # Else if current stat time is 10 min newer than most recent ehr
            elif timestamp - self.ehr_list[-1][0] >= ten_delta:
                # Calculate and add ehr
                # Get number of shares in last hour
                shares = shares_last_hour()
                # Calculate effective hash rate.
                ehr = round(self.diff * shares / 3600, 3) * 1000
                # Append new ehr stats
                if [timestamp, ehr] not in self.ehr_list:
                    self.ehr_list.append([timestamp, ehr])
                # TODO: Make this an if or.


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
            'Claymore json': self.format_claymore_json,
            'csv': self.format_csv
        }
        formatter = stat_types.get(self.type, lambda: 'Invalid type')
        if add_timestamp:
            return formatter(unf_stat, add_timestamp=True)
        else:
            return formatter(unf_stat)


# If Miner1Stats.py is run individually...
if __name__ == '__main__':
    clay_stats = Stats('Claymore log')
    clay_stats.add_stat('16:46:49:750	285c	'
                        + 'ETH - Total Speed: 26.302 Mh/s, '
                        + 'Total Shares: 0, Rejected: 0, Time: 00:00')
    print(clay_stats.hash_rates)
