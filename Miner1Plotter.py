from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.ticker import FuncFormatter
import time
import Miner1Watcher


# Set up figure, axis and plot element.
fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [], lw = 2)

# Create a new watcher.
watcher = Miner1Watcher.Watcher()

# Set watcher's stats list to the first of our list of stats.
watcher.get_new_stats()
# Set the x axis range to the previous uptime -> current uptime.
ax.set_xlim([watcher.uptime[0] - 20, watcher.uptime[0]])
# Set the y axis range from 0 to 40,000 kH/s
ax.set_ylim([0, 40000])

# Styling
fig.canvas.set_window_title('Miner1Hashrate')


def megahashes(x, pos):
    '''Provide formatting for the y axis tickers.'''
    return '{0:.3f} Mh/s'.format(x/1000)

def hours_minutes(x, pos):
    '''Provide formatting for the x axis tickers.'''
    h = str(int(x//60))
    m = str(int(x%60))
    if len(m) < 1:
        m = '0' + m
    x_hm = h + ':' + m
    return x_hm.format('{0:.0f}')
    # return '{0:.0f}:{0:.0f}'.format(x//60, x%60)
    # return x
    # return time.strftime('%H:%M', time.gmtime(x // 60))

# Create a formatters.
x_formatter = FuncFormatter(hours_minutes)
y_formatter = FuncFormatter(megahashes)
ax.xaxis.set_major_formatter(x_formatter)
ax.yaxis.set_major_formatter(y_formatter)
ax.locator_params(axis='x', nbins=10)
# Give a little space to the left wall.
fig.subplots_adjust(left = 0.16)


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
    watcher.get_new_stats(allow_dup_time = False)
    # Print formatted newest stats in console.
    watcher.print_stats_pretty()
    x = watcher.uptime  # ['minutes'] e.g. ['237']
    y = watcher.hash_rate  # ['kilohashes'] e.g. ['25000']
    line.set_data(x, y)
    # Set the x axis range to the previous uptime -> current uptime.
    ax.set_xlim([watcher.uptime[-1] - 20, watcher.uptime[-1]])
    return line,

# Animate with the animator function
anim = animation.FuncAnimation(fig, animate, frames = None,
                               init_func = init, interval = 1000, blit = True)

plt.show()
