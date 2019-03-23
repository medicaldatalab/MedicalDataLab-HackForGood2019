from getVolume import calculate_volume
import collections

class PatientTest:
    def setInfoDict(self):
        total_path = self.path + '/' + self.patient_id + '/Info.cfg'
        lines = []
        with open(total_path) as f:
            lines = f.read().split('\n')

        d = {}
        for line in lines:
            if line != '':
                (key, val) = line.split(sep=': ')
                d[key] = str(val)
        return d
        
    def setWeight(self):
        return self.infoDict['Weight']
    
    def setHeight(self):
        return self.infoDict['Height']
    
    def setSysVolumes(self):
        # Hay que acabar primero el script para obtener los volúmenes
        LV, RV, Myo = calculate_volume(self.path, self.patient_id, 'ES')
        return LV / 1000, RV / 1000, Myo / 1000
    def setDiaVolumes(self):
        # Hay que acabar primero el script para obtener los volúmenes
        LV, RV, Myo = calculate_volume(self.path, self.patient_id, 'ED')
        return LV / 1000, RV / 1000, Myo / 1000
    
    def hasPatology(self):
        return self.infoDict.get('Group') is not None
    
    def setPatologies(self, patologiesDict):
        self.patologyDict = patologiesDict
    
    def set_ey_frac(self):
        ey_frac_LV = (self.dia_volume_LV - self.sys_volume_LV) / self.dia_volume_LV
        ey_frac_RV = (self.dia_volume_RV - self.sys_volume_RV) / self.dia_volume_RV  
        
        return ey_frac_LV, ey_frac_RV
    
    def __init__(self, path, patient_id, weight=None, height=None, sys_volumes=None, dia_volumes=None):
        self.path = path
        self.patient_id = patient_id
        
        self.infoDict = self.setInfoDict()
        
        if weight == None:
            self.weight = self.setWeight()
        else:
            self.weight = weight
            
        if height == None:
            self.height = self.setHeight()
        else:
            self.height = height
            
        if sys_volumes == None:
            self.sys_volume_LV, self.sys_volume_RV, self.sys_volume_Myo = self.setSysVolumes()
        else:
            self.sys_volume_LV = sys_volumes["LV"]
            self.sys_volume_RV = sys_volumes["RV"]
            self.sys_volume_Myo = sys_volumes["Myo"]
        
        if dia_volumes == None:
            self.dia_volume_LV, self.dia_volume_RV, self.dia_volume_Myo = self.setDiaVolumes()
        else:
            self.dia_volume_LV = dia_volumes["LV"]
            self.dia_volume_RV = dia_volumes["RV"]
            self.dia_volume_Myo = dia_volumes["Myo"]
         
        self.ey_frac_LV, self.ey_frac_RV = self.set_ey_frac()

            
    def __str__(self):
        return "("+str(self.patient_id)+":"+str(self.weight)+":"+str(self.height)+")"
    
    def toDict(self):
        key_value_pairs = [("patient_id", self.patient_id),
                           ("height", self.height),
                           ("weight", self.weight),
                           ("sys_volume_RV_mL", self.sys_volume_RV),
                           ("sys_volume_LV_mL", self.sys_volume_LV),
                           ("sys_volume_Myo_mL", self.sys_volume_Myo),
                           ("dia_volume_RV_mL", self.dia_volume_RV),
                           ("dia_volume_LV_mL", self.dia_volume_LV),
                           ("dia_volume_Myo_mL", self.dia_volume_Myo),
                           ("ey_frac_LV", self.ey_frac_LV),
                           ("ey_frac_RV", self.ey_frac_RV)]
        
        patient_dict = collections.OrderedDict(key_value_pairs)
        
        return patient_dict
        