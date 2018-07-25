import socket
import json
import time
import datetime


# Create json request to send
request = {'id': 0,
           'jsonrpc': '2.0',
           'method': 'miner_getstat1'}  # dict
request = json.dumps(request)  # converts dict to str
request = bytes(request, 'utf-8')  # converts str to bytes-object

# Create stats headers and stats lists, stats being 2d
stats_headers = ['uptime', 'hashrate', 'shares', 'rejects', 'temp', 'fans']
stats = [[]]


def get_new_response():
    '''Open a socket stream, send a request, and return the response.'''
    # Create a socket stream
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.66', 3333))
    s.sendall(request)  # Send request
    response = s.recv(1024)  # Recieve response
    response = json.loads(response)  # Convert bytes to dict
    s.close()
    return response


def get_new_stats():
    '''Parse and return the 'result' from the response.'''
    response = get_new_response()
    # id = response['id']  Potentially use these in the future
    # error = response['error']
    result = response['result']  # list
    stats = [result[1], result[2], result[6]]
    stats = stretch_stats(stats)
    return stats


def stretch_stats(stats):
    '''Split and insert 2nd level list items into the parent lists.

    Take a list like:
    ['2670', '26406;1038;0', '59;38'],
    split the inside items based on instances of ';'.
    For each of the parent and child list items, append
    to a new list and return it. New list will look like:
    ['2670', '26406', '1038', '0', '59', '38'].
    '''
    newstats = []
    # For each element in stats, using range(len(var)) to iterate...
    for ele in range(len(stats)):
        # For each item split in the current element of stats...
        for item in range(len(stats[ele].split(';'))):
            # Append the item split from an element of stats to list: newstats.
            newstats.append(stats[ele].split(';')[item])
    return newstats


def print_stats_pretty(stats):
    '''Print the last line of stats with additional formatting.'''

    # Assign last_line the last item in stats.
    last_line = stats[-1]
    # Assign pretty_stats a shell to be formatted
    pretty_stats = '{}, {}.{} Mh/s, {} Shares, {} Rejected, {}C, {}%'
    # Print with formatting
    print(pretty_stats.format(
        # Convert minutes to a timedelta and remove seconds ([:-3]).
        str(datetime.timedelta(minutes = int(last_line[0])))[:-3],
        last_line[1][:-3],  # Tens and Ones place of Mh/s
        last_line[1][-3:],  # .000 places of Mh/s
        last_line[2],       # Total shares
        last_line[3],       # Rejected shares
        last_line[4],       # Degrees in Celsius
        last_line[5]        # Fan speed %
    ))


# Main Loop, runs until the user hits Ctrl-C to throw KeyboardInterrupt
try:
    start_time = time.time()  # Save starting time
    interval = 10.0  # Seconds
    while True:
        # Fetch current info and append them to list*2: stats
        stats.append(get_new_stats())
        # Display stats with formatting
        print_stats_pretty(stats)
        # Pause for the interval - the execution time since start_time
        time.sleep(interval - ((time.time() - start_time) % interval))
except KeyboardInterrupt:
    print('Closing Miner Watcher...')
