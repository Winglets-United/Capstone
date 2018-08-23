import numpy as np

class Five_Series_Constants(object):
    """holds constants information for 5-series airfoil"""
    def __init__(self):
        self.Camber = np.array([0.05, 0.1, 0.15, 0.2, 0.25])
        self.Camber_r = np.array([0.1, 0.15, 0.2, 0.25])
        self.r = np.array([0.05580, 0.126, 0.2025, 0.29, 0.391])
        self.r_r = np.array([0.13, 0.217, 0.318, 0.441])
        self.k1 = np.array([361.4, 51.64, 15.957, 6.643, 3.23])
        self.k1_r = np.array([51.99, 15.493, 6.520, 3.191])
        self.k2k1 = np.array([0.000764, 0.00677, 0.0303, 0.1355])
    def get_constants_by_camber(self, input_camber, Is_Reflexed = False):
        right_cam_index = 0
        if Is_Reflexed:
            for camber_index in range(0,len(self.Camber_r)):
                if input_camber <= self.Camber_r[camber_index]:
                    right_cam_index = camber_index
                    break

            if right_cam_index == 0:
                right_cam_index = 1

            r_gradient = (self.r_r[right_cam_index]-self.r_r[right_cam_index-1])/(self.Camber_r[right_cam_index]-self.Camber_r[right_cam_index-1])
            k1_gradient =  (self.k1_r[right_cam_index]-self.k1_r[right_cam_index-1])/(self.Camber_r[right_cam_index]-self.Camber_r[right_cam_index-1])
            k2k1_gradient =  (self.k2k1[right_cam_index]-self.k2k1[right_cam_index-1])/(self.Camber_r[right_cam_index]-self.Camber_r[right_cam_index-1])

            r = self.r_r[right_cam_index] + (input_camber-self.Camber_r[right_cam_index])*r_gradient
            k1 = self.k1_r[right_cam_index] + (input_camber-self.Camber_r[right_cam_index])*k1_gradient
            k2k1 = self.k2k1[right_cam_index] + (input_camber-self.Camber_r[right_cam_index])*k2k1_gradient
        else:
            for camber_index in range(0,len(self.Camber)):
                if input_camber <= self.Camber[camber_index]:
                    right_cam_index = camber_index
                    break

            if right_cam_index == 0:
                right_cam_index = 1

            r_gradient = (self.r[right_cam_index]-self.r[right_cam_index-1])/(self.Camber[right_cam_index]-self.Camber[right_cam_index-1])
            k1_gradient =  (self.k1[right_cam_index]-self.k1[right_cam_index-1])/(self.Camber[right_cam_index]-self.Camber[right_cam_index-1]) 

            r = self.r_r[right_cam_index] + (input_camber-self.Camber_r[right_cam_index])*r_gradient
            k1 = self.k1_r[right_cam_index] + (input_camber-self.Camber_r[right_cam_index])*k1_gradient
            k2k1 = 0

        return r, k1, k2k1

Five_series_constants = Five_Series_Constants()

def construct_wing(geo_panel, closed_trailing_edge = False):
    """function to construct wing using NACA 4-series or 5-series from geometric wing panel"""
    if len(geo_panel.airfoil) == 4:
        Max_Camber = float(geo_panel.airfoil[0])/100
        Max_Camber_Position = float(geo_panel.airfoil[1])/10
        Thickness = float(geo_panel.airfoil[2:])/100
        return construct_4_series(geo_panel, Max_Camber, Max_Camber_Position, Thickness, closed_trailing_edge)
    elif len(geo_panel.airfoil) == 5:
        Design_CL = float(geo_panel.airfoil[0])*3/20
        Max_Camber_Position = float(geo_panel.airfoil[1])/20
        Is_Reflexed = bool(int(geo_panel.airfoil[2])) #true = reflex
        Max_Thickness = float(geo_panel.airfoil[3:])/100
        return construct_5_series(geo_panel, Design_CL, Max_Camber_Position, Is_Reflexed, Max_Thickness, closed_trailing_edge)
    else:
        print('ERROR: airfoil type: ' + geo_panel.airfoil + ' NOT RECOGNIZED')
        raise ValueError

def construct_4_series(geo_panel, Max_Camber, Max_Camber_Position, Thickness, closed_trailing_edge):
    #define constants
    a0 = 0.2969
    a1 = -.126
    a2 = -.3516
    a3 = .2843
    if closed_trailing_edge:
        a4 = -0.1036
    else:
        a4 = -0.1015

    temp_z_bot = []
    temp_z_top = []
    z_bot = []
    z_top = []
    Z_top = None
    Z_bot = None
    for row in geo_panel.X:
        X_start = row[0]
        X_end = row[-1]
        chord = X_end-X_start
        for X_loc in row:
            #initialize intermediate calcs
            camber = 0
            gradient = 0
            thick_dist = 0
            theta = 0
            x = (X_loc-X_start)/chord

            #Camber Calculation
            if x<Max_Camber_Position: #front
                camber = ((Max_Camber)/(Max_Camber_Position**2))*(2*Max_Camber_Position*x-x**2)
                gradient = ((2*Max_Camber)/(Max_Camber_Position**2))*(Max_Camber_Position-x)
            else: #back
                camber = ((Max_Camber)/((1-Max_Camber_Position)**2))*(1-2*Max_Camber_Position+2*Max_Camber_Position*x-x**2)
                gradient = ((2*Max_Camber)/((1-Max_Camber_Position)**2))*(Max_Camber_Position-x)

            #thickness at location
            thick_dist = (Thickness/0.2)*(a0*x**0.5 + a1*x + a2*x**2 + a3*x**3 + a4*x**4)

            #get upper and lower surface
            theta = np.arctan(gradient)
            temp_z_top.append((camber + thick_dist*np.cos(theta))*chord) #re-normalize to actual size
            temp_z_bot.append((camber - thick_dist*np.cos(theta))*chord)
        z_bot.append(temp_z_bot)
        z_top.append(temp_z_top)
        temp_z_bot = []
        temp_z_top = []

    Z_top = np.array(z_top)
    Z_bot = np.array(z_bot)
    return Z_top, Z_bot

def construct_5_series(geo_panel, Design_CL, Max_Camber_Position, Is_Reflexed, Max_Thickness, closed_trailing_edge):
 #define constants
    a0 = 0.2969
    a1 = -.126
    a2 = -.3516
    a3 = .2843
    if closed_trailing_edge:
        a4 = -0.1036
    else:
        a4 = -0.1015

    temp_z_bot = []
    temp_z_top = []
    z_bot = []
    z_top = []
    Z_top = None
    Z_bot = None
    for row in geo_panel.X:
        X_start = row[0]
        X_end = row[-1]
        chord = X_end-X_start
        for X_loc in row:
            #initialize intermediate calcs
            camber = 0
            gradient = 0
            thick_dist = 0
            theta = 0
            x = (X_loc-X_start)/chord

            #Camber Calculation
            r, k1, k2k1 = Five_series_constants.get_constants_by_camber(Max_Camber_Position, Is_Reflexed)
            if x<Max_Camber_Position: #front
                if Is_Reflexed:
                    camber = (k1/6) * ((x-r)**3 - k2k1 * ((1-r)**3) * x - (r**3) * x + r**3)
                    gradient = (k1/6) * (3 * (x-r)**2 - k2k1 * (1-r)**3 - r**3)
                else:
                    camber = (k1/6) * (x**3 - 3 * r * x**2 + r**2 * (3-r) * x)
                    gradient = (k1/6) * (3 * x**2 - 6 * r * x + r**2 * (3-r))
            else: #back
                if Is_Reflexed:
                    camber = (k1/6)* (k2k1 * (x-r)**3 - k2k1 * (1-r)**3 * x - r**3 * x + r**3)
                    gradient = (k1/6) * (3 * k2k1 * (x-r)**2 - k2k1 * (1-r)**3 - r**3)
                else:
                    camber = ((k1 * r**3)/6) * (1-x)
                    gradient = -((k1 * r**3)/6)

            #thickness at location
            thick_dist = (Max_Thickness/0.2)*(a0*x**0.5 + a1*x + a2*x**2 + a3*x**3 + a4*x**4)

            #get upper and lower surface
            theta = np.arctan(gradient)
            temp_z_top.append((camber + thick_dist*np.cos(theta))*chord) #re-normalize to actual size
            temp_z_bot.append((camber - thick_dist*np.cos(theta))*chord)
        z_bot.append(temp_z_bot)
        z_top.append(temp_z_top)
        temp_z_bot = []
        temp_z_top = []

    Z_top = np.array(z_top)
    Z_bot = np.array(z_bot)
    return Z_top, Z_bot

