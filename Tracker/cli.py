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
        print(__name__, 'Path set {}'.format(path))
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
        print(__name__, 'File set {}'.format(f))
    else:
        # Get most recent log in path.
        # Iterate files in order and the last one stays assigned to f
        try:
            for file in os.listdir(path):
                if file.endswith('_log.txt'):
                    f = file
        except FileNotFoundError as exc:
            print(__name__, 'File or direcory not found with path. Try using --path.')
            sys.exit('Path attempted: \n    {}'.format(path))

    if args.interval:
        inter = args.interval
        print(__name__, 'Interval set {}s'.format(inter))
    else:
        if config['DEFAULT']['interval']:
            inter = int(config['DEFAULT']['interval'])
        else:
            inter = 60

    plotter = Plotter.Plotter(inter)
    reader = Reader.Reader(path, f)

    # Plot Static or Live
    if args.live:
        if args.read_log:
            print(__name__, 'Plotting past and live stats with Reader.')
            plotter.plot_live(reader)
        else:
            print(__name__, 'Plotting live stats with Watcher every {}s.'.format(inter))
            watcher = Watcher.Watcher()
            plotter.plot_live(watcher)
    else:
        print(__name__, 'Plotting {} with Reader.'.format(f))
        plotter.plot_static(reader)
