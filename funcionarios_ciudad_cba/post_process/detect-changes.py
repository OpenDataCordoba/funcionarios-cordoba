"""
Detectar cambios en las oficinas
"""
import os
import csv
import copy

data_folder = 'data'


class FuncionarioCiudadCordoba(object):
    def __init__(self, nombre=None, dni=None, cargo_generico=None, cargo_ocupado=None, ministerio=None, web_url=None, foto_url=None):
        self.nombre = nombre 
        self.dni = dni
        self.cargo_generico = cargo_generico
        self.cargo_ocupado = cargo_ocupado
        self.ministerio = ministerio
        self.web_url = web_url
        self.foto_url = foto_url
        self.duplicado = False
        self.procesado = False

    def clean(self):
        self.nombre = ''
        self.dni = ''
        self.cargo_generico = ''
        self.cargo_ocupado = ''
        self.ministerio = ''
        self.web_url = ''
        self.foto_url = ''

    def __str__(self):
        return 'Nombre: {} ({}) Cargo: {} Secretaría {}'.format(self.nombre, self.dni, self.cargo_generico, self.ministerio)


class DataFile(object):
    
    def __init__(self):
        self.funcionarios = []
        self.debug = True
        self.filename = ''

    def load(self, filename):
        self.filename = filename
        if self.debug:
            print('***********\nINICIA ARCHIVO {}'.format(filename))
        f = open(filename, newline='')
        reader = csv.DictReader(f)
        for row in reader:
            # if self.debug: print(row)
            if row['funcionario'].strip().upper() == '':
                continue
            func = FuncionarioCiudadCordoba(nombre=row['funcionario'].strip().upper(),
                                                dni=row['DNI'],
                                                cargo_generico=row['cargo_generico'].strip().upper(),
                                                cargo_ocupado=row['cargo_ocupado'].strip().upper(),
                                                ministerio=row['ministerio'].strip().upper(),
                                                web_url=row['web_url'],
                                                foto_url='' if 'foto_url' not in row.keys() else row['foto_url'])
            if func.nombre != '':
                # hay cargos sin funcionario designado
                # detectar duplicados
                duplicados = [funcionario for funcionario in self.funcionarios if funcionario.dni == func.dni]
                for duplicado in duplicados:
                    func.duplicado = True
                    duplicado.duplicado = True

                self.funcionarios.append(func)
        
        print('*********** {} registros'.format(len(self.funcionarios)))

    
    def clone(self):
        new_data_file = DataFile()
        new_data_file.funcionarios = self.funcionarios

        return new_data_file
    
    def unprocess(self):
        # marcar como no procesado
        for funcionario in self.funcionarios:
            funcionario.procesado = False

    def compare(self, data_file):
        # comparar y ver personas que cambian de puesto
        #TODO ver cargos que aparecen y desaparecen
        #TODO hay casos de funcionarios que tiene dos cargos. Eliminar porque ensucian los datos
        
        nuevos = []  # aparecieron y no estaban
        repetidos = []  # vuelven a aparecer
        cambiaron = []  # sigue la misma persona pero en otro cargo
        muertos = []  # ya no están más
        # hay funcionarios duplicados, algunos son el mismo, otros podrían ser personas con el mismo nombre
        duplicados = []  
        
        self.unprocess()
        data_file.unprocess()

        funcionarios_no_duplicados = [funcionario for funcionario in self.funcionarios if funcionario.duplicado == False]
        print('Funcionarios a analizar {} de {} (se sacan duplicados)'.format(len(funcionarios_no_duplicados), len(self.funcionarios)))
        for funcionario_aca in funcionarios_no_duplicados:
            encontrado = False

            funcionarios = [funcionario for funcionario in data_file.funcionarios]  # if funcionario.procesado == False]
            for funcionario_otro in funcionarios:

                if funcionario_aca.dni == funcionario_otro.dni:
                    encontrado = True
                    if funcionario_aca.cargo_generico == funcionario_otro.cargo_generico:
                        repetidos.append({'este': funcionario_aca, 'otro': funcionario_otro})
                        if self.debug:
                            pass
                            # print('REPETIDO {}: \n {} \n {}'.format(self.filename, funcionario_aca, funcionario_otro))
                    else:
                        cambiaron.append({'este': funcionario_aca, 'otro': funcionario_otro})
                        print('CAMBIO {}: \n Nuevo {} \n Anterior {}'.format(self.filename, funcionario_aca, funcionario_otro))
                    
                    funcionario_aca.procesado = True
                    funcionario_otro.procesado = True

            if encontrado == False:
                nuevos.append({'este': funcionario_aca, 'otro': ''})
                print('NUEVO {}: {}'.format(self.filename, funcionario_aca))
        
        # los que quedaron sueltos
        # funcionarios_aca = [funcionario for funcionario in self.funcionarios if funcionario.procesado == False and funcionario.duplicado == False]
        funcionarios_otro = [funcionario for funcionario in data_file.funcionarios if funcionario.procesado == False and funcionario.duplicado == False]
        for funcionario in funcionarios_otro:
            muertos.append({'este': funcionario, 'otro': ''})
            print('Dejó el cargo {}: {}'.format(self.filename, funcionario))

        return nuevos, repetidos, cambiaron, muertos

# cargar todo en memoria
data_files = []
archivos_ordenados = sorted(os.listdir(data_folder))
for filename in archivos_ordenados:
    data_file = DataFile()
    data_file.load('{}/{}'.format(data_folder, filename))
    # si no es el primero buscar cambios
    if len(data_files) > 0:
        print('***********\nINICIO COMPARACION {} registros vs {} del anterior'.format(len(data_file.funcionarios), len(anterior.funcionarios) ))
        nuevos, repetidos, cambiaron, muertos = data_file.compare(anterior)
        if data_file.debug:
            print('***********\nFIN ARCHIVO {}: nuevos: {} repetidos: {} cambiaron: {} Dejaron el cargo: {}\n'.format(filename, len(nuevos), len(repetidos), len(cambiaron), len(muertos) ))
    data_files.append(data_file)
    anterior = data_file.clone()




