import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import nibabel as nib
from skimage.measure import label, regionprops

def separateMasks(mask_array): # Se añadirán las máscaras en el orden: RV, LV y Myo
    RV, LV, Myo = RV_mask_detection(mask_array), LV_mask_detection(mask_array), Myo_mask_detection(mask_array)
    
    separatedMask = [RV, LV, Myo]
    
    return separatedMask

def RV_mask_detection (mask_array):
    bool_array = mask_array == 1
    RV_array = bool_array.astype(int)
    return RV_array

def Myo_mask_detection (mask_array):
    bool_array = mask_array == 2
    Myo_array = bool_array.astype(int)
    return Myo_array

def LV_mask_detection (mask_array):
    bool_array = mask_array == 3
    LV_array = bool_array.astype(int)
    return LV_array

def getRatio(image):
    ratio = image.header['pixdim'][2] ** 2
    return ratio

def getSep(image):
    plane_sep = image.header['pixdim'][3]
    return plane_sep

def getExternalArea(image, all_masks, index):
    RV_a = all_masks[0][:,:, index]
    LV_a = all_masks[1][:,:, index]
    Myo_a = all_masks[2][:,:, index]
    
    try:
        RV_b = all_masks[0][:,:, index+1]
    except IndexError:
        RV_b = np.zeros(shape=all_masks[0][:,:, index].shape).astype(int)
        
    try:
        LV_b = all_masks[1][:,:, index+1]
    except IndexError:
        LV_b = np.zeros(shape=all_masks[1][:,:, index].shape).astype(int)
    
    try:
        Myo_b = all_masks[2][:,:, index+1]
    except IndexError:
        Myo_b = np.zeros(shape=all_masks[2][:,:, index].shape).astype(int)
    
    RV_sum = np.subtract(RV_a, RV_b)
    LV_sum = np.subtract(LV_a, LV_b)
    Myo_sum = np.subtract(Myo_a, Myo_b)
    
    RV_sub = np.subtract(RV_a, RV_b)
    LV_sub = np.subtract(LV_a, LV_b)
    Myo_sub = np.subtract(Myo_a, Myo_b)
    
    try:
        RV_external_area = regionprops(RV_sum)[0].area - regionprops(RV_sum)[0].area
    except IndexError:
        RV_external_area = 0
    
    try:
        LV_external_area = regionprops(LV_sum)[0].area - regionprops(LV_sum)[0].area
    except IndexError:
        LV_external_area = 0
    
    try:
        Myo_external_area = regionprops(Myo_sum)[0].area - regionprops(Myo_sum)[0].area
    except IndexError:
        Myo_external_area = 0
    
    return RV_external_area, LV_external_area, Myo_external_area



def calculate_volume(path, patient_id, frame):
    mask = nib.load(path + patient_id + '/' + '{patient_id}_{frame}.nii.gz'.format(patient_id=patient_id, frame=str(frame)))
                     
    mask_array = np.array(mask.dataobj)
                     
    all_masks = separateMasks(mask_array)
                     
    ratio = getRatio(mask)
    plane_sep = getSep(mask)
                     
    RV_volume_mm3 = 0
    Myo_volume_mm3 = 0
    LV_volume_mm3 = 0
                     
    for i in range(0, mask_array.shape[2]):
        RV_array = all_masks[0]
        LV_array = all_masks[1]
        Myo_array = all_masks[2]
                     
        try:
            RV_area = regionprops(RV_array[:,:,i])[0].area
        except:
            RV_area = 0
                                         
        try:
            Myo_area = regionprops(Myo_array[:,:,i])[0].area
        except:
            Myo_area = 0
                                                         
        try:
            LV_area = regionprops(LV_array[:,:,i])[0].area
        except:
            LV_area = 0
                                                                         
        RV_area_mm2 = RV_area * ratio
        Myo_area_mm2 = Myo_area * ratio
        LV_area_mm2 = LV_area * ratio
        
        externalAreas = getExternalArea(mask, all_masks, i)
        
        RV_volume_mm3 = RV_volume_mm3 + (RV_area_mm2 + externalAreas[0]) * plane_sep
        Myo_volume_mm3 = Myo_volume_mm3 + (Myo_area_mm2 + externalAreas[1]) * plane_sep
        LV_volume_mm3 = LV_volume_mm3 + (LV_area_mm2 + externalAreas[2]) * plane_sep

    return LV_volume_mm3, RV_volume_mm3, Myo_volume_mm3
