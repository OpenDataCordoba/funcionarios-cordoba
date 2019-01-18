from bs4 import BeautifulSoup
import requests
import datetime
import os
import pandas as pd

PATH_DATA = os.path.join(".","post-process","data")

def obtener_nombre_archivos_historicos():
    """Funcion para obtener el listado de archivos csv que almacenan los cargos historicos."""    
    archivos_historicos = []
    
    for _, _, files in os.walk(PATH_DATA):
        for fname in files:
            archivos_historicos.append(fname)
            
    return(archivos_historicos)

def obtener_datos_relevamiento(file_path):
    """Funcion lee y devuelve el relevamiento hecho para el archivo dado"""
    path_archivo = os.path.join(PATH_DATA, file_path)
    df_tmp = pd.read_csv(path_archivo)
    return df_tmp

if __name__ == "__main__":
    # Asume que los nombres de los csv se pueden ordenar de mas viejo a mas nuevo.
    relevamientos = sorted(obtener_nombre_archivos_historicos())
    archivo_funcionarios_actuales = relevamientos[-1]
    df_funcionarios_actuales = obtener_datos_relevamiento(archivo_funcionarios_actuales)
    archivo_ultimo_relevamiento = relevamientos[-2]
    df_ultimo_relevamiento = obtener_datos_relevamiento(archivo_ultimo_relevamiento)

    # Logica comparacion
    df_comparacion = pd.concat([df_ultimo_relevamiento, df_funcionarios_actuales])
    print("Inicio de Comparacion para la Fecha: {}".format(datetime.date.today().isoformat()))
    
    cargos = ["Presidente", "Vocal por la Mayoria", "Vocal por la Minoria", "Secretaria de Fiscalizacion Legal", "Prosecretaria de Fiscalizacion Legal", "Secretaria de Fiscalizacion Presupuestaria", "Prosecretaria de Fiscalizacion Presupuestaria", "Fiscalia"]
    for cargo in cargos:
        df_tmp = df_comparacion[df_comparacion.cargo_ocupado == cargo]
              
        if df_tmp.iloc[0].funcionario != df_tmp.iloc[1].funcionario:
            print("Entre {} y {} el cargo de {} cambio de {} a {}".format(archivo_ultimo_relevamiento, archivo_funcionarios_actuales, cargo, df_tmp.iloc[0].funcionario, df_tmp.iloc[1].funcionario))
        else:
            print("Entre {} y {} el cargo {} se mantiene sin cambios.".format(archivo_ultimo_relevamiento, archivo_funcionarios_actuales, cargo))

    print("######## Fin Comparacion ###########")
