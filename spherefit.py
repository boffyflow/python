import numpy as np
import math
import argparse

#	fit a sphere to X,Y, and Z data points
#	returns the radius and center points of
#	the best fit sphere
#   http://jekel.me/2015/Least-Squares-Sphere-Fit/

def sphereFit(spX, spY, spZ):
    #   Assemble the A matrix
    spX = np.array(spX)
    spY = np.array(spY)
    spZ = np.array(spZ)
    A = np.zeros((len(spX), 4))
    A[:, 0] = spX*2
    A[:, 1] = spY*2
    A[:, 2] = spZ*2
    A[:, 3] = 1

    #   Assemble the f matrix
    f = np.zeros((len(spX), 1))
    f[:, 0] = (spX*spX) + (spY*spY) + (spZ*spZ)
    C, residules, rank, singval = np.linalg.lstsq(A, f)

    #   solve for the radius
    t = (C[0]*C[0])+(C[1]*C[1])+(C[2]*C[2])+C[3]
    radius = math.sqrt(t)

    return radius, C[0], C[1], C[2]


from matplotlib import rcParams
rcParams['font.family'] = 'serif'
#   3D plot of the sphere
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
    ax = Axes3D(fig)
    ax.scatter( px, py, pz, zdir='z', c='b',rasterized=True)
    ax.plot_wireframe(x, y, z, color="r")
    ax.set_aspect('equal')

    maxrange = max( max(px) - min(px), max(py) - min(py), max(pz) - min(pz)) + 0.5
    ax.set_xlim3d( min(px) - 0.5, min(px) + maxrange)
    ax.set_ylim3d( min(py) - 0.5, min(py) + maxrange)
    ax.set_zlim3d( min(pz) - 1.0, min(pz) + maxrange - 0.5)  # make fitted sphere stay in the positive quadrant

    ax.set_xlabel('$x$ (mm)',fontsize=16)
    ax.set_ylabel('\n$y$ (mm)',fontsize=16)
    zlabel = ax.set_zlabel('\n$z$ (mm)',fontsize=16)
    plt.show()
#    plt.savefig('FittedSphere.pdf', format='pdf', dpi=300, bbox_extra_artists=[zlabel], bbox_inches='tight')

def remove_outliers(px, py, pz):

    r,x0,y0,z0 = sphereFit(px,py,pz)

    errors = []
    i = 0
    while i < len(px):
        dx = px[i] - x0
        dy = py[i] - y0
        dz = pz[i] - z0
        rp = math.sqrt(dx*dx+dy*dy+dz*dz)
        errors.append(rp-r)
        i+=1

    sigma = np.std(errors)
    ave = np.mean(errors)
    print( 'average: %.5f' % ave)
    print( 'stdev: %.5f' % sigma)

    x = []
    y = []
    z = []

    i = 0
    while i < len(errors):
        if( abs(errors[i]) < (3 * sigma)):
            x.append( px[i])
            y.append( py[i])
            z.append( pz[i])
        i+=1

    print( 'number of original points: %d' % len(errors))
    print( 'number of clean points: %d' % len(x))
    print( 'removed %d points (or %.2f percent)' % (len(errors)-len(x), 100 * (len(errors) - len(x)) / len(errors) ) )

    return x,y,z


def parse_args():

    parser = argparse.ArgumentParser(description='Simple Sphere Fitting')

    parser.add_argument('-i','--input',required=True,help='Name of the text file containing the 3D points in XYZ (required)')
    parser.add_argument('-o','--output',default='results.txt',required=False,help='Name of the file containing results (default: results.txt)')
    parser.add_argument('-d','--delimiter',default='space',choices=['space','comma'],required=False,help='Character that separates XYZ in the input file (default: space)')
    parser.add_argument('-p','--plot',default='false',choices=['true','false'],required=False,help='Create a plot of the sphere (default: false)')

    return parser.parse_args()


def main():
  
    args = parse_args()
    fp = open( args.output, "w")

    sep = " " if (args.delimiter == 'space') else ','
    a = np.genfromtxt( args.input,unpack='True',delimiter=sep)

    x, y, z = remove_outliers( a[0],a[1],a[2])
    r, x0, y0, z0 = sphereFit(x,y,z)

    fp.write('Number of points: %d\n' % len(x))
    print('Number of points: %d' % len(x))
    fp.write('Radius,X0,Y0,Z0\n')
    print('Radius,X0,Y0,Z0')
    fp.write('%.5f,%.5f,%.5f,%.5f\n' % (r, x0, y0, z0))
    print('%.5f,%.5f,%.5f,%.5f' % (r, x0, y0, z0))

    i = 0
    errors = []

    while i < len(x):
        dx = x[i] - x0
        dy = y[i] - y0
        dz = z[i] - z0
        rp = math.sqrt(dx*dx+dy*dy+dz*dz)
        errors.append(rp-r)
        i+=1

    fp.write('Errors:\nmin,max,range,stdev\n')
    print('Errors:')
    print('min,max,range,stdev')
    fp.write('%.5f,%.5f,%.5f,%.5f\n' % (min(errors),max(errors),max(errors)-min(errors),np.std(errors)))
    print('%.5f,%.5f,%.5f,%.5f' % (min(errors),max(errors),max(errors)-min(errors),np.std(errors)))

    if args.plot == 'true':
        plotSphere( x,y,z)

    fp.close()


if __name__ == '__main__':
    main()      