#
# mesInterface.py -- a class that creates a nice GUI
# Works in conjunction with MESOffset ginga plugin for MOS Acquisition
#
# Justin Kunimune
#



# standard imports
import math
import sys

# local imports

# ginga imports
from ginga.gw import Widgets, Viewers

# third-party imports
import numpy as np
from numpy import ma



# constants
# database folder location
DBS = "../../MCSRED2/DATABASE"
# main menu parameters
params_0 = [    # TODO: get rid of these defaults; they're just for my convinience
        {'name':'star_chip1',
         'label':"Star Frame", 'type':'number', 'default':227463,   #TODO odd constraint
         'desc':"The frame number for the chip1 star FITS image",
         'format':"MCSA{}.fits"},
        
        {'name':'rootname',
         'label':"Root Name", 'type':'string', 'default':"sbr_elaisn1rev",
         'desc':"The filename of the SBR file, which is used as rootname",
         'format':"{}.sbr"},
        
        {'name':'c_file',
         'label':"Config File", 'type':'string', 'default':DBS+"/ana_apr16.cfg",
         'desc':"The location of the MCSRED configuration file"},
        
        {'name':'img_dir',
         'label':"Image Directory", 'type':'string', 'default':"RAW/",
         'desc':"The directory in which the input FITS images can be found"},
        
        {'name':'exec_mode',
         'label':"Execution Mode", 'type':'choice', 'default':0,    #TODO
         'desc':"The desired level of precision of alignment",
         'options':["Normal", "Fine"]},
        
        {'name':'mode',
         'label':"Mode", 'type':'choice', 'default':0,
         'desc':"I don't know what this means. Remind me to look it up later.",
         'options':["q1"]}
        ]

# mesoffset1 parameters
params_1 = [
        {'name':'star_chip1',
         'label':"Star Frame", 'type':'number',
         'desc':"The frame number for the chip1 star FITS image",
         'format':"MCSA{}.fits"},
        
        {'name':'sky_chip1',
         'label':"Sky Frame", 'type':'number',
         'desc':"The frame number for the chip1 sky FITS image",
         'format':"MCSA{}.fits"},
        
        {'name':'rootname',
         'label':"Root Name", 'type':'string',
         'desc':"The filename of the SBR file, which is used as rootname",
         'format':"{}.sbr"},
        
        {'name':'c_file',
         'label':"Config File", 'type':'string', 'default':DBS+"/ana_apr16.cfg",
         'desc':"The location of the MCSRED configuration file"},
        
        {'name':'img_dir',
         'label':"Image Directory", 'type':'string', 'default':"data$",
         'desc':"The directory in which the raw FITS images can be found"},
        
        {'name':'retry1',
         'label':"Reuse Star", 'type':'boolean',
         'desc':"Do you want to reuse mosaiced star images last time?"},
        
        {'name':'retry2',
         'label':"Reuse Mask", 'type':'boolean',
         'desc':"Do you want to reuse mosaiced mask images last time?"},
        
        {'name':'inter1',
         'label':"Interact Star", 'type':'boolean',
         'desc':"Do you want to interact with star position measurement?"},
        
        {'name':'inter2',
         'label':"Interact Hole", 'type':'boolean',
         'desc':"Do you want to interact with hole position measurement?"},
        
        {'name':'list1',
         'label':"List 1", 'type':'string',
         'desc':"something something something something something something "},
        
        {'name':'list2',
         'label':"List 2", 'type':'string',
         'desc':"I'm sorry, were you hoping for a descriptive tooltip?"},
        
        {'name':'mode',
         'label':"Mode", 'type':'choice',
         'desc':"I don't know what this means. Remind me to look it up later.",
         'options':["q1"]}
        ]

# mesoffset2 parameters
params_2 = [
        {'name':'starhole_chip1',
         'label':"Star-Hole Frame", 'type':'number',
         'desc':"The frame number for the chip1 star-hole FITS image",
         'format':"MCSA{}.fits"},
        
        {'name':'sky_chip1',
         'label':"Sky Name", 'type':'number',
         'desc':"The frame number for the chip1 sky FITS image",
         'format':"MCSA{}.fits"},
        
        {'name':'rootname',
         'label':"Root Name", 'type':'string',
         'desc':"The filename of the SBR file, which is used as rootname",
         'format':"{}.sbr"},
        
        {'name':'c_file',
         'label':"Config File", 'type':'string', 'default':DBS+"/ana_apr16.cfg",
         'desc':"The location of the MCSRED configuration file"},
        
        {'name':'img_dir',
         'label':"Image Directory", 'type':'string', 'default':"data$",
         'desc':"The directory in which the raw FITS images can be found"},
        
        {'name':'retry1',
         'label':"Reuse", 'type':'boolean', 'default':False,    #TODO: retry3?
         'desc':"Do you want to reuse mosaiced images last time?"},
        
        {'name':'interac1',
         'label':"Interact", 'type':'boolean',
         'desc':"Do you want to interact with star position measurement?"},
        
        {'name':'list1',
         'label':"List 1", 'type':'string',
         'desc':"something something something something something something "},
        
        {'name':'mode',
         'label':"Mode", 'type':'choice',
         'desc':"I don't know what this means. Remind me to look it up later.",
         'options':["q1"]}
        ]

# mesoffset3 parameters
params_3 = [
        {'name':'star_chip1',
         'label':"Star-Hole Frame", 'type':'number', 'default':226725,
         'desc':"The frame number for the chip1 star-hole FITS image",
         'format':"MCSA{}.fits"},
        
        {'name':'sky_chip1',
         'label':"Sky Name", 'type':'number', 'default':226725,
         'desc':"The frame number for the chip1 sky FITS image",
         'format':"MCSA{}.fits"},
        
        {'name':'rootname',
         'label':"Root Name", 'type':'string',
         'desc':"The filename of the SBR file, which is used as rootname",
         'format':"{}.sbr"},
        
        {'name':'c_file',
         'label':"Config File", 'type':'string', 'default':DBS+"/ana_apr16.cfg",
         'desc':"The location of the MCSRED configuration file"},
        
        {'name':'img_dir',
         'label':"Image Directory", 'type':'string', 'default':"data$",
         'desc':"The directory in which the raw FITS images can be found"},
        
        {'name':'retry1',
         'label':"Reuse Star", 'type':'boolean',
         'desc':"Do you want to reuse mosaiced star images last time?"},
        
        {'name':'retry2',
         'label':"Reuse Mask", 'type':'boolean',
         'desc':"Do you want to reuse mosaiced mask images last time?"},
        
        {'name':'interac1',
         'label':"Interact Hole", 'type':'boolean',
         'desc':"Do you want to interact with hole position measurement?"},
        
        {'name':'interac2',
         'label':"Interact Star-Hole", 'type':'boolean',
         'desc':"Do you want to interact with star-hole position measurement?"},
        
        {'name':'list1',
         'label':"List 1", 'type':'string',
         'desc':"something something something something something something "},
        
        {'name':'mode',
         'label':"Mode", 'type':'choice',
         'desc':"I don't know what this means. Remind me to look it up later.",
         'options':["q1"]}
        ]



class MESInterface:
    """
    A class that takes parameters from the user in a user-friendly menu.
    Intended for use as part of the MOS Acquisition software for aligning
    MOIRCS.
    """
    
    def __init__(self, manager):
        """
        Class constructor
        @param manager:
            The MESOffset plugin that this class communicates with
        """
        manager.initialise(self)
        
        # attributes
        self.get_value = []     # getter methods for all parameters
        self.set_value = []     # setter methods for all parameters
        
    
    
    def start(self):
        """
        Get user input so that we can start MES Locate/Analyze
        """
        # set the initial status message
        self.fv.showStatus("Waiting to start the MESOffset process.")
    
    
    def start_0_cb(self, *args):
        """
        Take the parameters from the mesoffset0 gui and go to page 1
        """
        # adjust parameters
        self.update_parameters(self.get_value[0])
        self.set_param('sky_chip1', self.get_param('star_chip1') + 2)
        if self.get_param('img_dir')[-1] != "/":
            self.set_param('img_dir', self.get_param('img_dir') + "/")
        self.set_defaults(1)
        
        # go to the MESOffset1 page
        self.log("Going to MES Offset 1...")
        self.manager.go_to_gui('epar 1')
    
    
    def start_1_cb(self, *args):
        """
        Begin mesoffset1 with the current parameters
        """
        self.update_parameters(self.get_value[1])
        self.manager.begin_mesoffset1()
    
    
    def start_2_cb(self, *args):
        """
        Begin mesoffset2 with the current parameters
        """
        self.update_parameters(self.get_value[2])
        self.manager.begin_mesoffset2()
    
    
    def start_3_cb(self, *args):
        """
        Begin mesoffset3 with the current parameters
        """
        self.update_parameters(self.get_value[3])
        self.manager.begin_mesoffset3()
    
    
    def get_param(self, name):
        """
        Returns the global parameter of the given name
        @param name:
            The name of the variable
        @returns:
            The current value of the variable
        """
        return self.manager.globals[name]
    
    
    def set_param(self, name, val): 
        """
        Assigns a value of val to the global parameter of the given name
        @param name:
            The name of the variable
        @param val:
            The new value of the variable
        """
        self.manager.globals[name] = val
    
    
    def update_parameters(self, getters):
        """
        Reads parameter values from getters and saves them in self.manager
        @param getters:
            The dictionary of getter methods for parameter values
        """
        new_params = {key:get_val() for key, get_val in getters.items()}
        self.manager.globals.update(new_params)
        
        
    def set_defaults(self, page_num):
        """
        Sets the default values for the gui on page page_num
        @param page_num:
            The number for the GUI whose defaults we must set
        """
        setters = self.set_value[page_num]
        for key in setters:
            if self.manager.globals.has_key(key):
                setters[key](self.manager.globals[key])
    
    
    def go_to_page(self, page_num):
        """
        Take the user to the interface for mesoffset{page_num}, and fills in
        default values
        @param page_num:
            The index of this mesoffset
        """
        print("GO TO PAGE")
        raise Exception("Test")
        setters = self.set_value[page_num]
        for key in setters:
            if self.manager.globals.has_key(key):
                setters[key](self.manager.globals[key])
            setters[key](17)
        self.stack.set_index(page_num)
        
        
    def log(self, text, *args, **kwargs):
        """
        Print text to the logger TextArea
        @param text:
            The string to be logged
        """
        self.logger.info(text.strip(), *args, **kwargs)
        self.log_textarea.append_text(text+"\n", autoscroll=True)
        self.fv.process_events()
        
        
    def gui_list(self, orientation='vertical'):
        """
        Combine the GUIs necessary for the interface part of this plugin
        Must be implemented for each MESPlugin
        @param orientation:
            Either 'vertical' or 'horizontal', the orientation of this new GUI
        @returns:
            A list of tuples with strings (names) and Widgets (guis)
        """
        return [('epar 0', self.make_gui_epar(0, self.start_0_cb, orientation)),
                ('epar 1', self.make_gui_epar(1, self.start_1_cb, orientation)),
                ('epar 2', self.make_gui_epar(2, self.start_2_cb, orientation)),
                ('epar 3', self.make_gui_epar(3, self.start_3_cb, orientation)),
                ('log',    self.make_gui_log(orientation))]
        
        
    def make_gui_epar(self, idx, process, orientation='vertical'):
        """
        Construct a GUI for the parameter menu, which prepares to launch process
        @param idx:
            The index of this MESOffset process
        @param process:
            The function that the GO! button will call
        @param orientation:
            Either 'vertical' or 'horizontal', the orientation of this new GUI
        @returns:
            A Widgets.Box object containing all necessary buttons, labels, etc.
        """
        name = "MES Offset {}".format(idx)
        # start by creating the container
        gui = Widgets.Box(orientation=orientation)
        gui.set_spacing(4)
        
        # fill a text box with brief instructions and put in in an expander
        exp = Widgets.Expander(title="Instructions")
        gui.add_widget(exp)
        txt = Widgets.TextArea(wrap=True, editable=False)
        txt.set_font(self.manager.body_font)
        txt.set_text("Use the widgets below to specify the parameters for "+
                     name+". Hover over each one to get a description of "+
                     "what it means. When you are finished, press the 'Go!' "+
                     "button, which will begin "+name+".")
        exp.set_widget(txt)
        
        # chose the params
        if idx == 0:
            params = params_0
        elif idx == 1:
            params = params_1
        elif idx == 2:
            params = params_2
        elif idx == 3:
            params = params_3

        # create a grid to group the different controls
        frm = Widgets.Frame(name)
        gui.add_widget(frm)
        grd, getters, setters = self.build_control_layout(params)
        self.get_value.append(getters)
        self.set_value.append(setters)
        frm.set_widget(grd)
        
        # the go button is important
        btn = Widgets.Button("Go!")
        btn.add_callback('activated', process)
        gui.add_widget(btn)
        
        # space appropriately and return
        gui.add_widget(Widgets.Label(''), stretch=True)
        return gui
        
        
    def make_gui_log(self, orientation='vertical'):
        """
        Construct a GUI for the second step: cropping the stars
        @param orientation:
            Either 'vertical' or 'horizontal', the orientation of this new GUI
        @returns:
            A Widgets.Box object containing all necessary buttons, labels, etc.
        """
        # start by creating the container
        gui = Widgets.Box(orientation=orientation)
        gui.set_spacing(4)
        
        # label the log
        lbl = Widgets.Label("Please wait...")
        lbl.set_font(self.manager.header_font)
        gui.add_widget(lbl)

        # the only thing here is a gigantic text box
        txt = Widgets.TextArea(wrap=False, editable=False)
        txt.set_font(self.manager.body_font)
        txt.set_text("\n"*100)
        gui.add_widget(txt, stretch=True)
        self.log_textarea = txt
        
        return gui
    
    
    
    @staticmethod
    def build_control_layout(controls):
        """
        Build a grid full of labels on the left and input widgets on the right.
        @param controls:
            A list of dictionary where each dictionary has the keys 'name' (the
            name of the parameter), 'type' (string, number, etc.), 'default'
            (the starting value), 'desc' (the tooltip), possibly 'format' (puts
            labels on either side of the input), and possibly 'options' (the
            list of possible values, if type is 'combobox')
        @returns:
            A Widgets.Box containing controls for all of the layouts,
            and a dictionary whose keys are parameter names and whose values
            are functions to return those parameter values,
            and a dictionary whose keys are parameter names and whose values
            are functions to set those parameter values
        """
        grd = Widgets.GridBox(rows=len(controls), columns=4)
        grd.set_column_spacing(0)
        getters = {}
        setters = {}
        
        # put each of the controls in a row on the grid
        for i, param in enumerate(controls):
            name = param['name']
            # start by labelling the parameter
            lbl = Widgets.Label(param['label']+":  ", halign='right')
            lbl.set_tooltip(param['desc'])
            grd.add_widget(lbl, i, 0)
            
            # create a widget based on type
            if param['type'] == 'string':
                wdg = Widgets.TextEntry(editable=True)
                getters[name] = wdg.get_text
                setters[name] = wdg.set_text
            elif param['type'] == 'number':
                wdg = Widgets.SpinBox()
                wdg.set_limits(0, 99999999)
                getters[name] = wdg.get_value
                setters[name] = wdg.set_value
            elif param['type'] == 'choice':
                wdg = Widgets.ComboBox()
                for option in param['options']:
                    wdg.append_text(option)
                getters[name] = wdg.get_index
                setters[name] = wdg.set_index
            elif param['type'] == 'boolean':
                wdg = Widgets.CheckBox()
                getters[name] = wdg.get_state
                setters[name] = wdg.set_state
            else:
                raise TypeError("{} is not a valid parameter type.".format(
                                                                param['type']))
            wdg.set_tooltip(param['desc'])
            
            # insert a default, if necessary
            if param.has_key('default'):
                setters[name](param['default'])
            
            # surround the widget with text, if necessary
            if param.has_key('format'):
                format_str = param['format']
                idx = format_str.index('{}')
                prefix = format_str[:idx]
                suffix = format_str[idx+2:]
                if prefix:
                    grd.add_widget(Widgets.Label(prefix, 'right'), i, 1)    #TODO: can I vertically align these
                grd.add_widget(wdg, i, 2)
                if suffix:
                    grd.add_widget(Widgets.Label(suffix, 'left'), i, 3)
            else:
                grd.add_widget(wdg, i, 2)
                
        return grd, getters, setters

#END

