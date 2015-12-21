#coding: UTF-8

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from scipy import optimize
import matplotlib.patches as mpatches
from numpy.lib.recfunctions import append_fields

#######################################

# Loading. GENERAL

#######################################
"""

 COMMAND:

  python MD_Plot.py file1 file2 [...]

 NOTE: 
 	Timestep = 0.001 ps !
 	Strain rate = 10^9 1/s !!
 	Change line #37 to match other configuration

"""

stress = []
# Change these to match your output file
COL_STEP = 0
COL_VMISES = 1
COL_PXX = 6
COL_PYY = 7
COL_PZZ = 8
COL_PXY = 9
COL_PXZ = 10
COL_PYZ = 11

for i,f in enumerate(sys.argv[1:]):
        # Use dummy column 1 to have that column present
        stress.insert(  i, \
                        np.loadtxt( sys.argv[i+1], \
                                    dtype=[ ('Strain',float), \
                                            ('vonMises',float), \
                                            ('Pxx',float), \
                                            ('Pyy',float), \
                                            ('Pzz',float), \
                                            ('Pxy',float), \
                                            ('Pxz',float), \
                                            ('Pyz',float)], \
                                    usecols=[   COL_STEP, \
                                                COL_VMISES, \
                                                COL_PXX, \
                                                COL_PYY, \
                                                COL_PZZ, \
                                                COL_PXY, \
                                                COL_PXZ, \
                                                COL_PYZ]))
        # Time in ps, (timestep = 0.001) / Strain in 1/s (strain rate = 10^9 1/s = 0.001 1/ps)
        stress[i]['Strain'] = np.subtract(  stress[i]['Strain'], \
                                            stress[i]['Strain'][0])*0.001*0.001

        # vonMises in bar
        stress[i]['vonMises'] = np.sqrt((0.5)*( (stress[i]['Pxx']-stress[i]['Pyy'])**2 + \
                                                (stress[i]['Pyy']-stress[i]['Pzz'])**2 + \
                                                (stress[i]['Pzz']-stress[i]['Pxx'])**2 + \
                                                6*( stress[i]['Pxy']**2+ \
                                                    stress[i]['Pyz']**2+ \
                                                    stress[i]['Pxz']**2)))

font = {'family' : 'serif',
        'color'  : 'black',
        'weight' : 'normal',
        'size'   : 24,
        }

fig = plt.figure()
a = fig.add_subplot(111)

# Set the tick labels font
for label in (a.get_xticklabels() + a.get_yticklabels()):
    label.set_fontname('serif')
    label.set_fontsize(font['size']-8)

# Change this. One temperature per file.
labels=['$10\,K$','$200\,K$','$300\,K$','$400\,K$'];
# Colors.
cols = ['#3232ff','#ff3232','#329932','#ff32ff']
for i in range(len(stress)):
	# vonMises in GPa (1 bar --> 0.0001 GPa)
	a.plot( stress[i]['Strain'], \
                stress[i]['vonMises']*0.0001, \
                color=cols[i], \
                label=labels[i], \
                ls='-',lw=2)

plt.xlabel('$\epsilon$',fontdict=font)
plt.ylabel('$\sigma{}_{VM} \; [GPa]$',fontdict=font)
plt.subplots_adjust(left=0.16,bottom=0.15)
a.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f'))
a.legend(loc='lower left',fontsize=font['size']-6)
plt.show()
