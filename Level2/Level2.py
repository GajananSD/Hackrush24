from math import sin, cos, acos, atan,sqrt,degrees
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import time

l1 = 1      # length of arm 1 (m)
l2 = 2      # length of arm 2 (m)

# let E (x,y) be end effector position

""" End effector range will be between two concentric circles with centres at origin and radius (l1 + l2) 
and radius (l1 - l2) """

""" Let the arbitarary trajectory of end effector be circle """
# Circle parameters
center = (0, 2.1)
radius = 1

# Generate points for the circle trajectory
t = linspace(0, 2*pi, 100)
x2 = center[0] + radius * cos(t)
y2 = center[1] + radius * sin(t)

for i in range(100):
    if ((x2[i]**2)+(y2[i]**2))>=(9):
        y2[i] = sqrt(9 - (x2[i])**2)

# creating array for coordinates of joint O2
x1=linspace(0,0,100)
y1=linspace(0,0,100)

x0=[0]*100       # x-coordinate of joint O1
y0=[0]*100       # y-coordinate of joint O1

# List for storing theta values
t1=[]
t2=[]

prev_theta2 = pi/2
for i in range(100):
    x=x2[i]
    y=y2[i]
    #Inverse kinematics
    theta1 =  acos( round(((x**2) + (y**2) - (l1**2) - (l2**2)) / (2 * l1 * l2),5 ))
    t1.append(degrees(theta1))
    theta2 = atan(y / x) - atan( (l2 * sin(theta1) ) / ( l1 + (l2 * cos(theta1) )))
    if prev_theta2>0 and theta2<0:
        theta2 = pi + theta2
    
    print(x,y,i,degrees(theta2))
    prev_theta2 = theta2
    t2.append(degrees(theta2))
    x1[i] = (l1 * cos(theta2))        # x-coordinate of joint O2
    y1[i] = (l1 * sin(theta2))        # y-coordinate of joint O2 


#creating figure
fig, ax = plt.subplots()
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
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

# Specify the file path
file_path = "Level2.csv"

# Write data to CSV
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['time', 'x2', 'y2'])  # Write the header
    
    start_time = time.time()  # Record the start time
    
    def animate(i):
        if i == len(x1) - 1:  # Check if it's the last frame
            ani.event_source.stop()  # Stop the animation
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        line1.set_data([x0[i], x1[i]], [y0[i], y1[i]])
        line2.set_data([x1[i], x2[i]], [y1[i], y2[i]])
        point_O1.set_data(x0[i], y0[i])
        point_O2.set_data(x1[i], y1[i])
        point_E.set_data(x2[i], y2[i])

        trace_x.append(x2[i])
        trace_y.append(y2[i])
        trace_line.set_data(trace_x, trace_y)
        
        # Write data to CSV
        writer.writerow([elapsed_time, x2[i], y2[i]])
        
        return line1, line2, point_O1, point_O2, point_E, trace_line

    ani = FuncAnimation(fig, animate, frames=len(x1), init_func=init, blit=True)
    plt.title("2R Manipulator End effector path tracing simulation.")
    plt.show()

