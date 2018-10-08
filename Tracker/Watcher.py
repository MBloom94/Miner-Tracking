import socket
import json
import time
from datetime import datetime
from retrying import retry
import os
import sys
import Stats
import configparser


class Watcher:
    '''Watches Miner and collects stats'''

    host = None
    port = None
    # Create json request to send
    request = {'id': 0,
               'jsonrpc': '2.0',
               'method': 'miner_getstat1'}  # dict
    request = json.dumps(request)  # converts dict to str
    request = bytes(request + '\n', 'utf-8')  # converts str to bytes-object
    # + '\n' is for support with Phoenix Miner

    def __init__(self, miner):
        '''Create stats headers and a Stats.stats_list.'''
        # TODO: Determine number of stats sources/miners there are
        # maybe an optional param int? default is one local one?
        #
        # Trying 'miners' as a list of strings, miner names.
        # Default is none, sets screwdriver default.
        if miner is None:
            self.miner = 'SCREWDRIVER'
            print('{}: WARNING: No miner specified. Using default {}'.format(__name__, self.miner))
        else:
            self.miner = miner
        # TODO: Change to for each miner in miners...
        miner = self.miner
        # Manage multiple stats, one per miner. Maybe add stats.name?
        self.stats = Stats.Stats('Claymore json')
        # TODO: make stats_headers part of Stats
        self.stats_headers = ['datetime', 'hashrate',
                              'shares', 'rejects',
                              'temp', 'fans']
        # Get host and port from config or user
        config = configparser.ConfigParser()
        config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
        config.read(config_file)
        # Host from config
        if config[miner]['host']:
            self.host = config[miner]['host']
            print('{}: Host set {}'.format(__name__, self.host))
        else:  # Host from user, overwrites in config
            self.host = input('No host set. Enter host IP.\n>')
            print('{}: Host set: {}'.format(__name__, self.host))
            config[miner]['host'] = self.host
            with open(config_file, 'w') as cf:
                config.write(cf)
        # Port from config
        if config[miner]['port']:
            self.port = int(config[miner]['port'])
            print('{}: Port set {}'.format(__name__, self.port))
        else:  # Port from user, overwrites in config
            self.port = input('No port set. Enter port number.\n>')
            print('{}: Port set: {}'.format(__name__, self.port))
            config[miner]['port'] = self.port
            with open(config_file, 'w') as cf:
                config.write(cf)

    def retry_on_oserror(exc):
        '''Return true if the exception is an OSError.'''
        return isinstance(exc, OSError)

    '''I ran into an issue a few times where I would try to connect the socket
    and it would raise an error that the socket was in use. To resolve this,
    I import retrying and use the retry decorator, with a function to
    let it retry after an OSError. # TODO: specify it as WinError 10048'''
    @retry(wait_fixed=100, stop_max_attempt_number=5,
           retry_on_exception=retry_on_oserror)
    def get_new_response(self):
        '''Open a socket stream, send a request, and return the response.'''
        # Create a socket stream
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # If Claymore is running
        try:
            s.connect((self.host, self.port))
            s.sendall(Watcher.request)  # Send request bytes object
            response = s.recv(1024)  # Receive response
            response = json.loads(response)  # Convert bytes to dict
            s.close()
            return response
        except ConnectionRefusedError as exc:
            sys.exit('Connection refused.\n    Check if Claymore is running.')

    def get_new_stat(self):
        '''Parse and return the 'result' from the response.'''
        timestamp = datetime.now()
        #
        response = self.get_new_response()
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
        self.stats.add_stat(new_stat)

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
        self.get_new_stat()

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
