#EXAMPLE FILE FOR USING Vorlax_Lib PYTHON MODULES
#PANEL PARSING: OBJECTS ARE 0-BASED ARRAYS, THUS NVOR_array[0].RNCV_array[1] CORRESPONDS TO S = 1, C = 2

import matplotlib.pyplot as plt
from mayavi import mlab
from Vorlax_Lib.Log_parser_module import logParser
from Vorlax_Lib.Aircraft_state_module import Aircraft_state
from Vorlax_Lib.AC_surface_plotter import AC_surface_plotter

#Create log_parser and attach log file to parser
log_parser = logParser('vorlax.LOG')
#Load log file to local memory
log_parser.load()
#Get aircraft name from log files
log_parser.get_AC_identifier()
#Get locations of each computational run of aircraft
log_parser.get_ident_stations()

#Initialize aircraft state container list
AC_states = []

#Parse aircraft states from log file
print('Total AC_states found: ', len(log_parser.AC_ident_list))
cur_AC = 1
for AC_ident in log_parser.AC_ident_list:
    print('Parsing AC_state: ', cur_AC)
	#Initialize new empty AC state
    AC_states.append(Aircraft_state())
	#Parse AC metadata
    try:
		log_parser.parse_metadata(AC_ident, AC_states[-1])  
        print('metadata parse success!')
    except:
       print('ERROR IN METADATA PARSING; METADATA GENERATION FAILED')
	
	#parse AC panel data
    try: 
        log_parser.parse_paneldata(AC_ident, AC_states[-1])
        print('panel parse success!')
    except:
        print('ERROR IN PANEL PARSING; PANEL GENERATION FAILED')
    cur_AC += 1

#Create new surface plot object. Each surface plot object holds info for ONE AC state
AC_surf_plot = AC_surface_plotter()
#Attach aircraft state to surface plot object
try:
    AC_surf_plot.attach(AC_states[7])
except AttributeError:
    print('ERROR: AIRCRAFT STATE ALREADY ATTACHED IN AC_SURFACE_PLOTTER')
#plot 2d panels of AC state
AC_surf_plot.plot_all_panels_2D()

#3d plot of wings
wing_panel_names = ['PANEL NO. 3', 'PANEL NO. 4', 'PANEL NO. 5', 'PANEL NO. 6', 'PANEL NO. 7', 'PANEL NO. 10']
for wing_panel_name in wing_panel_names:
    for panel in AC_states[7].get_panel_by_name(wing_panel_name):
        panel.set_geometry('wing',airfoil='23112')
        panel.Geometry.set_scalar('Gamma', panel)
        AC_surf_plot.plot_3D_panel(panel.Geometry, panel.Geometry.Scalar)

for panel in AC_states[7].get_panel_by_name('PANEL NO. 11'):
    panel.set_geometry('wing',orientation='vertical')
    panel.Geometry.set_scalar('Gamma', panel)
    AC_surf_plot.plot_3D_panel(panel.Geometry, panel.Geometry.Scalar)

#show plots from AC surface plot objects
mlab.show()

