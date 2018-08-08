import socket
import json
import time
from datetime import datetime
from retrying import retry


class Watcher:
    '''Watches Miner and collects stats'''

    # Create json request to send
    request = {'id': 0,
               'jsonrpc': '2.0',
               'method': 'miner_getstat1'}  # dict
    request = json.dumps(request)  # converts dict to str
    request = bytes(request, 'utf-8')  # converts str to bytes-object

    def __init__(self):
        # Create stats headers and stats lists, stats being 2d
        self.stats_headers = ['datetime', 'hashrate',
                              'shares', 'rejects',
                              'temp', 'fans']
        self.stats = []

    def retry_on_oserror(exc):
        '''Return true if the exception is an OSError.'''
        return isinstance(exc, OSError)

    '''I ran into an issue a few times where I would try to connect the socket
    and it would raise an error that the socket was in use. To resolve this,
    I import retrying and use the retry decorator, with a function to
    let it retry after an OSError. # TODO: specify it as WinError 10048'''
    @retry(wait_fixed=100,
           retry_on_exception=retry_on_oserror)
    def get_new_response(self):
        '''Open a socket stream, send a request, and return the response.'''
        # Create a socket stream
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.1.66', 3333))
        s.sendall(Watcher.request)  # Send request
        response = s.recv(1024)  # Recieve response
        response = json.loads(response)  # Convert bytes to dict
        s.close()
        # raise OSError; for testing purposes
        return response

    def get_new_stats(self):
        '''Parse and return the 'result' from the response.'''
        response = self.get_new_response()
        timestamp = datetime.now()  # TODO: Get datetime timestamp
                                    #       - exe time... maybe half?
        # id = response['id']  Potentially use these in the future
        # error = response['error']  Potentially use these in the future
        result = response['result']  # list
        # Get the parts we care about from the result
        new_stats = [timestamp, result[2], result[6]]
        # Stretch 2 and 6 out into their own list items
        new_stats = self.stretch_stats(new_stats)
        self.stats.append(new_stats)

    def stretch_stats(self, stats_clumpy):
        '''Split and insert 2nd level list items into the parent lists.

        Take a clumpy list like:
        ['2670', '26406;1038;0', '59;38'],
        split the inside items based on instances of ';'.
        For each of the parent and child list items, append
        to a new list and return it. New list will look like:
        ['2670', '26406', '1038', '0', '59', '38'].
        '''
        self.stats_clumpy = stats_clumpy
        new_stats = []
        # For each element in stats, using range(len(var)) to iterate...
        for ele in range(len(self.stats_clumpy)):
            # For each item split in the current element of stats...
            if isinstance(self.stats_clumpy[ele], str):
                for item in range(len(self.stats_clumpy[ele].split(';'))):
                    # Append the item split from an ele of stats to newstats.
                    new_stats.append(self.stats_clumpy[ele].split(';')[item])
            else:
                new_stats.append(self.stats_clumpy[ele])
        return new_stats

    def print_stats_pretty(self, last_line=None):
        '''Print the last line of stats with additional formatting.'''

        # Assign last_line the last item in stats.
        # last_line = self.stats[-1]
        if last_line is None:
            last_line = self.stats[-1]

        # Assign pretty_stats a shell to be formatted
        pretty_stats = '{}, {}.{} Mh/s, {} Shares, {} Rejected, {}C, {}%'
        # Print with formatting
        print(pretty_stats.format(
            datetime.time(last_line[0]),
            last_line[1][:-3],  # Tens and Ones place of Mh/s
            last_line[1][-3:],  # .000 places of Mh/s
            last_line[2],       # Total shares
            last_line[3],       # Rejected shares
            last_line[4],       # Degrees in Celsius
            last_line[5]        # Fan speed %
        ))

    @property
    def timestamp(self):
        '''Get current uptime list.'''

        timestamp_list = []
        for stat in self.stats:
            timestamp_list.append(stat[0])
        return timestamp_list

    @property
    def hash_rate(self):
        '''Get current hash rate list'''

        hash_rate_list = []
        for stat in self.stats:
            hash_rate_list.append(int(stat[1]))
        return hash_rate_list


# Main Loop, runs until the user hits Ctrl-C to throw KeyboardInterrupt
if __name__ == '__main__':
    try:
        watcher = Watcher()
        start_time = time.time()  # Save starting time
        interval = 4.0  # Seconds
        while True:
            # Update stats list with current stats
            watcher.get_new_stats()
            # Print stats with formatting
            watcher.print_stats_pretty()
            # Pause for the interval - the execution time since start_time
            time.sleep(interval - ((time.time() - start_time) % interval))
    except KeyboardInterrupt:
        print('Closing Miner Watcher...')
