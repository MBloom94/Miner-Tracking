import argparse
import configparser
import os
import sys
import Stats
import Reader
import Watcher
import Plotter
import Miner


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
        if config['GENERAL']['path']:
            # Path exists in config, do nothing
            pass
        else:
            # Set config['GENERAL']['path'] to args.path
            config['GENERAL']['path'] = args.path
            with open(config_file, 'w') as cf:
                config.write(cf)
    else:
        # No path arg given
        # Check config file
        if config['GENERAL']['path']:
            # Use path from config
            path = config['GENERAL']['path']
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
        if config['GENERAL']['interval']:
            inter = int(config['GENERAL']['interval'])
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
    else:
        command = 'default'

    # Prep plotter
    plotter = Plotter.Plotter(inter)

    '''Commands'''

    def default():
        #  Get default stat source from config_file
        watch()

    def read():
        reader = Reader.Reader(path, f)
        print('{}: Plotting {}.'.format(__name__, f))
        plotter.plot_static(reader)

    def watch():
        #  Get miners
        miners = []
        #  First check args
        if args.miner:
            #  Look for given miner in config
            if config[args.miner]:
                #  Miner exists in config file, create instance
                new_miner = Miner.Miner(args.miner, #  Name
                                    config[args.miner]['host'],
                                    config[args.miner]['port'],
                                    Stats.Stats('Claymore json'))
                miners.append(new_miner)
                print('{}: Miner set {}'.format(__name__, str(new_miner)))
            else:
                sys.exit('Miner not in config.')
        #  Second check config
        elif int(config['GENERAL']['miners']) > 0:
            #  Get miners from config
            num_miners = int(config['GENERAL']['miners'])
            miners = []
            for each_section in config.sections():
                if each_section == 'GENERAL':
                    #  General is not a miner name, skip this section.
                    pass
                else:
                    #  For each miner section...
                    new_miner = Miner.Miner(each_section, #  Name
                                            config.get(each_section, 'host'),
                                            config.get(each_section, 'port'),
                                            Stats.Stats('Claymore json'))
                    miners.append(new_miner)
        else:
            #  No miners in config
            print('{}: Miner not set. Add one to config.'.format(__name__))

        # TODO: Validate miners, if theyre inactive remove them from the list

        watcher = Watcher.Watcher(miners)
        names = [miner.name for miner in miners]
        print('{}: Plotting {} stats every {}s.'.format(__name__, ', '.join(names), inter))
        plotter.plot_live(watcher)

    # TODO: Add a command to add a new miner to config

    command_pick = {
        'default': default,
        'read': read,
        'watch': watch
    }
    com = command_pick.get(command)
    com()
