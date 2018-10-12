import argparse
import configparser
import os
import sys
import Stats
import Reader
import Watcher
import Plotter


def main():
    '''CLI entrypoint'''
    # Set up arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--live',
                        help=("Plot live data. By default uses Watcher with "
                              "default interval. "),
                        action='store_true')
    parser.add_argument('-r', '--read_log',
                        help=("Plot a log file. Use --path and --file to "
                              "specify source."),
                        action='store_true')
    parser.add_argument('-p', '--path', help='Path to file\'s directory.')
    parser.add_argument('-f', '--file', help='File name.')
    parser.add_argument('-i', '--interval', help='Stats interval in seconds.',
                        type=int)
    parser.add_argument('-m', '--miner', help='Name of miner for watcher.')
    args = parser.parse_args()
    # Get config info from file
    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_file)

    # Get file path
    if args.path:
        # If path is given as an argument
        path = args.path
        print('{}: Path set {}'.format(__name__, path))
        # Check if path exists in config
        if config['DEFAULT']['path']:
            # Path exists in config, do nothing
            pass
        else:
            # Set config['DEFAULT']['path'] to args.path
            config['DEFAULT']['path'] = args.path
            with open(config_file, 'w') as cf:
                config.write(cf)
    else:
        # No path arg given
        # Check config file
        if config['DEFAULT']['path']:
            # Use path from config
            path = config['DEFAULT']['path']
        else:
            # Path not in config or given, get path from user
            sys.exit('No path arg given, no path in config. Use --path to set path.')

    # Get file name
    if args.file:
        f = args.file
        print('{}: File set {}'.format(__name__, f))
    else:
        # Get most recent log in path.
        # Iterate files in order and the last one stays assigned to f
        try:
            for file in os.listdir(path):
                if file.endswith('_log.txt'):
                    f = file
        except FileNotFoundError as exc:
            print('{}: File or direcory not found with path. Try using --path.'.format(__name__))
            sys.exit('Path attempted: \n    {}'.format(path))

    # Set data interval
    if args.interval:
        inter = args.interval
        print('{}: Interval set {}s'.format(__name__, inter))
    else:
        if config['DEFAULT']['interval']:
            inter = int(config['DEFAULT']['interval'])
        else:
            inter = 60

    '''Command logic for which data source to plot'''

    #  Set command
    if args.live and args.read_log:
        sys.exit('Use either --live or --read_log but not both.')
    elif args.live:
        command = 'watch'
    elif args.read_log:
        command = 'read'

    # Prep plotter
    plotter = Plotter.Plotter(inter)
    # TODO: Set default plotter range

    '''Commands'''

    def default():
        #  Get default stat source from config_file
        watch()

    def read():
        reader = Reader.Reader(path, f)
        print('{}: Plotting {}.'.format(__name__, f))
        plotter.plot_static(reader)

    def watch():
        if args.miner:
            miner = args.miner
            print('{}: Miner set {}'.format(__name__, miner))
        else:
            miner = 'SCREWDRIVER'
            print('{}: Miner not set. Using default {}'.format(__name__, miner))

        watcher = Watcher.Watcher(miner)
        print('{}: Plotting live stats every {}s.'.format(__name__, inter))
        plotter.plot_live(watcher)

    command_pick = {
        'default': default,
        'read': read,
        'watch': watch
    }
    com = command_pick.get(command)
    com()

    # # Plot Static or Live
    # if args.live:
    #     if args.read_log:
    #         reader = Reader.Reader(path, f)
    #         print('{}: Plotting live stats with log every {}s.'.format(__name__, inter))
    #         plotter.plot_live(reader)
    #     else:
    #         # Using Watcher for live stats
    #         if args.miner:
    #             miner = args.miner
    #             print('{}: Miner set {}'.format(__name__, miner))
    #         else:
    #             miner = 'SCREWDRIVER'
    #             print('{}: Miner not set. Using default {}'.format(__name__, miner))
    #
    #         watcher = Watcher.Watcher(miner)
    #         print('{}: Plotting live stats every {}s.'.format(__name__, inter))
    #         plotter.plot_live(watcher)
    # else:
    #     reader = Reader.Reader(path, f)
    #     print('{}: Plotting {}.'.format(__name__, f))
    #     plotter.plot_static(reader)
