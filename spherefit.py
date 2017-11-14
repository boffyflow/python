import numpy as np
import math
#	fit a sphere to X,Y, and Z data points
#	returns the radius and center points of
#	the best fit sphere
#   http://jekel.me/2015/Least-Squares-Sphere-Fit/

def sphereFit(spX,spY,spZ):
    #   Assemble the A matrix
    spX = np.array(spX)
    spY = np.array(spY)
    spZ = np.array(spZ)
    A = np.zeros((len(spX),4))
    A[:,0] = spX*2
    A[:,1] = spY*2
    A[:,2] = spZ*2
    A[:,3] = 1
    
    #   Assemble the f matrix
    f = np.zeros((len(spX),1))
    f[:,0] = (spX*spX) + (spY*spY) + (spZ*spZ)
    C, residules, rank, singval = np.linalg.lstsq(A,f)

    #   solve for the radius
    t = (C[0]*C[0])+(C[1]*C[1])+(C[2]*C[2])+C[3]
    radius = math.sqrt(t)
    
    return radius, C[0], C[1], C[2]


from matplotlib import rcParams
rcParams['font.family'] = 'serif'
#   3D plot of the 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plotSphere(px,py,pz):

    r, x0, y0, z0 = sphereFit(px,py,pz)
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x=np.cos(u)*np.sin(v)*r
    y=np.sin(u)*np.sin(v)*r
    z=np.cos(v)*r
    x = x + x0
    y = y + y0
    z = z + z0

    #   3D plot of Sphere
    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')

    ax = Axes3D(fig)

    ax.scatter( px, py, pz, zdir='z', c='b',rasterized=True)
    ax.plot_wireframe(x, y, z, color="r")
    ax.set_aspect('equal')
    ax.set_xlim3d(3, 4.5)
    ax.set_ylim3d(2.5, 4)
    ax.set_zlim3d(-0.5, 1)
    ax.set_xlabel('$x$ (mm)',fontsize=16)
    ax.set_ylabel('\n$y$ (mm)',fontsize=16)
    zlabel = ax.set_zlabel('\n$z$ (mm)',fontsize=16)
    plt.show()
    plt.savefig('steelBallFitted.pdf', format='pdf', dpi=300, bbox_extra_artists=[zlabel], bbox_inches='tight')

def main():
  
    a = np.genfromtxt('mc_sphere3.txt',unpack='True',delimiter=' ')

    r, x0, y0, z0 = sphereFit( a[0],a[1],a[2])

    print( r, x0, y0, z0)

    i = 0
    while i < len(a[0]):
        dx = a[0][i] - x0
        dy = a[1][i] - y0
        dz = a[2][i] - z0
        rp = math.sqrt(dx*dx+dy*dy+dz*dz)
        print(rp-r)
        i+=1

    plotSphere( a[0],a[1],a[2])


if __name__ == '__main__':
    main()      