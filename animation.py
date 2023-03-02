import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# fig = plt.figure()
# ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
# line, = ax.plot([], [], lw=2)

# def f(n):
#     x = np.linspace(0, 2, 1000)
#     y = n*x**2
#     line.set_data(x, y)
#     return line,

# def animate(i):
#     x = np.linspace(0, 2, 1000)
#     y = np.sin(2 * np.pi * (x - 0.01 * i))
#     line.set_data(x, y)
#     return line,

# #A function used to draw a clear frame
# def init():
#     line.set_data([], [])
#     return line,

# def flat_animation():
#     myAnimation = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=200, interval=20, blit=True)
#     #myAnimation.save('basic_animation.mp4', fps=30)#, extra_args=['-vcodec', 'libx264'])
    
#     plt.show()


fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))


#Gathering vector data from text file
vector_list = []
f = open("vector_data.txt", "r")
for line in f.readlines():
    temp_string = line.strip("[]\n")
    floats = [float(x) for x in temp_string.split()]
    vector_list.append(floats)
f.close()
vector_list = np.asarray(vector_list)
#------------------------------------

#--------Animation-------------------
def get_arrow(i):
    i = int(i)
    x = 0
    y = 0
    z = 0
    u = vector_list[i][0]
    v = vector_list[i][1]
    w = vector_list[i][2]
    return x,y,z,u,v,w

quiver = ax.quiver(*get_arrow(0))
text = ax.text(0.4, 0.4, -0.2, str(round(1.0, 2)))

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-2, 2)

def update(i):
    global quiver
    global text
    quiver.remove()
    text.remove()
    quiver = ax.quiver(*get_arrow(i))

    #Adding length on vector to animation
    v_length = np.linalg.norm(vector_list[int(i)])
    text = ax.text(0.4, 0.4, -0.2, "l: " + str(round(v_length, 2)))
    

ani = FuncAnimation(fig, update, frames=np.linspace(0,len(vector_list) - 1, num=len(vector_list)), interval=50) #Nå vil linspace lage masse float verdier, for å kjøre kajppere, så kan num=len(vector_list)
plt.show()
#-----------------------------------