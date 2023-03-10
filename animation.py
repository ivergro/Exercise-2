import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation



fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))


#Gathering vector data from text file. 
#vector_data_list[line/step][vector][coordinate]
vector_data_list = []
f = open("vector_data.txt", "r")
for line in f.readlines():
    line_vec = []
    temp_string = line.strip("[ ] \n")
    temp_string = temp_string.replace("[", "")
    temp_string = temp_string.replace("]", "")
    floats = [float(x) for x in temp_string.split()]
    for i in range(len(floats)//3):
        line_vec.append(floats[i*3:i*3+3])
    vector_data_list.append(line_vec)
f.close()
vector_data_list = np.asarray(vector_data_list)
#------------------------------------

#--------Animation-------------------
def get_arrow(i, j):
    i = int(i)
    x = j
    y = 0
    z = 0
    u = vector_data_list[i][j][0]
    v = vector_data_list[i][j][1]
    w = vector_data_list[i][j][2]
    return x,y,z,u,v,w

quiver_list = []
text_list   = []
step_text   =  ax.text(0,0,4, "step: 0" + "  /  " + str(len(vector_data_list)))
for j in range(len(vector_data_list[0])):
    quiver_list.append(ax.quiver(*get_arrow(0, j)))
    text_list.append(ax.text(0.4 + j, 0.0, -0.2, str(round(1.0, 2))))

ax.set_xlim(-1, len(vector_data_list[0]))
ax.set_ylim(-1, 1)
ax.set_zlim(-2, 2)

def update(i):
    # global quiver_list
    # global text_list
    global step_text
    for j in range(len(quiver_list)):
        quiver_list[j].remove()
        text_list[j].remove()
        quiver_list[j] = ax.quiver(*get_arrow(i, j))

        #Adding length on vector to animation
        v_length = np.linalg.norm(vector_data_list[int(i)][j])
        text_list[j] = ax.text(0.4 + j, 0.0, -0.2, "l: " + str(round(v_length, 2)))
    step_text.remove()
    step_text = ax.text(0,0,4, "step: " + str(int(i)) + "  /  " + str(len(vector_data_list)))
    

 #Nå vil linspace lage masse float verdier
 #For å skippe masse verdier, kan num=len(vector_list) fjernes fra frames
ani = FuncAnimation(fig, update, frames=np.linspace(0, len(vector_data_list) - 1, num=len(vector_data_list)), interval=50)
#plt.show()

f = r"animations/Prep-2.1.2.gif" 
writergif = animation.PillowWriter(fps=30) 
ani.save(f, writer=writergif)
#-----------------------------------