import argparse
import configparser
import os
import sys
import Stats
import Reader
import Watcher
import Plotter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--live',
                        help=("Plot live data. By default uses Watcher with "
                              "default interval. Aditionally use -r / --read_log "
                              "to use Reader."),
                        action='store_true')
    parser.add_argument('-r', '--read_log',
                        help=("If --live is set, --read_log will cause Reader to "
                              "be used instead of Watcher to plot log data and "
                              "then continue plotting live data."),
                        action='store_true')
    parser.add_argument('-p', '--path', help='Path to file\'s directory.')
    parser.add_argument('-f', '--file', help='File name.')
    parser.add_argument('-i', '--interval', help='Stats interval in seconds.',
                        type=int)
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_file)

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

    if args.interval:
        inter = args.interval
        print('{}: Interval set {}s'.format(__name__, inter))
    else:
        if config['DEFAULT']['interval']:
            inter = int(config['DEFAULT']['interval'])
        else:
            inter = 60

    plotter = Plotter.Plotter(inter)
    # Set default plotter range

    # Plot Static or Live
    if args.live:
        if args.read_log:
            reader = Reader.Reader(path, f)
            print('{}: Plotting live stats with log every {}s.'.format(__name__, inter))
            plotter.plot_live(reader)
        else:
            watcher = Watcher.Watcher()
            print('{}: Plotting live stats every {}s.'.format(__name__, inter))
            plotter.plot_live(watcher)
    else:
        reader = Reader.Reader(path, f)
        print('{}: Plotting {}.'.format(__name__, f))
        plotter.plot_static(reader)
