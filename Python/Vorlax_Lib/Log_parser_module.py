import numpy as np
from Vorlax_Lib.Aircraft_state_module import Aircraft_state

class logParser(object):
    def __init__(self, Vorlax_log_path):
        self.log_file_path = Vorlax_log_path
        self.AC_states = []
    def load(self):
        
        self.log = open(self.log_file_path, 'r')
        self.tot_line_num = 0
        self.log_lines = []
        for line in self.log:
            self.log_lines.append(line)
        self.tot_line_num = len(self.log_lines)
        self.log.close()
    def get_AC_identifier(self):
        self.AC_identifier = self.log_lines[4]
        print('Parsing', self.AC_identifier)
    def get_ident_stations(self):
        #gets identifying points in log file (start and end of each run, etc.)
        self.AC_ident_list = []
        AC_ident_index_list = []
        End_of_case_index_list = []
        curRow = 0
        for line in self.log_lines:
            if self.AC_identifier in line:
                AC_ident_index_list.append(curRow) #cues start of run
            if "END OF CASE" in line:
                End_of_case_index_list.append(curRow) #cues end of run
            curRow += 1
        AC_ident_index_list = AC_ident_index_list[1:]
        skip = False
        for index in AC_ident_index_list:
            if not skip:
                self.AC_ident_list.append(AC_ident_index())
                self.AC_ident_list[-1].meta_index = index
            else:
                self.AC_ident_list[-1].panel_index = index
            skip = not skip

        for i in range(0, len(End_of_case_index_list)):
            self.AC_ident_list[i].end_of_case_index = End_of_case_index_list[i]

    def parse_metadata(self, AC_ident_obj, AC_state_obj):
        if not isinstance(AC_state_obj, Aircraft_state):
            raise ValueError('AC_state_obj must be of type Aircraft_state')
            return
        [temp, temp, AC_state_obj.Mach] = self.log_lines[AC_ident_obj.meta_index+1].split()
        try: #If negative alpha, there will be no space between '=' and alpha in the log file
            [temp, temp, AC_state_obj.Alpha, temp] = self.log_lines[AC_ident_obj.meta_index+3].split()
        except ValueError:
            [temp, alphaTemp, temp] = self.log_lines[AC_ident_obj.meta_index+3].split()
            AC_state_obj.Alpha = alphaTemp[1:-1]
        [temp, temp, AC_state_obj.Psi, temp] = self.log_lines[AC_ident_obj.meta_index+4].split()
        [temp, temp, temp, AC_state_obj.Aero_cont_obj.Pitch_rate, temp] = self.log_lines[AC_ident_obj.meta_index+6].split()
        [temp, temp, temp, AC_state_obj.Aero_cont_obj.Roll_rate, temp] = self.log_lines[AC_ident_obj.meta_index+7].split()
        [temp, temp, temp, AC_state_obj.Aero_cont_obj.Yaw_rate, temp] = self.log_lines[AC_ident_obj.meta_index+8].split()
        [temp, temp, temp, temp, temp, temp, temp, AC_state_obj.Aero_cont_obj.XBAR, temp, temp, AC_state_obj.Aero_cont_obj.ZBAR, 
         temp, temp, temp, AC_state_obj.V_inf] = self.log_lines[AC_ident_obj.meta_index+13].split()
        [temp, temp, temp, temp, temp, temp, temp, AC_state_obj.vortex_wake_floatation_params.Float_x, temp, temp, 
         AC_state_obj.vortex_wake_floatation_params.Float_y] = self.log_lines[AC_ident_obj.meta_index+15].split()
        if "CONFIGURATION IS OUT OF GROUND EFFECT" in self.log_lines[AC_ident_obj.meta_index+14]:
            AC_state_obj.is_in_ground_effect = False
        else:
            AC_state_obj.is_in_ground_effect = True
        self.get_I_data(AC_ident_obj, AC_state_obj)
         
        AC_state_obj.cast_metadata_members_to_float()

    def get_I_data(self, AC_ident_obj, AC_state_obj):
        end_of_I_index = AC_ident_obj.meta_index
        start_of_I_index = AC_ident_obj.meta_index+22
        SREF_counter = 0
        for line in self.log_lines[AC_ident_obj.meta_index:AC_ident_obj.panel_index]:
            if "SREF" in line:
                SREF_counter += 1
            if SREF_counter == 3:
                break
            end_of_I_index += 1
        end_of_I_index = end_of_I_index-1
        for index in range(start_of_I_index,end_of_I_index):
            AC_state_obj.create_I_object()
            if self.log_lines[index][0] == '*':
                try:
                    [temp, AC_state_obj.I_object_list[-1].I, AC_state_obj.I_object_list[-1].Surf_SREF,  AC_state_obj.I_object_list[-1].CN,  
                     AC_state_obj.I_object_list[-1].CL,  AC_state_obj.I_object_list[-1].CY,  AC_state_obj.I_object_list[-1].CD,  
                     AC_state_obj.I_object_list[-1].CT,  AC_state_obj.I_object_list[-1].CS,  AC_state_obj.I_object_list[-1].CM,  
                     AC_state_obj.I_object_list[-1].CRM,  AC_state_obj.I_object_list[-1].CYM] = self.log_lines[index].split()
                except ValueError: #if ** list is too long, first value will merge with **
                    [tempI, AC_state_obj.I_object_list[-1].Surf_SREF,  AC_state_obj.I_object_list[-1].CN,  
                     AC_state_obj.I_object_list[-1].CL,  AC_state_obj.I_object_list[-1].CY,  AC_state_obj.I_object_list[-1].CD,  
                     AC_state_obj.I_object_list[-1].CT,  AC_state_obj.I_object_list[-1].CS,  AC_state_obj.I_object_list[-1].CM,  
                     AC_state_obj.I_object_list[-1].CRM,  AC_state_obj.I_object_list[-1].CYM] = self.log_lines[index].split()
                    AC_state_obj.I_object_list[-1].I = tempI[2:]
            else:
                [AC_state_obj.I_object_list[-1].I, AC_state_obj.I_object_list[-1].Surf_SREF,  AC_state_obj.I_object_list[-1].CN,  
                 AC_state_obj.I_object_list[-1].CL,  AC_state_obj.I_object_list[-1].CY,  AC_state_obj.I_object_list[-1].CD,  
                 AC_state_obj.I_object_list[-1].CT,  AC_state_obj.I_object_list[-1].CS,  AC_state_obj.I_object_list[-1].CM,  
                 AC_state_obj.I_object_list[-1].CRM,  AC_state_obj.I_object_list[-1].CYM] = self.log_lines[index].split()

        [AC_state_obj.Aero_cont_obj.SREF, AC_state_obj.Aero_cont_obj.WSPAN, AC_state_obj.Aero_cont_obj.CBAR,
         AC_state_obj.Aero_cont_obj.CL_tot, AC_state_obj.Aero_cont_obj.CD_tot, AC_state_obj.Aero_cont_obj.CY_tot, AC_state_obj.Aero_cont_obj.CM_tot,
         AC_state_obj.Aero_cont_obj.CRM_tot, AC_state_obj.Aero_cont_obj.CYM_tot] = self.log_lines[end_of_I_index+2].split()

    def parse_paneldata(self, AC_ident_obj, AC_state_obj):
        #multi-panel parsing
        AC_ident_obj.get_panel_loc_index(self.log_lines)
        parse_nvor = False
        for panel in AC_ident_obj.panel_loc_index:
            #create a new panel
            AC_state_obj.create_panel_object()
            panel_name_split = self.log_lines[panel.start-1].split()
            for word in panel_name_split:
                AC_state_obj.Panel_array[-1].name += word
                AC_state_obj.Panel_array[-1].name += ' '
            AC_state_obj.Panel_array[-1].name = AC_state_obj.Panel_array[-1].name[:-1]
            for line_num in range(panel.start, panel.end):
                #create a new RNCV
                line_split = self.log_lines[line_num].split()
                if len(line_split) == 17:
                    #create a new NVOR
                    AC_state_obj.Panel_array[-1].create_NVOR_object()
                    parse_nvor = True
                AC_state_obj.Panel_array[-1].NVOR_array[-1].create_RNCV_array()
                if parse_nvor:
                    [AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].S, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].C,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].XC, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].X,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Y, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Z,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Chord, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Slope,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].ITS, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].DCP,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].CNC, AC_state_obj.Panel_array[-1].NVOR_array[-1].CN, AC_state_obj.Panel_array[-1].NVOR_array[-1].DL,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].CMT,AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Gamma, 
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].CTC, AC_state_obj.Panel_array[-1].NVOR_array[-1].CDC] = line_split
                    parse_nvor = False
                else:
                     [AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].S, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].C,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].XC, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].X,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Y, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Z,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Chord, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Slope,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].ITS, AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].DCP,
                     AC_state_obj.Panel_array[-1].NVOR_array[-1].RNCV_array[-1].Gamma] = line_split
        AC_state_obj.cast_paneldata_members_to_float()

class AC_ident_index(object):
    """Index of aircraft runs in log file. Contains pair: 1-metadata, 2-panel info"""
    def __init__(self):
        self.meta_index = 0
        self.panel_index = 0
        self.end_of_case_index = 0
        self.panel_loc_index = []
    def get_panel_loc_index(self, log_lines):
        panel_locs = []
        Cur_Row = self.panel_index
        for line in log_lines[self.panel_index:self.end_of_case_index]:
            if "PANEL" in line:
                panel_locs.append(Cur_Row)
            Cur_Row += 1
        skip = True
        for i in range(0,len(panel_locs)):
            self.panel_loc_index.append(Panel_index())
            if i > 0:
                self.panel_loc_index[-2].end = panel_locs[i]
            self.panel_loc_index[-1].start = panel_locs[i]
        for panel in self.panel_loc_index:
            panel.start = panel.start+1
        self.panel_loc_index[-1].end = self.end_of_case_index-5

class Panel_index(object):
    def __init__(self):
        self.start = 0
        self.end = 0

class LogParser_old(object):
    """LOG File Parser for Vorlax"""
    def __init__(self, filePath):
        self.filePath = filePath
        self.VorFile = open(self.filePath,"r")
        self.VorInfo=[] #store VorFile information as singular lines
        self.lineNum = 0 #store number of lines in VorFile
        self.parseObjs = []
        self.loadFile() # load VorFile into VorInfo
        self.panelLoc = self.getLines('PANEL NO.') # Load Panel Begin Locations
        self.panEndLoc = self.getLines('ITRMAX =')
        self.iterLoc = self.getLines('ANALYSIS (DIRECT)  CASE') # Load Iteration Locations
        self.panel =  np.zeros(shape = (self.panelLoc[1]-self.panelLoc[0],17))
        self.temp = []
        self.rowIter = 0
        self. colIter = 0
        self.lBound = 0
        self.parsePanels()

    def loadFile(self):
        for line in self.VorFile:
            self.VorInfo.append(line)
            self.lineNum += 1

    def getLines(self, infoStr):
        #find line numbers where infoStr occurs
        tempMat = []
        for i in range(0,len(self.VorInfo)):
            if self.VorInfo[i].find(infoStr) != -1:
                tempMat.append(i)
        return tempMat

    def getLine(self, startLine, infoStr):
        #find first line where infoStr appears from start
        lineNum = []
        for i in range(startLine, len(self.VorInfo)):
            if self.VorInfo[i].find(infoStr) != -1:
                lineNum = i
                return lineNum

    def setOutPanel(self, panelLoc):
        self.panel = np.zeros(shape = (self.panelLoc[panelLoc+1]-self.panelLoc[panelLoc]-1,17))

    def getPanelLoc(self):
        return self.panelLoc

    def rowParse(self, panLoc): # Creates an array with the numbers in a line
        num = []
        for k in range(0, len(self.VorInfo[panLoc])):  # goes through an entire line
            a = self.VorInfo[panLoc][k]
            if a != " " and k != len(self.VorInfo[panLoc]) - 1:
                self.temp.append(self.VorInfo[panLoc][k])  # store numbers in temp array
            elif len(self.temp) != 0:
                num.append(''.join(self.temp))  # once it gets back to spaces, join temp array into 1 str => store in num
                # print(num)
                self.temp.clear()
                # after k loop, num will have all values for a line WORKS
        return num

    # Expects line to have 17 members
    def longParse(self, panLoc):
        rowVect = np.zeros(shape = (1,17)) # create temporary vector for storing numbers
        num = self.rowParse(panLoc) # get all numbers in a specific line
        for col in range(0, len(num)):
            # self.panel[panNum][col] = (float(num[col]))
            rowVect[0][col] = (float(num[col]))
        return rowVect

    # Expects line to have 11 members
    def shortParse(self, panLoc):
        rowVect = np.zeros(shape=(1, 17))
        num = self.rowParse(panLoc)
        for col in range(0, len(num)):
            if(col < 10) :
               # self.panel[panNum][col] = (float(num[col]))
                rowVect[0][col] = float(num[col])
            elif(col == 10):
                # print(num[11])
                # self.panel[panNum][14] = float(num[11]);
                rowVect[0][14] = float(num[10])
            else:
                # self.panel[panNum][col] = float(0)
                rowVect[0][col] = float(0)
        return rowVect

    # Segment parse inside a panel
    def segParse(self, panel, startLoc, endLoc, type):
        iter = 0
        for j in range(self.panelLoc[panel]+startLoc, self.panelLoc[panel] + endLoc):
            if type == "long":
                self.panel[iter] = self.longParse(j, iter)
                iter += 1
            else:
                self.panel[iter] = self.shortParse(j, iter)
                # print(self.panel[iter])
                iter+=1
        return self.panel

    def panParse(self, parseObj, panelNum):
        parseObj.newPanel()
        iter = 0
        for line in range(self.panelLoc[panelNum]+1, self.panEndLoc[panelNum]):
            if self.VorInfo[line].find('ITRMAX') != -1: #quit at end of panels
                break;
            if iter == 0 or self.shortParse(line)[0][0] > self.shortParse(line-1)[0][0]:
                longParse = self.longParse(line)
                #print(longParse)
                parseObj.getLastPanel().addSingular(longParse[0])
            shortParse = self.shortParse(line)
            #print(shortParse)
            parseObj.getLastPanel().addVortex_C(shortParse[0])
            iter += 1
                #parseObj.panels[len(parseObj.panels)].addSingular(longParse)
            #elif self.panel[iter-1][1] > self.panel[iter][1]:
             #   longParse = self.longParse(line, iter)

    def parsePanels(self):
        for iter in range(0, len(self.iterLoc)):#Check through each iteration
            self.parseObjs.append(po.parseObj())
            self.setIterConsts(self.parseObjs[iter], self.iterLoc[iter])
            #print(self.parseObjs[iter].Mach)
            for pan in range(0, len(self.panelLoc)):
                self.panParse(self.parseObjs[iter],pan)

    def parseConsts(self, line):
        numMat = []
        temp = []
        record = False
        recIter = 0
        for i in range(0,len(self.VorInfo[line])): #Go through the MACH line character after character
            char = self.VorInfo[line][i]
            if char == '=':
                record = True
                continue
            if record:
                #print(char, ord(char))
                if (ord(char) >= 48 and ord(char) <= 57) or char == '.':
                    temp.append(char)
                elif char == ' ':
                    continue
                else:
                    numMat.append(''.join(temp))
                    temp.clear()
                    record = False
            #print(record, char)
        return numMat

    def setIterConsts(self, parseObj, iterLine):
        constLine = self.getLine(iterLine, 'MACH')
        #NEED TO PARSE MACH LINE FOR CONSTANTS
        constMatrix = self.parseConsts(constLine)
        #print(constMatrix)
        parseObj.setConstants(constMatrix)

