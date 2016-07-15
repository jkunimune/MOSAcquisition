#!/usr/bin/env python

#
# mes_plot.py -- a script that starts Ginga with the MESAnalyze plugin running
# Works in conjunction with mesoffset scripts for MOS Acquisition
#
# Justin Kunimune
#

import ginga.main

import sys
argv = sys.argv

if len(argv) < 3:
    print("usage: mes_plot( FITS_image_name, input_coo_filename )")
    quit()

ginga.main.reference_viewer(['$HOME/Install/bin/ginga',
                             argv[1],
                             '--plugins=MESAnalyze'])

#END

