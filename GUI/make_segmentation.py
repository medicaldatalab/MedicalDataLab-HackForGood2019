#!/home/ubuntu/anaconda3/envs t35

from Patient import Patient
import subprocess
import os
import shlex
import time

import nibabel as nib

def makePrediction(path, patient_id):
    final_path = os.path.join(path, patient_id + '/')
    
    command1 = "source activate t35"
    
    command2 = "python /home/ubuntu/ACDC_yeah/acdc_segmenter/evaluate_patients.py -s /home/ubuntu/ACDC_yeah/acdc_segmenter/experiments_settings {final_path} {patient_id}".format(final_path=final_path, patient_id=patient_id)
    
    result = subprocess.run(command1, stdout=subprocess.PIPE, shell=True)
    result = subprocess.run(command2, stdout=subprocess.PIPE, shell=True)
    
    ED_seg = nib.load(path + patient_id + '/' + '{patient_id}_ED.nii.gz'.format(patient_id=patient_id)) 
    ES_seg = nib.load(path + patient_id + '/' + '{patient_id}_ES.nii.gz'.format(patient_id=patient_id)) 
    
    return ED_seg, ES_seg