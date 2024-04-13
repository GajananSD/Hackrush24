from math import sin, cos, acos, atan, degrees
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

l1 = 1      # length of arm 1 (m)
l2 = 2      # length of arm 2 (m)

# creating array for coordinates of joint O2
x1=linspace(0,0,100)
y1=linspace(0,0,100)

x0=[0]*100       # x-coordinate of joint O1 (origin)
y0=[0]*100       # y-coordinate of joint O1 

# Define starting and ending points
x_start, y_start = 3, 0
x_end, y_end = -1.75, 2

# Define constants
radius = 3
theta_end = pi/2

# Define points for the arc
theta = np.linspace(0, theta_end, 80)
x_arc = radius * np.cos(theta)
y_arc = radius * np.sin(theta)

# Define points for the line from (0,3) to (-1.75,2)
x_line = np.linspace(0, -1.75, 20)
y_line = np.linspace(3, 2, 20)

x2 = np.concatenate((x_arc,x_line))
y2 = np.concatenate((y_arc,y_line))

t1 =[pi]
t2 =[0]
prev_theta2 = 0
for i in range(1, 100):
    x=x2[i]
    y=y2[i]
    theta1 =  acos( round((x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2), 5) )
    t1.append(degrees(theta1))
    theta2 = atan(y / x) - atan( (l2 * sin(theta1) ) / ( l1 + (l2 * cos(theta1) )))
    if prev_theta2>0 and theta2<0:
        theta2 = theta2*(-1)
    print(i, degrees(theta2))
    prev_theta2 = theta2
    t2.append(degrees(theta2))
    x1[i] = (l1 * cos(theta2))        # x-coordinate of joint O2
    y1[i] = (l1 * sin(theta2))        # y-coordinate of joint O2 
    #theta2 = theta + theta1

x1[0] = 1
y1[0] = 0

#creating figure
fig, ax = plt.subplots()
ax.set_xlim(-4, 4)
ax.set_ylim(-2, 4)
ax.set_aspect('equal', adjustable='box')

# Enable grid lines
ax.grid(True)

# Initialize the plot elements
line1, = ax.plot([], [], 'b-', linewidth=2)  # Line for arm 1
line2, = ax.plot([], [], 'g-', linewidth=2)  # Line for arm 2
point_O1, = ax.plot([], [], 'ko', markersize=8)  # Joint O1
point_O2, = ax.plot([], [], 'ko', markersize=8)  # Joint O2
point_E, = ax.plot([], [], 'r*', markersize=8)   # End effector E
trace_line, = ax.plot([], [], 'k--', linewidth=1)  # Trace line

trace_x = []  # To store the traced x-coordinates
trace_y = []  # To store the traced y-coordinates

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    point_O1.set_data([], [])
    point_O2.set_data([], [])
    point_E.set_data([], [])
    trace_line.set_data([], [])
    
    return line1, line2, point_O1, point_O2, point_E, trace_line

def animate(i):
    if i == len(x1) - 1:  # Check if it's the last frame
        ani.event_source.stop()  # Stop the animation
    line1.set_data([x0[i], x1[i]], [y0[i], y1[i]])
    line2.set_data([x1[i], x2[i]], [y1[i], y2[i]])
    point_O1.set_data(x0[i], y0[i])
    point_O2.set_data(x1[i], y1[i])
    point_E.set_data(x2[i], y2[i])
    trace_x.append(x2[i])
    trace_y.append(y2[i])
    trace_line.set_data(trace_x, trace_y)
    return line1, line2, point_O1, point_O2, point_E, trace_line

# Save x1, y1, x2, y2 points into a CSV file
with open('level1.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['x1', 'y1', 'theta_1', 'x2', 'y2', 'theta_2'])
    for i in range(100):
        writer.writerow([x1[i], y1[i],t1[i], x2[i], y2[i], t2[i]])


ax.legend()  # Show legend
ani = FuncAnimation(fig, animate, frames=len(x1), init_func=init, blit=True)
# Plot the point (-1.75, 2.0)
plt.plot(-1.75, 2.0, 'ro', label='(-1.75, 2.0)')
plt.title("RoboRig Destination (-1.75, 2.0)")
plt.show()

