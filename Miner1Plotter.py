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
        self.data_interval_ms = 1000*8  # 8 second interval.
        self.data_interval_s = data_interval_ms//1000  # seconds

        self.fig = plt.figure()  # Create a figure to plot onto.
        self.ax_1 = plt.axes()  # Assign an axis.
        self.line, = ax_1.plot_date([], [], 'b-')  # 'b-' for line graph

        # Styling
        # Set the y axis range from 0 to 40,000 kH/s
        # ax.set_ylim([0, 40000])
        self.ax_1.set_ylim([0, 30000])
        self.fig.canvas.set_window_title('Miner1Hashrate')
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
