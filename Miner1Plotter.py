from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import dates
from matplotlib import ticker
import time
import datetime
import Miner1Watcher


# Set data interval. How often new stats are collected and animated.
data_interval_ms = 1000*60  # 60 second interval. Attempting hour long graph...
# data_interval_ms = 1000  # milliseconds. Should always be a multiple of 1000.
data_interval_s = data_interval_ms//1000  # seconds

# Set up figure, axis and plot element.
fig = plt.figure()
ax = plt.axes()
line, = ax.plot_date([], [], 'b-')  # 'b-' is a standard line graph.

# Create a new watcher.
watcher = Miner1Watcher.Watcher()

# Styling
# Set the y axis range from 0 to 40,000 kH/s
# ax.set_ylim([0, 40000])
ax.set_ylim([0, 30000])
fig.canvas.set_window_title('Miner1Hashrate')
ax.grid(True)
fig.autofmt_xdate()


def megahashes(x, pos):
    '''Provide formatting for the y axis tickers.'''
    return '{0:.0f} Mh/s'.format(x/1000)  # e.g. 26 Mh/s


# Create formatters.
ax.format_xdata = dates.DateFormatter('%H:%M:%S')
x_formatter = dates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(x_formatter)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(megahashes))


# Initialize; plot background of each frame
def init():
    '''Initializes the line for FuncAnimation.'''
    line.set_data([], [])
    return line,


# Animate; called sequentially
def animate(i):
    '''Function to drive the animation to be run each interval.'''
    # Update the stats list.
    watcher.get_new_stat()
    watcher.print_stats_pretty()
    x = watcher.timestamp  # ['timestamp'] e.g. [datetime.datetime()]
    y = watcher.hash_rate  # ['kilohashes'] e.g. ['25000']
    line.set_data(x, y)
    # x axis ends at the most recent timestamp,
    # and starts 60*interval before that.
    # e.g. if the interval is 1 second, the range will be 1 minute.
    #      if the interval is 4 seconds, the range will be 4 minutes.
    #      if the interval is 60 seconds, the range will be 60 minutes.
    ax.set_xlim(x[-1] - datetime.timedelta(minutes=data_interval_s), x[-1])
    return line,


# Animate with the animator function
anim = animation.FuncAnimation(fig, animate, frames=None, init_func=init,
                               interval=data_interval_ms)
plt.show()
