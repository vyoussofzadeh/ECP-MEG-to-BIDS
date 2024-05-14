#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:23:47 2024

@author: jstout
"""

import glob
import mne_bids
import mne
import os, os.path as op
import pandas as pd
import sys

topdir = '/fast2/ECP'  #Change this to the ECP MEG working dir
subject = sys.argv[1]

logdir = op.join(topdir, 'bids_logs')
if not op.exists(logdir): os.mkdir(logdir)
os.chdir(op.join(topdir, subject))


trans_fname = op.join(topdir, subject, 'Anatomy', 'Anatomy-trans.fif')
t1w_fname = op.join(topdir, subject, 'Anatomy', 'mri', 'T1.mgz') 
raw_dir = op.join(topdir, subject, 'Raw')


meg_expected = {'ERNoise': 2, 
                'PN': 2, 
                'RestEC': 2, 
                'RestEO':3, 
                'SD': 2,
                'SM':2
                }

meg_actual = {'ERNoise': 0, 
                'PN': 0, 
                'RestEC': 0, 
                'RestEO':0, 
                'SD': 0,
                'SM':0
                }

fnames = glob.glob(op.join(raw_dir, '*raw.fif'))

outlog = [f'#########  {subject}   ##############']
outlog.append('MEG Dataset Checks::')
errors={}
for i in fnames:
    print(i)
    base = op.basename(i)
    fparts = base.split('_')
    fparts[0]=='ec'+subject
    task = fparts[1]
    if task not in meg_expected.keys():
        outlog.append(f'{base} is not part of the standard tasks')
        errors[i] = f'{base} is not part of the standard task naming'
    else:
        meg_actual[task]+=1
    run = fparts[2]
    if run[0:3].lower() != 'run':
        outlog.append(f'Naming convention on run wrong: {run}')



        
#%% Check for correct numbers 
outlog.append('###############')
outlog.append('###############')
outlog.append('Dataset Counts:::')
for key in meg_expected.keys():
    if meg_expected[key] == meg_actual[key]:
        outlog.append(f'{subject} : task {key} : PASSED ')
    if int(meg_expected[key]) > int(meg_actual[key]):
        outlog.append(f'{subject} : task {key} : actual, {meg_actual[key]} < expected, {meg_expected[key]}  ')

outlog.append('###############')
outlog.append('###############')

if not op.exists(trans_fname):
    outlog.append('No transform located at: {trans_fname}')
else:
    outlog.append('Transform found: PASS')
if not op.exists(t1w_fname):
    outlog.append('No T1w in the fresurfer folder: {t1w_fname}')
else:
    outlog.append('T1w found: PASS')

logfile = op.join(logdir, f'{subject}_log.txt')
outlog = [i+'\n' for i in outlog]
with open(logfile, 'w') as f:
    f.writelines(outlog)
    
    

        

        
        
    
        
    
