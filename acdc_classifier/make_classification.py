import pandas as pd
from sklearn.externals import joblib
from Patient import Patient

def patient_to_dataframe(patient):
    patientDf = pd.DataFrame(columns = patient.toDict().keys())
    patientDf = patientDf.append(patient.toDict(), ignore_index=True)
    patientDf = patientDf.drop(patientDf.columns[0], axis = 1)
    patientDf = patientDf.drop(patientDf.columns[-1], axis = 1)

    return patientDf

def dfToDict(patientDf):
    d = {}
    
    d['height'] = patientDf['height']
    d['weight'] = patientDf['weight']
    d['sys_volume_RV_mL'] = patientDf['sys_volume_RV_mL']
    d['sys_volume_LV_mL'] = patientDf['sys_volume_LV_mL']
    d['sys_volume_Myo_mL'] = patientDf['sys_volume_Myo_mL']
    d['dia_volume_RV_mL'] = patientDf['dia_volume_RV_mL']
    d['dia_volume_LV_mL'] = patientDf['dia_volume_LV_mL']
    d['dia_volume_Myo_mL'] = patientDf['dia_volume_Myo_mL']
    d['ey_frac_LV'] = patientDf['ey_frac_LV']
    d['ey_frac_RV'] = patientDf['ey_frac_RV']
    d['sys_volume_RV_mL'] = patientDf['sys_volume_RV_mL']
    d['sys_volume_LV_mL'] = patientDf['sys_volume_LV_mL']
    d['sys_volume_Myo_mL'] = patientDf['sys_volume_Myo_mL']
    d['patology'] = patientDf['patology']
    
    return d

def saveInfo(patientDf, path, output_Name):
     patientDf.to_csv("path/{output_Name}_info.csv".format(output_Name=outputName))
        
        
def makePrediction(patient):
    rf = joblib.load('./random_forest.pkl')

    patientDf = patient_to_dataframe(patient)
    patientDf['Patology'] = rf.predict(patientDf)
    
    infoDict = dfToDict(patientDf)
    
    return infoDict, patientDf