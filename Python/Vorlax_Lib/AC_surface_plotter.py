import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d
from mayavi import mlab
#import Aircraft_state_module.Aircraft_state as ACS

class AC_surface_plotter(object):
    def __init__(self, Aircraft_state_obj = None):
        self.figureNum = 1
        self.figure = plt.figure()
        self.ACS = None
        try: 
            self.attach(Aircraft_state_obj)
        except AttributeError:
            print('ERROR: AIRCRAFT STATE ALREADY ATTACHED IN AC_SURFACE_PLOTTER')
    def attach(self, Aircraft_state_obj):
        if self.ACS != None:
            raise AttributeError
            return
        self.ACS = Aircraft_state_obj
    def plot_single_panel_2D(self, panel_num):
        panel = self.ACS.Panel_array[panel_num]
        self.plot_2D_panel(panel)
    def plot_panels_2D(self, panel_end, panel_start = 0):
        panels = self.ACS.Panel_array[panel_start:panel_end]
        for panel in panels:
            self.plot_2D_panel(panel)
    def plot_all_panels_2D(self):
        for panel in self.ACS.Panel_array:
            self.plot_2D_panel(panel)
    def plot_2D_panel(self, panel):
        x = []
        y = []
        z = []
        temp_x = []
        temp_y = []
        temp_z = []
        temp_s = []
        s = []
        mesh_array = []
        for NVOR in panel.NVOR_array:
            for RNCV in NVOR.RNCV_array:
                temp_x.append(RNCV.X)
                temp_y.append(RNCV.Y)
                temp_z.append(RNCV.Z)
                temp_s.append(RNCV.Gamma)
            x.append(temp_x)
            y.append(temp_y)
            z.append(temp_z)
            s.append(temp_s)
            temp_x = []
            temp_y = []
            temp_z = []
            temp_s = []

        #for point in range(0,len(x)):
        #    mesh_array.append([x[point], y[point], z[point], s[point]])
        #panel_mesh = np.array(mesh_array)

        X_np = np.array(x)
        Y_np = np.array(y)
        Z_np = np.array(z)
        S_np = np.array(s)

        mlab.mesh(X_np, Y_np, Z_np, scalars = S_np)

        #mlab.plot3d(panel_mesh[:,0], panel_mesh[:,1], panel_mesh[:,2], panel_mesh[:,3], colormap = 'blue-red')
        #print(mesh_array)
        #X = np.array(x)
        #Y = np.array(y)
        #print (len(X), len(Y))
        #X,Y = np.meshgrid(X,Y)
        #mlab.surf(X,Y,Z)
        #ax = plt.axes(projection='3d')
        #ax.plot_wireframe(X,Y,np.transpose(Z))
        #plt.show()
        #y = np.sin(phi) * np.sin(theta)
        #z = np.cos(phi)
        #mlab.mesh(x, y, z)
        #mlab.mesh(x, y, z, representation='wireframe', color=(0, 0, 0))
        #print(x)
        #print(y)
        #print(z)
        #pts = mlab.points3d(X,Y,Z,Z)
        #mesh = mlab.pipeline.delaunay2d(pts)

        #pts.remove()

        #surf = mlab.pipeline.surface(mesh)
    def plot_3D_panel(self, geo_panel, scalar = None):
        if geo_panel.orientation == 'horizontal':
            mlab.mesh(geo_panel.X, geo_panel.Y, geo_panel.Top, scalars = scalar)
            mlab.mesh(geo_panel.X, geo_panel.Y, geo_panel.Bottom, scalars = scalar)
        elif geo_panel.orientation == 'vertical':
            mlab.mesh(geo_panel.X, geo_panel.Top, geo_panel.Z, scalars = scalar)
            mlab.mesh(geo_panel.X, geo_panel.Bottom, geo_panel.Z, scalars = scalar)
        else:
            raise AttributeError

