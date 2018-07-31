from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import dates
from matplotlib.ticker import FuncFormatter
import time
import datetime
import Miner1Watcher


# Set up figure, axis and plot element.
fig = plt.figure()
ax = plt.axes()
# line, = ax.plot_date([], [], lw = 2)
line, = ax.plot_date([], [], 'b-')

# Create a new watcher.
watcher = Miner1Watcher.Watcher()

# Set watcher's stats list to the first of our list of stats.
# watcher.get_new_stats()

# Set the y axis range from 0 to 40,000 kH/s
# ax.set_ylim([0, 40000])
ax.set_ylim([0, 30000])

# Styling
fig.canvas.set_window_title('Miner1Hashrate')


def megahashes(x, pos):
    '''Provide formatting for the y axis tickers.'''
    return '{0:.0f} Mh/s'.format(x/1000)

# Create formatters.
# x_formatter = dates.DateFormatter('%H:%M:%S')
# ax.xaxis.set_major_formatter(x_formatter)
y_formatter = FuncFormatter(megahashes)
ax.yaxis.set_major_formatter(y_formatter)
# ax.locator_params(axis='x', nbins=10)


# Initialize; plot background of each frame
def init():
    '''Initializes the line so that we can skip over it with blit.'''
    line.set_data([], [])
    return line,


# Animate; called sequentially
def animate(i):
    '''Function to drive the animation to be run each interval.'''
    # Update the stats list, allowing duplicate timestaps in minutes
    #    by default only appends new stats when stats[0][0] != stats[1][0]
    watcher.get_new_stats()
    watcher.print_stats_pretty()
    x = list(dates.date2num(watcher.timestamp))  # ['timestamp'] e.g. ['']
    # x = [dates.date2num()]
    y = watcher.hash_rate  # ['kilohashes'] e.g. ['25000']
    line.set_data(x, y)
    # Set the x axis range to the previous uptime -> current uptime.
    ax.set_xlim([x[0], x[-1]])
    return line,

# Animate with the animator function
anim = animation.FuncAnimation(fig, animate, frames = None,
                               init_func = init, interval = 1000, blit = True)

plt.show()
