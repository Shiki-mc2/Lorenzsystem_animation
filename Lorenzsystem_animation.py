# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cv2, sys

def f(v):
    a = np.array([0,0,0])
    a[0] = sgm*(v[1] - v[0])
    a[1] = v[0]*(rho - v[2]) - v[1]
    a[2] = v[0]*v[1] - bet*v[2]
    
    return a

startT= 0.0
endT  = startT + 15.0
dt    = 0.00005
dlt   = 0.01
fps   = 20.0
speed = 5.0
n_time= (endT - startT)*fps/speed
n_case= 2

sgm = 10
bet = 8/3
rho = 28

#OpenCV
fourcc = cv2.VideoWriter_fourcc("h","2","6","4")
video  = cv2.VideoWriter("%s_%d_%d.mp4" % (sys.argv[0][sys.argv[0].rfind("/")+1:-3], startT ,endT), fourcc, fps, (600, 600))

fig = plt.figure(figsize=(6,6),dpi=100)
plt.subplots_adjust(left=0, right=1.0, bottom=0, top=1.0)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.xlim(-25,25)
plt.ylim(  0,50)

color = [[1.0, 0.0, 0.0],
         [1.0, 0.5, 0.0],
         [0.0, 0.8, 0.0],
         [0.0, 0.8, 0.8],
         [0.0, 0.0, 1.0],
         [0.8, 0.0, 0.8]]
log_x = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

for j in range(n_case):
    c = color[j]
    plot_x = []
    plot_y = []
    plot_z = []
    v = np.array([11.0, 10.0, 33.0*(1+j*0.00001)])

    i    = 0
    t    = 0.0
    lt   = startT
    vt   = startT
    dvt  = 1.0/fps*speed

    while i <= n_time:
        t += dt
        a1 = dt*f(v)
        a2 = dt*f(v+a1*0.5)
        a3 = dt*f(v+a2*0.5)
        a4 = dt*f(v+a3)
        v = v + (a1 + 2*(a2+a3) + a4)/6
    
        if lt <= t:
            plot_x.append(v[0])
            plot_y.append(v[1])
            plot_z.append(v[2])
            lt +=dlt
            
        if vt <= t:        
            print ("j=%d t = %f, i=%d" % (j,t,i))
            if v[0] == 0 and v[2] == 0:
                print ("zero")
    
            plt.plot(plot_x, plot_z, color=color[j],  linewidth=0.5)
    
            fig.canvas.draw()
            image_array = np.array(fig.canvas.renderer._renderer)
            img = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
            video.write(img)
            plot_x = [plot_x[-1]]
            plot_y = [plot_y[-1]]
            plot_z = [plot_z[-1]]        

            vt += dvt
            i +=1
    log_x[j] = v
            
for i in range(20):
    video.write(img)
plt.savefig("%s_%d_%d.png" % (sys.argv[0][sys.argv[0].rfind("/")+1:-3],startT ,endT))
plt.close()
video.release()
