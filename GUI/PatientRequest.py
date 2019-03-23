import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PatientTest import PatientTest
import make_classification as mc
import make_segmentation as ms

import nibabel as nib

class PatientRequest:
    
    def imageLoad(self, frame):
        image = nib.load(self.path + self.patient_id + '/' + '{patient_id}_{frame}.nii.gz'.format(patient_id=self.patient_id, frame=str(frame))) 
        return image
    
    def loadMasks(self):
        isED = os.path.isfile(self.path + self.patient_id + '/{patient_id}_ED.nii.gz'.format(patient_id=self.patient_id))
        isES = os.path.isfile(self.path + self.patient_id + '/{patient_id}_ES.nii.gz'.format(patient_id=self.patient_id))
        
        if isED and isES:
            ED = self.imageLoad('ED')
            ES = self.imageLoad('ES')
        elif isED and not isES:
            ED = self.imageLoad('ED')
            ES = ms.makePrediction(self.path, self.patient_id)[1]
        elif isES and not isED:
            ED = ms.makePrediction(self.path, self.patient_id)[0]
            ES = self.imageLoad('ES')
        else:
            ED, ES = ms.makePrediction(self.path, self.patient_id)
            
        return ED, ES
    
    def getResultsPred(self):
        
        infoPat, patientDf = mc.makePrediction(self.patient)
        
        mc.saveInfo(patientDf, os.path.join(self.path, self.patient_id), self.patient.patient_id)
        
        return infoPat
    
    
    def __init__(self, path, patient_id):
        
        self.path = path
        self.patient_id = patient_id
        
        
        self.ori = self.imageLoad('4d')
        
        self.ED, self.ES = self.loadMasks()
        
        self.patient = PatientTest(path=path, patient_id=patient_id)
        infoPred = self.getResultsPred()
        self.patologyDict = infoPred