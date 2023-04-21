# Uncomment the next two lines if you want to save the animation
#import matplotlib
#matplotlib.use("Agg")

import numpy
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation



# Sent for figure
font = {'size'   : 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
f0.suptitle("Oscillation decay", fontsize=12)
ax01 = subplot2grid((2, 2), (0, 0))
ax02 = subplot2grid((2, 2), (0, 1))
ax03 = subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
#tight_layout()

# Set titles of subplots
ax01.set_title('Position vs Time')
ax02.set_title('Velocity vs Time')
ax03.set_title('Position and Velocity vs Time')

# set y-limits
ax01.set_ylim(0,2)
ax02.set_ylim(-6,6)
ax03.set_ylim(-0,5)

# sex x-limits
ax01.set_xlim(0,5.0)
ax02.set_xlim(0,5.0)
ax03.set_xlim(0,5.0)

# Turn on grids
ax01.grid(True)
ax02.grid(True)
ax03.grid(True)

# set label names
ax01.set_xlabel("x")
ax01.set_ylabel("py")
ax02.set_xlabel("t")
ax02.set_ylabel("vy")
ax03.set_xlabel("t")
ax03.set_ylabel("py")

# Data Placeholders
# yp1=zeros(0)
yp1 = []
yv1 = []
yp2 = []
yv2 = []
t = []

# set plots
p011, = ax01.plot(t,yp1,'b-', label="yp1")
p021, = ax02.plot(t,yv1,'b-', label="yv1")
p031, = ax03.plot(t,yp1,'b-', label="yp1")

# set lagends
# ax01.legend([p011,p012], [p011.get_label(),p012.get_label()])
# ax02.legend([p021,p022], [p021.get_label(),p022.get_label()])
# ax03.legend([p031,p032], [p031.get_label(),p032.get_label()])

# Data Update
xmin = 0.0
xmax = 5.0
x = 0.0

def updateData(self):
    global x
    global yp1
    global yv1
    global yp2
    global yv2
    global t

    tmpp1 = 1 + exp(-x) *sin(2 * pi * x)
    tmpv1 = - exp(-x) * sin(2 * pi * x) + exp(-x) * cos(2 * pi * x) * 2 * pi
    yp1.append(tmpp1)
    yv1.append(tmpv1)
    yp2.append(0.5*tmpp1)
    yv2.append(0.5*tmpv1)
    t.append(x)

    x += 0.05

    yp1 = yp1[-500:]
    yv1 = yv1[-500:]
    yp2 = yp2[-500:]
    yv2 = yv2[-500:]
    t = t[-500:]


    p011.set_data(t,yp1)
    p021.set_data(t,yv1)
    p031.set_data(t,yp1)

    if x >= xmax-1.00:
        p011.axes.set_xlim(x-xmax+1.0,x+1.0)
        p021.axes.set_xlim(x-xmax+1.0,x+1.0)
        p031.axes.set_xlim(x-xmax+1.0,x+1.0)


    return p011, p021, p031

# interval: draw new frame every 'interval' ms
# frames: number of frames to draw
simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=None, interval=100, repeat=False)

# Uncomment the next line if you want to save the animation
#simulation.save(filename='sim.mp4',fps=30,dpi=300)

plt.show()
