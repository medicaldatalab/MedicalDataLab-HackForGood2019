import pandas as pd
from sklearn.externals import joblib
from Patient import Patient

def patient_to_dataframe(patient):
    patientDf = pd.DataFrame(columns = patient.toDict().keys())
    patientDf = patientDf.append(patient.toDict(), ignore_index=True)
    patientDf = patientDf.drop(patientDf.columns[0], axis = 1)

    return patientDf

def dfToDict(patientDf, patologiesList):
    d = {}
    
    patientDf = patientDf.loc[0]
    
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
    
    patologyDict = {}
    
    patologyDict['DCM'] = patologiesList[0]
    patologyDict['HCM'] = patologiesList[1] 
    patologyDict['MINF'] = patologiesList[2]
    patologyDict['NOR'] = patologiesList[3]  
    patologyDict['RV'] = patologiesList[4]  
   
    d.update(patologyDict)
    
    return d

def saveInfo(patientDf, path, output_Name):
     patientDf.to_csv("{path}{output_Name}_info.csv".format(path=path, output_Name=output_Name))
        
        
def makePrediction(patient):
    rf = joblib.load('./random_forest.pkl')

    patientDf = patient_to_dataframe(patient)
    patologiesList = rf.predict_proba(patientDf)
    
    infoDict = dfToDict(patientDf, patologiesList[0])
    
    patologiesDf = pd.DataFrame(columns = infoDict.keys())
    patologiesDf = patologiesDf.append(infoDict, ignore_index=True)
    
    patientDf = pd.concat([patientDf, patologiesDf], axis=1)
    
    return infoDict, patientDf