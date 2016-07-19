#
# MESPinpoint.py -- a ginga plugin designed to help pinpoint a group of objects.
# Similar to MESLocate.py, but with more precision and no step 1
# Works in conjunction with mesoffset scripts for MOS Acquisition
#
# Justin Kunimune
#



# standard imports
import math
import sys

# local imports
from MESLocate import MESLocate

# ginga imports
from ginga import GingaPlugin
from ginga.gw import Widgets, Viewers, Plot
from ginga.util import iqcalc

# third-party imports
import numpy as np
from numpy import ma



# constants
# the arguments passed in to the outer script
argv = sys.argv
fits_image = argv[1]
input_coo = argv[2]
output_coo = argv[3]    #TODO: What do I have to output?
interact = argv[4]

# the object we are looking for
#mode = 'star' if 'star' in argv[1] else 'hole'
# the size of the object-finding squares (dependent on whether we look for holes or stars)
sq_size = 50
# the difference between the threshold and the mean, in standard deviations
#threshold_dist = 3 if mode == 'star' else -.2
# the colors of said squares
#colors = ('green','red','blue','yellow','magenta','cyan','orange')
# the different ways we can select things
selection_modes = ("Automatic", "Crop", "Mask")



class MESPinpoint(MESLocate):
    """
    A custom LocalPlugin for ginga that locates a set of calibration objects,
    asks for users to help locate anomolies and artifacts on its images
    of those objects, and then calculates their centers of masses. Intended
    for use as part of the MOS Acquisition software for aligning MOIRCS.
    """
    
    def start(self):    # TODO: output
        """
        Called when the plugin is invoked, right after build_gui()
        One of the required LocalPlugin methods
        """
        MESLocate.start(self)
        self.fitsimage.get_settings().set(autocut_method='minmax')
        self.step2_cb()
    
    
    def __str__(self):
        return "MESPinpoint"
    
    
    
    @staticmethod
    def readInputFile():
        """
        Reads the COO file and returns the position of the first active
        object as well as the relative positions of all the other objects in a list
        @returns:
            A tuple containing a list of float tuples representing relative
            locations and radii of objects, and a single float tuple (absolute
            location of first object)
        """
        # define variables
        obj_list = []
        obj0 = None
        
        # try to open the file
        try:
            coo = open(input_coo, 'r')
        except IOError:
            try:
                coo = open("sbr_elaisn1rev_mask.coo")
            except IOError:
                return [(dx, dy) for dx in [0,1,-1] for dy in [0,1,-1]], (0,0)
        
        # now parse it!
        line = coo.readline()
        while line != "":
            # for each line, get the important values and save them in obj_list
            vals = [float(word) for word in line.split()]
            if obj0 == None:
                obj_list.append((0, 0, vals[2]))
                obj0 = (vals[0], vals[1])
            else:
                obj_list.append((vals[0]-obj0[0],   # don't forget to shift it so object #0 is at the origin
                                 vals[1]-obj0[1],
                                 vals[2]))
            line = coo.readline()
            
        return obj_list, obj0
    
    
    @staticmethod
    def locate_obj(bounds, masks, image, viewer=None):
        return MESLocate.locate_obj(bounds, masks, image, viewer, True, 1)

#END

