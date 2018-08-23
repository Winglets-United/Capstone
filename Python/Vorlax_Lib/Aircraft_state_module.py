import numpy as np
import Vorlax_Lib.Geometry_Constructor as GC

class Aircraft_state(object):
    """Contains vorlax information of an aircraft for set conditions (M/alpha)"""
    def __init__(self):
        self.Panel_array = []
        self.Mach = float(0)
        self.Alpha = float(0)
        self.Psi = float(0)
        self.V_inf = float(0)
        self.is_in_ground_effect = False
        self.vortex_wake_floatation_params = Vortex_wake_floatation_params() 
        self.I_object_list = []
        self.Aero_cont_obj = Aero_container()
    def create_I_object(self):
        self.I_object_list.append(I_object())
    def create_panel_object(self):
        self.Panel_array.append(Panel())
    #Utility functions for converting string instances to floats. Used when pulling info from log file.
    def cast_metadata_members_to_float(self):
        self.Mach = float(self.Mach)
        self.Alpha = float(self.Alpha)
        self.Psi = float(self.Psi)
        self.V_inf = float(self.V_inf)
        self.vortex_wake_floatation_params.cast_members_to_float()
        self.Aero_cont_obj.cast_members_to_float()
        for I in self.I_object_list:
            I.cast_members_to_float()
    def cast_paneldata_members_to_float(self):
        for panel in self.Panel_array:
            panel.cast_members_to_float()
    def cast_all_members_to_float(self):
        self.cast_metadata_members_to_float()
        self.cast_paneldata_members_to_float()
    def get_panel_by_name(self, panel_name):
        panel_list = []
        for panel in self.Panel_array:
            if panel.name == panel_name:
                panel_list.append(panel)
        return panel_list
    
class Vortex_wake_floatation_params(object):
    """Vortex wake floatation parameters"""
    def __init__(self):
        self.Float_x = 0
        self.Float_y = 0
    def cast_members_to_float(self):
        self.Float_x = float(self.Float_x)
        self.Float_y = float(self.Float_y)
class I_object(object):
    """Vorlax I-specific information"""
    def __init__(self):
        self.I = 0
        self.Surf_SREF = 0
        self.CN = 0
        self.CL = 0
        self.CY = 0
        self.CD = 0
        self.CT = 0
        self.CS = 0
        self.CM = 0
        self.CRM = 0
        self.CYM = 0
    def cast_members_to_float(self):
        self.I = float(self.I)
        self.Surf_SREF = float(self.Surf_SREF)
        self.CN = float(self.CN)
        self.CL = float(self.CL)
        self.CY = float(self.CY)
        self.CD = float(self.CD)
        self.CT = float(self.CT)
        self.CS = float(self.CS)
        self.CM = float(self.CM)
        self.CRM = float(self.CRM)
        self.CYM = float(self.CYM)
class Aero_container(object):
    """Total aero_information for aircraft state"""
    def __init__(self):
        self.SREF = 0
        self.WSPAN = 0
        self.CBAR = 0
        self.CL_tot = 0
        self.CD_tot = 0
        self.CY_tot = 0
        self.CM_tot = 0
        self.CRM_tot = 0
        self.CYM_tot = 0
        self.Pitch_rate = 0
        self.Roll_rate = 0
        self.Yaw_rate = 0
        self.XBAR = 0
        self.ZBAR = 0
        self.drag_polar = 0
        self.E = 0
    def cast_members_to_float(self):
        self.SREF = float(self.SREF)
        self.WSPAN = float(self.WSPAN)
        self.CBAR = float(self.CBAR)
        self.CL_tot = float(self.CL_tot)
        self.CD_tot = float(self.CD_tot)
        self.CY_tot = float(self.CY_tot)
        self.CM_tot = float(self.CM_tot)
        self.CRM_tot = float(self.CRM_tot)
        self.CYM_tot = float(self.CYM_tot)
        self.Pitch_rate = float(self.Pitch_rate)
        self.Roll_rate = float(self.Roll_rate)
        self.Yaw_rate = float(self.Yaw_rate)
        self.XBAR = float(self.XBAR)
        self.ZBAR = float(self.ZBAR)
        self.drag_polar = float(self.drag_polar)
        self.E = float(self.E)
class Panel(object):
    """Contains vorlax information of an aircraft panel per Aircraft_state"""
    def __init__(self):
        self.NVOR_array = []
        self.name = ''
        self.Geometry = None
    def create_NVOR_object(self):
        self.NVOR_array.append(NVOR())
    def cast_members_to_float(self):
        for NVOR in self.NVOR_array:
            NVOR.cast_members_to_float()
    def initialize_geometry(self, type = 'wing'):
        if type == 'wing':
            self.Geometry = Panel_Wing_Geometry('horizontal')
        elif type == 'vertical':
            self.Geometry = Panel_Wing_Geometry('vertical')
        elif type == 'fuse' or type == 'fuselage':
            self.Geometry = Panel_Fuselage_Geometry()
    def set_geometry(self, type, orientation = 'horizontal', airfoil = '0012'):
        if type != 'fuselage' and type!= 'wing':
            raise ValueError
        if type == 'fuselage':
            self.Geometry = Panel_Fuselage_Geometry()
            self.Geometry.get_geometry(self)
        if type == 'wing':
            self.Geometry = Panel_Wing_Geometry()
            self.Geometry.orientation = orientation
            self.Geometry.airfoil = airfoil
            self.Geometry.get_geometry(self)

class Panel_Fuselage_Geometry(object):
    def __init(self):
        self.X = None
        self.Y = None
        self.Z = None
    def get_geometry(self, log_panel):
        temp_x = []
        temp_y = []
        x = []
        y = []
        for NVOR in log_panel.NVOR_array:
            for RNCV in NVOR.RNCV_array:
                temp_x.append(RNCV.X)
                temp_y.append(RNCV.Y)
            x.append(temp_x)
            y.append(temp_y)
            temp_x = []
            temp_y = []
        self.X = np.array(x)
        self.Y = np.array(y)

class Panel_Wing_Geometry(object):
    """Contains geometry information of a panel representing a wing"""
    def __init(self, orientation = 'horizontal', airfoil = '0012'):
        self.X = None
        self.Y = None
        self.Z = None
        self.Top = None
        self.Bottom = None
        self.Scalar = None
        self.orientation = orientation
        self.airfoil = airfoil
    def set_scalar(self, scalar_type, log_panel):
        s = []
        temp_s = []
        if scalar_type.lower() == 'x/c':
            for NVOR in log_panel.NVOR_array:
                for RNCV in NVOR.RNCV_array:
                    temp_s.append(RNCV.XC)
                s.append(temp_s)
                temp_s = []
        elif scalar_type.lower() == 'chord':
            for NVOR in log_panel.NVOR_array:
                for RNCV in NVOR.RNCV_array:
                    temp_s.append(RNCV.Chord)
                s.append(temp_s)
                temp_s = []
        elif scalar_type.lower() == 'slope':
            for NVOR in log_panel.NVOR_array:
                for RNCV in NVOR.RNCV_array:
                    temp_s.append(RNCV.Slope)
                s.append(temp_s)
                temp_s = []
        elif scalar_type.lower() == 'its':
            for NVOR in log_panel.NVOR_array:
                for RNCV in NVOR.RNCV_array:
                    temp_s.append(RNCV.ITS)
                s.append(temp_s)
                temp_s = []
        elif scalar_type.lower() == 'dcp':
            for NVOR in log_panel.NVOR_array:
                for RNCV in NVOR.RNCV_array:
                    temp_s.append(RNCV.DCP)
                s.append(temp_s)
                temp_s = []
        elif scalar_type.lower() == 'gamma':
            for NVOR in log_panel.NVOR_array:
                for RNCV in NVOR.RNCV_array:
                    temp_s.append(RNCV.Gamma)
                s.append(temp_s)
                temp_s = []
        else:
            print('ERROR IN RETRIEVING SCALAR IN PANEL_WING_GEOMETRY: scalar ' + scalar_type + ' not found!')
            return None
        self.Scalar = np.array(s)

    def get_geometry(self, log_panel):
        temp_x = []
        temp_y = []
        temp_z = []
        x = []
        y = []
        z = []
        for NVOR in log_panel.NVOR_array:
            for RNCV in NVOR.RNCV_array:
                temp_x.append(RNCV.X)
                temp_y.append(RNCV.Y)
                temp_z.append(RNCV.Z)
            x.append(temp_x)
            y.append(temp_y)
            z.append(temp_z)
            temp_x = []
            temp_y = []
            temp_z = []
        self.X = np.array(x)
        self.Y = np.array(y)
        self.Z = np.array(z)
        self.Top, self.Bottom = GC.construct_wing(self)
        if self.orientation == 'horizontal': #add Z-offset
            self.Top += self.Z
            self.Bottom += self.Z
        elif self.orientation == 'vertical': #add Y-offset
            self.Top += self.Y
            self.Bottom += self.Y
        
class NVOR(object):
    """Contains vorlax information of an aircraft panel at NVOR location"""
    def __init__(self):
        self.RNCV_array = []
        self.CNC = 0
        self.CN = 0
        self.DL = 0
        self.CMT = 0
        self.CTC = 0
        self.CDC = 0
    def create_RNCV_array(self):
        self.RNCV_array.append(RNCV())
    def cast_members_to_float(self):
        self.CNC = float(self.CNC)
        self.CN = float(self.CN)
        self.DL = float(self.DL)
        self.CMT = float(self.CMT)
        self.CTC = float(self.CTC)
        self.CDC = float(self.CDC)
        for RNCV in self.RNCV_array:
            RNCV.cast_members_to_float()
class RNCV(object):
    """Contains vorlax information of an aircraft panel at RNCV location"""
    def __init__(self):
        self.S = 0
        self.C = 0
        self.XC = 0
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.Chord = 0
        self.Slope = 0
        self.ITS = 0
        self.DCP = 0
        self.Gamma = 0
    def cast_members_to_float(self):
        self.S = float(self.S)
        self.C = float(self.C)
        self.XC = float(self.XC)
        self.X = float(self.X)
        self.Y = float(self.Y)
        self.Z = float(self.Z)
        self.Chord = float(self.Chord)
        self.Slope = float(self.Slope)
        self.ITS = float(self.ITS)
        self.DCP = float(self.DCP)
        self.Gamma = float(self.Gamma)

