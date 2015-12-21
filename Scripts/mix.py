#coding: UTF-8

import numpy as np

ids = np.loadtxt('SPHERE_IDS',dtype=[('ID',int)])
atoms = np.loadtxt( 'SPHERE_ATOMS',
                    dtype=[   ('Type',int),
                              ('X',float),
                              ('Y',float),
                              ('Z',float),
                              ('VX',float),
                              ('VY',float),
                              ('VZ',float)],
                    usecols=[1,2,3,4,5,6,7])

lim = 0

for i,t in enumerate(ids):
	print   t[0], \
                atoms[i][0], \
                atoms[i][1]-25+20, \
                atoms[i][2]-25+85, \
                atoms[i][3]-25+175, \
                atoms[i][4], \
                atoms[i][5], \
                atoms[i][6]
	lim = i

lim+=1
lim2 = 0
for i in range(len(atoms)-lim):
	print   i+160001, \
                atoms[i+lim][0], \
                atoms[i+lim][1]-25+20, \
                atoms[i+lim][2]-25+85, \
                atoms[i+lim][3]-25+175, \
                atoms[i+lim][4], \
                atoms[i+lim][5], \
                atoms[i+lim][6]
	lim2 = i
