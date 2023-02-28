from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
line, = ax.plot([], [], lw=2)

def f(n):
    x = np.linspace(0, 2, 1000)
    y = n*x**2
    line.set_data(x, y)
    return line,

def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

#A function used to draw a clear frame
def init():
    line.set_data([], [])
    return line,

myAnimation = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

#myAnimation.save('basic_animation.mp4', fps=30)#, extra_args=['-vcodec', 'libx264'])





cone_fig = go.Figure(data=go.Cone(x=[0], y=[0], z=[0], u=[0], v=[0], w=[2], sizemode="absolute", anchor="tail", sizeref=2))

cone_fig.update_layout(scene_camera_eye=dict(x=-0.76, y=1.8, z=0.92))

#plt.show()

cone_fig.show()