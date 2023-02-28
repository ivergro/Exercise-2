from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import Magnet

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

def flat_animation():
    myAnimation = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)
    #myAnimation.save('basic_animation.mp4', fps=30)#, extra_args=['-vcodec', 'libx264'])
    
    plt.show()

def one_cone():
    cone_fig = go.Figure(data=go.Cone(x=[0], y=[0], z=[0], u=[0], v=[0], w=[2], sizemode="absolute", anchor="tail", sizeref=2))
    cone_fig.update_layout(scene_camera_eye=dict(x=-0.76, y=1.8, z=0.92))
    cone_fig.show()

def multiple_cones():
    mag_list = []
    for i in range(3):
        mag_list.append(Magnet.Magnet(np.random.normal(0, 1, 3), [i,0,0]))

    fig = go.Figure(data=go.Cone(x=[mag_list[0].pos[0], mag_list[1].pos[0], mag_list[2].pos[0]], 
                                y=[mag_list[0].pos[1], mag_list[1].pos[1], mag_list[2].pos[1]], 
                                z=[mag_list[0].pos[2], mag_list[1].pos[2], mag_list[2].pos[2]], 
                                u=[mag_list[0].vector[0], mag_list[1].vector[0], mag_list[2].vector[0]], 
                                v=[mag_list[0].vector[1], mag_list[1].vector[1], mag_list[2].vector[1]], 
                                w=[mag_list[0].vector[2], mag_list[1].vector[2], mag_list[2].vector[2]], 
                                sizemode="absolute", anchor="tail", sizeref=2))
    fig.update_layout(scene_camera_eye=dict(x=-0.76, y=1.8, z=0.92))
    fig.update_traces(title_value = mag_list[0].pos, title_position = "bottom left", selector=dict(type='pie'))
    fig.show()
