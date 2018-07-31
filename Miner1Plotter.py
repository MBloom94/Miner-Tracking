from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import dates
# from matplotlib.ticker import FuncFormatter
from matplotlib import ticker
import time
import datetime
import Miner1Watcher


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
    return '{0:.0f} Mh/s'.format(x/1000)

# Create formatters.
ax.format_xdata = dates.DateFormatter('%H:%M:%S')
x_formatter = dates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(x_formatter)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(megahashes))


# Initialize; plot background of each frame
def init():
    '''Initializes the line.'''
    line.set_data([], [])
    return line,


# Animate; called sequentially
def animate(i):
    '''Function to drive the animation to be run each interval.'''
    # Update the stats list.
    watcher.get_new_stats()
    watcher.print_stats_pretty()
    # x = list(dates.date2num(watcher.timestamp))  # ['timestamp'] e.g. ['']
    x = watcher.timestamp  # ['timestamp'] e.g. [datetime.datetime(
                           #     2018, 7, 31, 17, 12, 27, 542521)]
    y = watcher.hash_rate  # ['kilohashes'] e.g. ['25000']
    line.set_data(x, y)
    # Set the x axis range to the previous uptime -> current uptime.
    ax.set_xlim([x[0], x[-1]])
    return line,

# Animate with the animator function
anim = animation.FuncAnimation(fig, animate, frames = None,
                               init_func = init, interval = 1000)
plt.show()
