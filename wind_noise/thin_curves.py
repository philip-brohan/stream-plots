#!/usr/bin/env python
# Wind vector plot - for custom wind field.
# Plots anti-aliased vectors rather than advecting points.
# Thins the vectors according to wind speed.

import os
import sys
import iris
import iris.coords
import iris.coord_systems
import iris.fileformats
import iris.util
import numpy as np
import PIL.Image
from aggdraw import Draw, Pen, Path
from scipy.stats.qmc import PoissonDisk

plot_width=10000
plot_height=5000
iterations=1000
epsilon=0.05
poisson_radius = 0.005
pen = []
for width in range(1,20):
    pen.append(Pen("red",21-width))
bgcol = (225,225,225)
penb = Pen(bgcol,20)
data_resolution=0.2

# COP colour scheme
COP_white = (1.0, 1.0, 1.0)
COP_blue = (55 / 255, 52 / 255, 139 / 255)
COP_green = (140 / 255, 219 / 255, 114 / 255)

def plot_cube(resolution, xmin=-180, xmax=180, ymin=-90, ymax=90):
    cs = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
    lat_values = np.flip(np.arange(ymin, ymax + resolution, resolution))
    latitude = iris.coords.DimCoord(
        lat_values, standard_name="latitude", units="degrees_north", coord_system=cs
    )
    lon_values = np.arange(xmin, xmax + resolution, resolution)
    longitude = iris.coords.DimCoord(
        lon_values, standard_name="longitude", units="degrees_east", coord_system=cs
    )
    dummy_data = np.zeros((len(lat_values), len(lon_values)))
    plot_cube = iris.cube.Cube(
        dummy_data, dim_coords_and_dims=[(latitude, 0), (longitude, 1)]
    )
    return plot_cube


u10m = plot_cube(data_resolution)
v10m = u10m.copy()

def get_bezier_coef(points):
    # since the formulas work given that we have n+1 points
    # then n must be this:
    n = len(points) - 1
    # build coefficents matrix
    C = 4 * np.identity(n)
    np.fill_diagonal(C[1:], 1)
    np.fill_diagonal(C[:, 1:], 1)
    C[0, 0] = 2
    C[n - 1, n - 1] = 7
    C[n - 1, n - 2] = 2
    # build points vector
    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
    P[0] = points[0] + 2 * points[1]
    P[n - 1] = 8 * points[n - 1] + points[n]
    # solve system, find a & b
    A = np.linalg.solve(C, P)
    B = [0] * n
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2
    return A, B


# Add a cyclone (circular wind field)
def add_cyclone(u,v,x,y,strength=10,decay=0.1):
    lats = u.coord('latitude').points
    lons = v.coord('longitude').points
    lons_g,lats_g = np.meshgrid(lons,lats)
    rsq = (lons_g-x)**2+(lats_g-y)**2
    rsq[rsq<1]=1
    tx = 1*(lats_g-y)/rsq
    ty = 1*(lons_g-x)/rsq
    speed = strength/(1.0+rsq*decay)
    u.data += speed*tx
    v.data += speed*ty
    return (u,v)

#for cyclone in [
    #[180,100,20,0.0001],
    #[90,45,100,0.0001]
    #[0,0,100,0.0001]
#]:
for ci in range(100):
    x = np.random.random()*360-180
    y = np.random.random()*180-90
    speed = (np.random.random()*200-100)*(x+180)/360
    cyclone = [x,y,speed,0.0001,]
    u10m,v10m = add_cyclone(u10m,v10m,cyclone[0],cyclone[1],strength=cyclone[2],decay=cyclone[3])
u10m.data += 5

# Generate a set of origin points for the wind vectors
opx = []
opy = []
for i in range(-180, 180, 5):
    for j in range(-90, 90, 5):
        opx.append(i)
        opy.append(j)
engine=PoissonDisk(d=2,radius=poisson_radius)
sample=engine.fill_space()
sample = sample*360-180
sample = sample[(sample[:,1]>-90) & (sample[:,1]<90)]
sample = sample[(sample[:,0]<-170)]
opx = sample[:,0]
opy = sample[:,1]

# Each point in this field has an index location (i,j)
#  and a real (x,y) position
xc = u10m.coords()[1].points
xmin = np.min(xc)
xmax = np.max(xc)
dwidth = len(xc)
yc = u10m.coords()[0].points
ymin = np.min(yc)
ymax = np.max(yc)
dheight = len(yc)
# Convert between index and real positions
def x_to_i(x,width):
    return np.minimum(
        width - 1, np.maximum(0, np.floor((x - xmin) / (xmax - xmin) * (width - 1)))
    ).astype(int)
def y_to_j(y,height):
    return np.minimum(
        height - 1,
        np.maximum(0, np.floor((y - ymin) / (ymax - ymin) * (height - 1))),
    ).astype(int)


# Propagate the origin points with the wind
def wind_vectors(
    uw, vw, opx, opy,iterations=5, epsilon=1
):
    op = np.empty((len(opx),2,iterations+1))
    op[:,0,0] = opx
    op[:,1,0] = opy
    # Repeatedly make a new set of x,y points by moving the previous set with the wind
    for k in range(iterations):
        i = x_to_i(op[:,0,k],dwidth)
        j = y_to_j(op[:,1,k],dheight)
        op[:,0,k+1] = op[:,0,k]+epsilon * uw.data[j, i]
        op[:,0,k+1][op[:,0,k+1] > xmax] = xmax
        op[:,0,k+1][op[:,0,k+1] < xmin] = xmin
        op[:,1,k+1] = op[:,1,k]+epsilon * vw.data[j, i]
        op[:,1,k+1][op[:,1,k+1] > ymax] = ymax
        op[:,1,k+1][op[:,1,k+1] < ymin] = ymin
    return op

line_points = wind_vectors(
    u10m,
    v10m,
    opx,
    opy,
    epsilon=epsilon,
    iterations=iterations,
)
#print(line_points[100,:,:])
#sys.exit(0)

def render_lines(img,op,pen,penb=None):
    draw = Draw(img)

    lp = np.empty(((iterations+1),2)) 
    for line in range(op.shape[0]):
        lp[:,0] = x_to_i(op[line,0,:],plot_width)
        lp[:,1] = y_to_j(op[line,1,:],plot_height)
        (x,y) = get_bezier_coef(lp)
        cp = Path()
        cp.moveto(lp[0,0],lp[0,1])
        for segment in range(iterations):
            cp.curveto(x[segment,0],x[segment,1],y[segment][0],y[segment][1],lp[segment+1,0],lp[segment+1,1])
        xs = np.diff(lp[:,0])
        ys = np.diff(lp[:,1])
        ss = np.sqrt(xs**2+ys**2)
        sm = np.mean(ss)
        pi = int(min(len(pen)-1,len(pen)*sm*500/plot_width))
        if penb is not None:
            draw.line(cp,penb)
        draw.line(cp, pen[pi])
    return draw

img = PIL.Image.new(mode='RGB',size=(plot_width,plot_height),color=bgcol)
result = render_lines(img,line_points,pen,penb=None)
result.flush()

img.save("thin_curves.png")
