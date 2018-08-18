from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import dates
from matplotlib import ticker
import time
import datetime


class Plotter():
    '''Plot Claymore live or log data.'''

    def __init__(self):
        '''Initialize plot artifacts.'''
        self.data_interval_ms = 1000*10  # 10 second interval.
        self.data_interval_s = self.data_interval_ms//1000  # seconds

        self.fig = plt.figure()  # Create a figure to plot onto.
        self.ax_1 = plt.axes()  # Assign an axis.
        self.line, = self.ax_1.plot_date([], [], 'b-')  # 'b-' for line graph

        # Styling
        # Set the y axis range from 0 to 40,000 kH/s
        self.ax_1.set_ylim([0, 40000])
        # self.ax_1.set_ylim([0, 30000])
        self.fig.canvas.set_window_title('Miner1 Stats')
        self.ax_1.grid(True)
        self.fig.autofmt_xdate()

        def megahashes(x, pos):
            '''Provide formatting for the y axis tickers.'''
            return '{0:.0f} Mh/s'.format(x/1000)  # e.g. 26 Mh/s

        # Create formatters.
        self.ax_1.format_xdata = dates.DateFormatter('%H:%M:%S')
        x_formatter = dates.DateFormatter('%H:%M:%S')
        self.ax_1.xaxis.set_major_formatter(x_formatter)
        self.ax_1.yaxis.set_major_formatter(ticker.FuncFormatter(megahashes))

    def plot_live(self, stats_source):
        '''Plot live data from Watcher object.'''

        # Define animation function
        def animate(i):
            '''Function to drive the animation to be run each interval.'''
            # Update the stats list.
            x = []
            y = []
            # Watcher get new data
            stats_source.update_stats()
            # Print new data to console
            print('{} {} Mh/s'.format(
                stats_source.hash_rates[-1][0].strftime('%H:%M:%S'),
                stats_source.hash_rates[-1][1]/1000))
            # For each hash rate in hashrates, append to x and y
            for h in range(len(stats_source.hash_rates)):
                x.append(stats_source.hash_rates[h][0])
                y.append(stats_source.hash_rates[h][1])
            self.line.set_data(x, y)
            # x axis ends at the most recent timestamp,
            # and starts 60*interval before that.
            self.ax_1.set_xlim(x[-1]
                - datetime.timedelta(minutes=self.data_interval_s), x[-1])
            return self.line,

        # Assign the animator
        anim = animation.FuncAnimation(self.fig, animate, frames=None,
            interval=self.data_interval_ms)

        # Show the live plot.
        plt.show()


if __name__ == '__main__':
    pass
