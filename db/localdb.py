import json
import os

class Database:
    def __init__(self, data_folder):
        self.DataFolder = data_folder
        if not os.path.exists(self.DataFolder):
            os.makedirs(self.DataFolder)
    
    def validar_archivos(self, jsonfile):
        file_loc = os.path.join(self.DataFolder, jsonfile)
        if not os.path.exists(file_loc):
            with open(file_loc, 'w') as file:
                json_data = []
                json.dump(json_data, file, indent=4)

    def load_file(self, jsonfile):
        file_loc = os.path.join(self.DataFolder, jsonfile)

        self.validar_archivos(jsonfile)

        with open(file_loc, 'r') as file:
            datos = json.load(file)
        return datos

    def save_file(self, jsonfile, jsondata):
        fileloc = os.path.join(self.DataFolder, jsonfile)
        with open(fileloc, 'w') as file:
            json.dump(jsondata, file, indent=4)
    
    def obtener_id_ai(self, jsonfile, param_name='id'):
        json_data = self.load_file(jsonfile)
        max_param = 0
        if json_data:
            for elemento in json_data:
                elem_id = int(elemento[param_name])
                if elem_id > max_param:
                    max_param = elem_id
            max_param += 1
        else:
            max_param = 0
        return max_param
