import socket
import json
import time
from datetime import datetime
from retrying import retry
import os
import sys
import Stats
import Miner
import configparser


class Watcher:
    '''Watches Miner and collects stats'''

    # Create json request to send
    request = {'id': 0,
               'jsonrpc': '2.0',
               'method': 'miner_getstat1'}  # dict
    request = json.dumps(request)  # converts dict to str
    request = bytes(request + '\n', 'utf-8')  # converts str to bytes-object
    # + '\n' is for support with Phoenix Miner

    def __init__(self, miners):
        '''Create stats headers and a Stats.stats_list.'''

        self.miners = miners
        self.stats_totals = Stats.Stats('Claymore json')


    def retry_on_oserror(exc):
        '''Return true if the exception is an OSError.'''
        return isinstance(exc, OSError)

    '''I ran into an issue a few times where I would try to connect the socket
    and it would raise an error that the socket was in use. To resolve this,
    I import retrying and use the retry decorator, with a function to
    let it retry after an OSError. # TODO: specify it as WinError 10048'''
    @retry(wait_fixed=100, stop_max_attempt_number=5,
           retry_on_exception=retry_on_oserror)
    def get_new_response(self, miner):
        '''Open a socket stream, send a request, and return the response.'''
        # Create a socket stream
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # If Claymore is running
        try:
            s.connect((miner.host, miner.port))
            s.sendall(Watcher.request)  # Send request bytes object
            response = s.recv(1024)  # Receive response
            response = json.loads(response)  # Convert bytes to dict
            s.close()
            return response
        except ConnectionRefusedError as exc:
            sys.exit('Connection refused.\n    Check if Claymore is running.')

    def get_new_stat(self, miner):
        '''Parse and return the 'result' from the response.'''
        timestamp = datetime.now()
        #
        response = self.get_new_response(miner)
        # TODO: Get datetime timestamp - exe time... maybe half?
        # id = response['id']  Potentially use these in the future
        # error = response['error']  Potentially use these in the future
        result = response['result']  # list
        # Get the parts we care about from the result
        new_stat = [timestamp, result[2], result[6]]
        # Stretch 2 and 6 out into their own list items
        new_stat = self.stretch_stats(new_stat)
        # new_stat == ['2670', '26406', '1038', '0', '59', '38'] for example.
        # print('Got_new_stat:')
        # print('--> {}'.format(new_stat))
        # self.stats.stats_list.append(new_stat)
        miner.stats.add_stat(new_stat)

    def stretch_stats(self, stats_clumpy):
        '''Split and insert 2nd level list items into the parent lists.

        Take a clumpy list like:
        ['2670', '26406;1038;0', '59;38'],
        split the inside items based on instances of ';'.
        For each of the parent and child list items, append
        to a new list and return it. New list will look like:
        ['2670', '26406', '1038', '0', '59', '38'].
        '''
        new_stat = []
        # For each element in stats, using range(len(var)) to iterate...
        for ele in range(len(stats_clumpy)):
            # For each item split in the current element of stats.stats_list...
            if isinstance(stats_clumpy[ele], str):
                for item in range(len(stats_clumpy[ele].split(';'))):
                    # Append the item split from an ele of stats to newstats.
                    new_stat.append(stats_clumpy[ele].split(';')[item])
            else:
                new_stat.append(stats_clumpy[ele])
        return new_stat

    def print_stats_pretty(self, last_line=None):
        '''Print the last line of stats with additional formatting.'''

        # print('Raw stats:')
        # print(self.stats.stats_list)

        # Assign last_line the last item in stats_list.
        # last_line = self.stats[-1]
        if last_line is None:
            last_line = self.stats.stats_list[-1]

        # Assign pretty_stats a shell to be formatted
        pretty_stats = '{}: {}, {}.{} Mh/s, {} Shares, {} Rejected, {}C, {}%'
        # Print with formatting
        print(pretty_stats.format(
            __name__,
            # datetime.time(last_line[0]),
            last_line[0].strftime('%H:%M:%S'),
            last_line[1][:-3],  # Tens and Ones place of Mh/s
            last_line[1][-3:],  # .000 places of Mh/s
            last_line[2],       # Total shares
            last_line[3],       # Rejected shares
            last_line[4],       # Degrees in Celsius
            last_line[5]        # Fan speed %
        ))

    def update_stats(self):
        '''Update stats lists with get_new_stat for plotter.'''
        #  For each miner, fetch new stats
        for miner in self.miners:
            self.get_new_stat(miner)
        #  Update stat totals
        #  Create new 'total stat' to add
        # datetime, Kh/s, total shares, rejects
        # ['datetime obj', '26406', '1038', '0']
        sum_ts = datetime.now()
        #  This is fine... I can get a more accurate timestamp later
        sum_hr = 0
        sum_shares = 0
        sum_rejects = 0
        # Add up all the miners most recent hashrates
        for miner in self.miners:
            sum_hr += miner.stats.hash_rates[-1][1]
            sum_shares += miner.stats.tshares[-1][1]
            sum_rejects += miner.stats.rejects[-1][1]

        sum_stat = [sum_ts, sum_hr, sum_shares, sum_rejects] #
        self.stats_totals.add_stat(sum_stat)


    @property
    def timestamps(self):
        return self.stats_totals.hash_rates

    @property
    def hash_rates(self):
        '''Return the sum of all miners hash_rates'''
        return self.stats_totals.hash_rates

    @property
    def tshares(self):
        '''Return the sum of all miners shares'''
        return self.stats_totals.tshares

    @property
    def ehrs(self):
        '''Return the sum of all miners effective_hash_rates'''
        return self.stats_totals.ehrs

    @property
    def avgs(self):
        '''Return sum of avgs'''
        return self.stats_totals.avgs


# Main Loop, runs until the user hits Ctrl-C to throw KeyboardInterrupt
if __name__ == '__main__':
    try:
        watcher = Watcher()
        start_time = time.time()  # Save starting time
        interval = 4.0  # Seconds
        while True:
            # Update stats list with current stats
            watcher.get_new_stat()
            # Print stats with formatting
            watcher.print_stats_pretty()
            # Pause for the interval - the execution time since start_time
            time.sleep(interval - ((time.time() - start_time) % interval))
    except KeyboardInterrupt:
        print('{}: Closing Miner Watcher...'.format(__name__))
