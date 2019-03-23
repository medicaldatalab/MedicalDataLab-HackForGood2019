import pandas as pd
import csv
import os, sys
from Patient import Patient

def main(args):
    path_patient = args[0]
    outputName = args[1]
    
    patient_id_list = os.listdir(path_patient)
    
    patient_list = []
    for patient_id in patient_id_list:
        if patient_id.startswith('patient'):
            patient_list.append(Patient(path=path_patient, patient_id=patient_id))
    
    patientsDf = pd.DataFrame(columns = patient_list[0].toDict().keys())

    for patient in patient_list:
        patientsDf = patientsDf.append(patient.toDict(), ignore_index=True)
        
    final_df = patientsDf.sort_values(by='patient_id')
    final_df.to_csv("./data/{output_Name}.csv".format(output_Name=outputName))

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except IndexError:
        print("Error, introduce como argumentos la ruta de los pacientes y el nombre del dataset de destino.")