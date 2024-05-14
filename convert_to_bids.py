#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:23:47 2024

@author: jstout
"""

import glob
import mne_bids
import mne
from mne_bids import BIDSPath, write_raw_bids, write_anat
import os, os.path as op
import pandas as pd
import sys

topdir = '/fast2/ECP'  #Change this to the ECP MEG working dir
bids_root = op.join(topdir, 'BIDS')
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

errors={}
dframe = pd.DataFrame(columns=['subject','path','task','run'])

for i in fnames:
    idx = len(dframe)
    base = op.basename(i)
    fparts = base.split('_')   
    
    dframe.loc[idx, 'path'] = i
    dframe.loc[idx, 'subject'] = fparts[0].lower()
    dframe.loc[idx, 'task'] = fparts[1]
    
    tmp_ = fparts[2].strip('run')
    dframe.loc[idx, 'run'] = str(int(tmp_))  #strip off leading zeros

#Make sure that the subject ID is consistent    
assert set(dframe.subject.values).__len__() == 1  

#Add anatomical info
dframe['mri'] = op.join(topdir, subject, 'Anatomy', 'mri', 'T1.mgz') 
dframe['trans_fname'] = op.join(topdir, subject, 'Anatomy', 'Anatomy-trans.fif')

    
#%% Convert MEG Data to bids

errors=[]
for idx, row in dframe.iterrows():
    try:
        raw = mne.io.read_raw_fif(row.path, allow_maxshield=True)  
        raw.info['line_freq'] = 60 
        ses = '1'
        bids_path = BIDSPath(subject=row.subject, session='1', task=row.task,
                              run=row.run, root=bids_root)
        
        # Events ===  FIX!! - need to add an events parser
        write_raw_bids(raw, bids_path, overwrite=True, anonymize=True)
    except BaseException as e:
        errors.append(row.path)
        errors.append(str(e))
        
dframe.to_csv(op.join(logdir, f'{subject}_dataframe.csv'))    
#%% Convert MRI to BIDS w/coreg

#Strip out emptyrooms 
dframe = dframe.loc[dframe.task.str.lower().str[0:2]!='er']
row = dframe.iloc[0]

raw = mne.io.read_raw_fif(row.path, allow_maxshield=True)
trans = mne.read_trans(row.trans_fname)

t1w_bids_path = \
    BIDSPath(subject=row.subject, session='1', root=bids_root, suffix='T1w')

# Each subject has its own subjects_dir.  All fs_subjectIDs are Anatomy
landmarks = mne_bids.get_anat_landmarks(
    image=row.mri, 
    info=raw.info,
    trans=trans,
    fs_subject='Anatomy',
    fs_subjects_dir=op.join(topdir, subject)
    )

# Write MRI bids
t1w_bids_path = write_anat(
    image=row.mri,
    bids_path=t1w_bids_path,
    landmarks=landmarks,
    deface=False, 
    overwrite=True
    )

#%% Write output logs

    
    



    
    

        

        
        
    
        
    
