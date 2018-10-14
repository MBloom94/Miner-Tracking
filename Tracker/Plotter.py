from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import dates
from matplotlib import ticker
from matplotlib import patches as mpatches
import time
import datetime



class Plotter():
    '''Plot Claymore live or log data.'''

    def __init__(self, interval=None):
        '''Initialize plot artifacts.'''

        if interval is None:
            self.data_interval_s = 60  # Default interval
            self.data_interval_ms = 1000 * self.data_interval_s
        else:
            self.data_interval_s = interval  # Seconds
            self.data_interval_ms = 1000 * interval  # Param: interval

        self.fig = plt.figure()
        self.ax_1 = plt.axes()
        self.line, = self.ax_1.plot_date([], [], 'b-')  # 'b-' for line graph

        # Styling
        self.fig.canvas.set_window_title('Miner Stats')
        self.ax_1.grid(True)
        self.fig.autofmt_xdate()
        # TODO: implement calc_y_range
        # Set the y axis range from 0 to 100,000 kH/s
        self.ax_1.set_ylim([0, 100000])
        # Legend
        green_patch = mpatches.Patch(color='green',
                                     label='Reported Hashrate')
        blue_patch = mpatches.Patch(color='blue',
                                    label='Effective Hashrate')
        orange_patch = mpatches.Patch(color='orange',
                                      label='Avg Effective Hashrate')
        plt.legend(handles=[green_patch,
                            blue_patch,
                            orange_patch])

    def plot_live(self, stats_source):
        '''Plot live data from Watcher object.'''

        self.lines = [self.ax_1.plot_date([], [], 'b-', color='green')[0],
                      self.ax_1.plot_date([], [], 'b-', color='blue')[0],
                      self.ax_1.plot_date([], [], 'b-', color='orange')[0]]

        # Specific Styling

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
            stats_source.update_stats()
            # Print new data to console
            print('{}: {} {:.3f} Mh/s, {:.3f} Eff Mh/s'.format(
                __name__,
                stats_source.timestamps[-1][0].strftime('%H:%M:%S'),
                stats_source.hash_rates[-1][1]/1000,
                stats_source.ehrs[-1][1]/1000))

            # For each hash rate in hashrates, append to x and y
            x1, y1 = self.set_x_y(stats_source.hash_rates)
            x2, y2 = self.set_x_y(stats_source.ehrs)
            x3, y3 = self.set_x_y(stats_source.avgs)

            xlist = [x1, x2, x3]
            ylist = [y1, y2, y3]

            # Set line data, will handle more axes
            for lnum, line in enumerate(self.lines):
                line.set_data(xlist[lnum], ylist[lnum])

            # TODO: Only update range if the range is the same as it was last
            # animation tick. This is annoying when you are trying to explore
            # data and it jumps back to the live frame. Should be able to use
            # self.ax_1.get_xlim() and self.ax_1.get_ylim() to check location.
            start, end = self.calc_x_range(x1)
            self.ax_1.set_xlim(start, end)
            # TODO: Actually implement calc_y_range
            start, end = self.calc_y_range(y1)
            self.ax_1.set_ylim(start, end)
            return self.lines,

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
        plt.plot_date(x, y, 'b-', color='green')

        x2, y2 = self.set_x_y(stats_source.ehrs)
        plt.plot_date(x2, y2, 'b-', color='blue')

        x3, y3 = self.set_x_y(stats_source.avgs)
        plt.plot_date(x3, y3, 'b-', color='orange')

        # Specific Styling
        def megahashes(x, pos):
            '''Provide formatting for the y axis tickers.'''
            return '{0:.0f} Mh/s'.format(x/1000)  # e.g. 26 Mh/s

        # Create formatters.
        x_formatter = dates.DateFormatter('%a %d %H:%M')  # Sun 02 10:00
        self.ax_1.xaxis.set_major_formatter(x_formatter)
        self.ax_1.yaxis.set_major_formatter(ticker.FuncFormatter(megahashes))
        self.ax_1.yaxis.set_major_locator(ticker.AutoLocator())

        plt.xlim(x[0], x[-1])
        # TODO: Implement calc_y_range
        # plt.ylim(0, 40000)

        print('{}: Showing plot.'.format(__name__))
        plt.show()

    def set_x_y(self, stats_list):
        '''Take a list of [timestamp, stat], split it to x, y and return it.'''
        x = []
        y = []
        for h in range(len(stats_list)):
            x.append(stats_list[h][0])
            y.append(stats_list[h][1])
        return x, y

    def calc_x_range(self, times):
        '''Return the starting and ending points for the x1 range.'''
        start = None
        end = times[-1]  # Current data point
        delta = times[-1] - times[0]
        # Minimum range is ten minutes
        if delta < datetime.timedelta(minutes=10):
            start = times[-1] - datetime.timedelta(minutes=10)
        # Next range is 1 hour
        elif delta < datetime.timedelta(hours=1):
            start = times[-1] - datetime.timedelta(hours=1)
        # Next range is six hours
        elif delta < datetime.timedelta(hours=6):
            start = times[-1] - datetime.timedelta(hours=6)
        elif delta < datetime.timedelta(hours=12):
            start = times[-1] - datetime.timedelta(hours=12)
        # Max range is 24 hours
        else:
            start = times[-1] - datetime.timedelta(hours=24)

        return start, end

    def calc_y_range(self, rates):
        '''Return start and end data points for the y range'''
        start = 0
        end = None
        max = 0
        # Get max value from times
        for rate in rates:
            if rate > max:
                max = rate
        # Set end max(times) * 2
        end = max * 2

        return start, end



if __name__ == '__main__':
    print('{}: Run Plotter from Main with a stats_source.'.format(__name__))
