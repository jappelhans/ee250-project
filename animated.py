# Uncomment the next two lines if you want to save the animation
#import matplotlib
#matplotlib.use("Agg")

import numpy
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import random



# Sent for figure
font = {'size'   : 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
# fig = figure(num = 0, figsize = (5, 5))#, dpi = 100)
fig = figure()
fig.suptitle("Sensor Monitoring Plots", fontsize=12)
ax01 = subplot2grid((2, 2), (0, 0))
ax02 = subplot2grid((2, 2), (0, 1))
# ax03 = subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
ax03 = subplot2grid((2, 2), (1, 0))
ax04 = subplot2grid((2,2), (1, 1))
tight_layout()

# Set titles of subplots
ax01.set_title('Light Measurements')
ax02.set_title('Sound Measurements')
ax03.set_title('Rangefinder Measurements')
ax04.set_title('Alarm Status')

# set y-limits
ax01.set_ylim(0,2)
ax02.set_ylim(-6,6)
ax03.set_ylim(-0,5)
ax04.set_ylim(-1,2)

# sex x-limits
ax01.set_xlim(0,5.0)
ax02.set_xlim(0,5.0)
ax03.set_xlim(0,5.0)
ax04.set_xlim(0,5.0)

# Turn on grids
ax01.grid(True)
ax02.grid(True)
ax03.grid(True)
ax04.grid(True)

# set label names
ax01.set_xlabel("time")
ax01.set_ylabel("Light Intensity")
ax02.set_xlabel("time")
ax02.set_ylabel("Sound Intensity")
ax03.set_xlabel("time")
ax03.set_ylabel("Distance")
ax04.set_xlabel("time")
ax04.set_ylabel("Status (On/Off)")

# Data Placeholders
light_data = []
sound_data = []
range_data = []
alarm_data = []
t = []
light_thresh = []
sound_thresh = []
range_thresh = []

# set plots
light_plot, = ax01.plot(t,light_data,'b-', label="light data")
light_thresh_plot, = ax01.plot(t,light_thresh,'r-', label="light threshold")

sound_plot, = ax02.plot(t,sound_data,'b-', label="sound data")
sound_thresh_plot, = ax02.plot(t,sound_thresh, '-r', label="sound threshold")

range_plot, = ax03.plot(t,range_data,'b-', label="range data")
range_thresh_plot, = ax03.plot(t,range_thresh, '-r', label="range threshold")

alarm_plot, = ax04.plot(t,alarm_data,'b-', label="alarm data")

# set legends
ax01.legend([light_plot,light_thresh_plot], [light_plot.get_label(),light_thresh_plot.get_label()])
ax02.legend([sound_plot,sound_thresh_plot], [sound_plot.get_label(),sound_thresh_plot.get_label()])
ax03.legend([range_plot,range_thresh_plot], [range_plot.get_label(),range_thresh_plot.get_label()])

# Data Update
xmin = 0.0
xmax = 5.0
x = 0.0

def updateData(self):
    global x
    global light_data
    global light_thresh
    global sound_data
    global sound_thresh
    global range_data
    global range_thresh
    global alarm_data
    global t

    # tmpp1 = 1 + exp(-x) *sin(2 * pi * x)
    # tmpv1 = - exp(-x) * sin(2 * pi * x) + exp(-x) * cos(2 * pi * x) * 2 * pi
    temp1 = random.random()
    temp2 = random.random()

    light_data.append(temp1)
    sound_data.append(temp2)
    range_data.append(0.5*temp1)
    alarm_data.append(0.5*temp2)
    t.append(x)
    light_thresh.append(1.5)
    sound_thresh.append(1.5)
    range_thresh.append(1.5)

    x += 0.05

    light_data = light_data[-500:]
    sound_data = sound_data[-500:]
    range_data = range_data[-500:]
    t = t[-500:]
    light_thresh = light_thresh[-500:]
    sound_thresh = sound_thresh[-500:]
    range_thresh = range_thresh[-500:]


    light_plot.set_data(t,light_data)
    light_thresh_plot.set_data(t,light_thresh)
    sound_plot.set_data(t,sound_data)
    sound_thresh_plot.set_data(t, sound_thresh)
    range_plot.set_data(t,range_data)
    range_thresh_plot.set_data(t, range_thresh)
    alarm_plot.set_data(t,alarm_data)

    if x >= xmax-1.00:
        light_plot.axes.set_xlim(x-xmax+1.0,x+1.0)
        sound_plot.axes.set_xlim(x-xmax+1.0,x+1.0)
        range_plot.axes.set_xlim(x-xmax+1.0,x+1.0)
        alarm_plot.axes.set_xlim(x-xmax+1.0,x+1.0)


    return light_plot, light_thresh_plot, sound_plot, sound_thresh_plot, range_plot, range_thresh_plot, alarm_plot

# interval: draw new frame every 'interval' ms
# frames: number of frames to draw
simulation = animation.FuncAnimation(fig, updateData, blit=False, frames=None, interval=1000, repeat=False)

# Uncomment the next line if you want to save the animation
#simulation.save(filename='sim.mp4',fps=30,dpi=300)

plt.show()
