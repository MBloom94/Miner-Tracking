from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import dates
from matplotlib import ticker
import time
import datetime
import numpy as np


class Plotter():
    '''Plot Claymore live or log data.'''

    def __init__(self):
        '''Initialize plot artifacts.'''
        self.data_interval_ms = 1000*10  # 10 second interval.
        self.data_interval_s = self.data_interval_ms//1000  # seconds

        self.fig, self.ax_1 = plt.subplots()
        self.line, = self.ax_1.plot_date([], [], 'b-')  # 'b-' for line graph

        # Styling
        self.fig.canvas.set_window_title('Miner1 Stats')
        self.ax_1.grid(True)
        self.fig.autofmt_xdate()

    def plot_live(self, stats_source):
        '''Plot live data from Watcher object.'''

        # Specific Styling
        # Set the y axis range from 0 to 40,000 kH/s
        self.ax_1.set_ylim([0, 40000])

        def megahashes(x, pos):
            '''Provide formatting for the y axis tickers.'''
            return '{0:.0f} Mh/s'.format(x/1000)  # e.g. 26 Mh/s

        # Create formatters.
        self.ax_1.format_xdata = dates.DateFormatter('%H:%M:%S')
        x_formatter = dates.DateFormatter('%H:%M:%S')
        self.ax_1.xaxis.set_major_formatter(x_formatter)
        self.ax_1.yaxis.set_major_formatter(ticker.FuncFormatter(megahashes))

        # Define animation function
        def animate(i):
            '''Function to drive the animation to be run each interval.'''

            # Watcher get new data
            stats_source.update_stats()
            # Print new data to console
            print('{} {} Mh/s'.format(
                stats_source.hash_rates[-1][0].strftime('%H:%M:%S'),
                stats_source.hash_rates[-1][1]/1000))
            # For each hash rate in hashrates, append to x and y
            x, y = self.set_x_y(stats_source.hash_rates)
            self.line.set_data(x, y)
            # x axis ends at the most recent timestamp,
            # and starts 60*interval before that.
            self.ax_1.set_xlim(
                x[-1] - datetime.timedelta(minutes=self.data_interval_s),
                x[-1])
            return self.line,

        # Assign the animator
        anim = animation.FuncAnimation(
            self.fig, animate, frames=None,
            interval=self.data_interval_ms)

        # Show the live plot.
        plt.show()

    def plot_static(self, stats_source):
        '''Plot log data from Reader object.'''

        stats_source.read_log()
        x, y = self.set_x_y(stats_source.hash_rates)
        plt.plot_date(x, y, 'b-')

        # Specific Styling
        def megahashes(x, pos):
            '''Provide formatting for the y axis tickers.'''
            return '{0:.0f} Mh/s'.format(x)  # e.g. 26 Mh/s

        # Create formatters.
        x_formatter = dates.DateFormatter('%H:%M:%S')
        self.ax_1.xaxis.set_major_formatter(x_formatter)
        self.ax_1.yaxis.set_major_formatter(ticker.FuncFormatter(megahashes))
        self.ax_1.yaxis.set_major_locator(ticker.AutoLocator())

        plt.xlim(x[0], x[-1])
        plt.ylim(0.000, 40.000)

        plt.show()

    def set_x_y(self, stats_list):
        '''Take a list of [timestamp, stat], split it to x, y and return it.'''
        x = []
        y = []
        for h in range(len(stats_list)):
            x.append(stats_list[h][0])
            y.append(stats_list[h][1])
        return x, y


if __name__ == '__main__':
    print('Run Plotter from Main with a stats_source.')
