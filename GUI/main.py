from tkinter import *
from tkinter import filedialog
import os.path
from PIL import Image, ImageTk
from PatientRequest import PatientRequest
import matplotlib.pyplot as plt
import nibabel as nib
import time


class Application():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x200")


        self.root.resizable(width=False, height=False)
        self.root.title('Medical DataLab')

        self.ilogo = PhotoImage(file ="./images/logoCardio.png")

        self.titleBanner = Label(self.root, text="Medical DataLab", fg = "green", font = ("Helvetica", 64))
        self.titleBanner.pack()


        def fileopen():
            mriPath = filedialog.askopenfilename(initialdir = "/home/ubuntu/ACDC_yeah/acdc_data/test/", filetypes=[("Nifty images", "*.nii.gz")])
            
            if mriPath == '':
                return

            path, patientID = getPatientPathAndID(mriPath)
            patient = PatientRequest(path, patientID)
            
            showPatientResults(patient)

        def getPatientPathAndID(mriPath):
            patientPath, mriFileName = mriPath.rsplit('/', 1)
            patientIDArray = patientPath.rsplit('/', 1)
            path = patientIDArray[0] + '/'
            patientID = patientIDArray[1]
            
            return path, patientID

        button = Button(text="Open file", width = 30, command = fileopen).pack()

        def showPatientResults(patient):
            #resultsWindow = Tk()
            resultsWindow = Toplevel()
            resultsWindow.geometry('800x600')
            resultsWindow.resizable(width=False, height=False)
            resultsWindow.title('Resultados paciente ' + patient.patient_id)
                     
            
            cellNames = {'Volumen del VD sis':'red', 
                         'Volumen del VD dias':'red',
                         'Volumen del VI sis':'orange',
                         'Volumen del VI dias':'orange',
                         'Volumen del Mio sis':'lightgray',
                         'Volumen del Mio dias':'lightgray'}
            
            collectedVolumesData = [patient.patologyDict['sys_volume_RV_mL'], patient.patologyDict['dia_volume_RV_mL'],
                                    patient.patologyDict['sys_volume_LV_mL'], patient.patologyDict['dia_volume_LV_mL'], 
                                    patient.patologyDict['sys_volume_Myo_mL'], patient.patologyDict['dia_volume_Myo_mL']]
            
            collectedWeightAndHeight = [patient.patologyDict['height'], patient.patologyDict['weight']]
            
            deseasesResults = {'RV': patient.patologyDict['RV'],
                               'NOR': patient.patologyDict['NOR'],
                               'DCM': patient.patologyDict['DCM'],
                               'HCM': patient.patologyDict['HCM'],
                               'MINF': patient.patologyDict['MINF']}
            
            ED_array = patient.ED.get_data()
            ES_array = patient.ES.get_data()
            
            ED_img = Image.fromarray(ED_array[:,:,4]).convert('RGB')
            ES_img = Image.fromarray(ES_array[:,:,4]).convert('RGB')
            
            ED_img_path="{path}{patient_id}/{patient_id}_ED.png".format(path=patient.path, patient_id=patient.patient_id)
            ES_img_path="{path}{patient_id}/{patient_id}_ES.png".format(path=patient.path, patient_id=patient.patient_id)
           
            
            fig, axis = plt.subplots()
            axis.imshow(ED_array[:,:,4], cmap = "bone")
            fig.savefig(ED_img_path, format='png')
            
            fig, axis = plt.subplots()
            axis.imshow(ES_array[:,:,4], cmap = "bone")
            fig.savefig(ES_img_path, format='png')
            
            r = 1
            for c, colour in cellNames.items():
                Label(resultsWindow, text=c, bg=colour,relief=RIDGE,height=2,width=15).grid(row=r,column=0)
                Label(resultsWindow, text='%d mm^3'%collectedVolumesData[r-1], relief=SUNKEN,heigh=2,width=10).grid(row=r,column=1)
                r = r + 1

            r = 1
            for c, colour in {'Peso (Kg)':'violet', 'Altura (cm)':'lightblue'}.items():
                Label(resultsWindow, text=c, bg=colour,relief=RIDGE,height=2,width=15).grid(row=r,column=3)
                Label(resultsWindow, text='%s'%collectedWeightAndHeight[r-1], relief=SUNKEN,heigh=2,width=10).grid(row=r,column=4)
                r = r + 1

            r = 8
            for deseaseName, prob in deseasesResults.items():
                Label(resultsWindow, text=deseaseName, relief=RIDGE,height=2,width=15).grid(row=r,column=0, pady=10)
                Label(resultsWindow, text='%lf'%(prob*100), relief=SUNKEN,heigh=2,width=10).grid(row=r,column=1, pady=10)
                r = r + 1
            
           
            # IMAGES
            
            sis_window = Toplevel()
            sis_window.geometry('800x600')
            sis_window.resizable(width=False, height=False)
            sis_window.title('Systolic')
            
            ES_img = ImageTk.PhotoImage(file=ES_img_path)
            canvas = Canvas(sis_window, width=500, height=500)
            canvas.pack()
            canvas.create_image(20, 10, image=ES_img, anchor=NW)
            
            
            dia_window = Toplevel()
            dia_window.geometry('800x600')
            dia_window.resizable(width=False, height=False)
            dia_window.title('Diastolic')
            
            ED_img = ImageTk.PhotoImage(file=ED_img_path)
            canvas = Canvas(dia_window, width=500, height=500)
            canvas.pack()
            canvas.create_image(20, 10, image=ED_img, anchor=NW)
           
            time.sleep(3)
            resultsWindow.mainloop()


def main():
    app = Application()
    app.root.mainloop()
    return 0

if __name__ == '__main__':
    main()