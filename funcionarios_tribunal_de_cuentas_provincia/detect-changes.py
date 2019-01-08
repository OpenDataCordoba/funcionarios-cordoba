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

def obtener_ultimo_relevamiento_cargos(listado_archivos):
    """Funcion lee y devuelve el ultimo relevamiento hecho. Performance al pedo."""
    ultimo_relevamiento = max([datetime.datetime.strptime(x, '%Y-%m-%d.csv') for x in listado_archivos])
    path_archivo = os.path.join(PATH_DATA, ultimo_relevamiento.date().isoformat() + ".csv")
    df_tmp = pd.read_csv(path_archivo, parse_dates=[2])
    return df_tmp

if __name__ == "__main__":
    # Obtener HTML
    r  = requests.get("http://www.tcpcordoba.gov.ar/tc/index.php/institucional/autoridades")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    # Obtener Datos
    nombre_presidente = soup.select("div.white_mainbox")[0].text.strip()
    nombre_vpmayoria = soup.select("div.white_box > div.txt")[0].text.strip()
    nombre_vpminoria = soup.select("div.white_box1 > div.txt")[0].text.strip()
    nombre_sdfl = soup.select("div.whitebox_item_solo")[0].text.strip()
    nombre_pdfl = soup.select("div.greybox_item")[0].text.strip()
    nombre_sdfp = soup.select("div.whitebox_item_solo")[1].text.strip()
    nombre_pdfp = soup.select("div.greybox_item")[1].text.strip()
    nombre_fiscalia = soup.select("div.whitebox_item_solo")[2].text.strip()

    # Funcionarios
    cargos = ["Presidente", "Vocal por la Mayoria", "Vocal por la Minoria", "Secretaria de Fiscalizacion Legal", "Prosecretaria de Fiscalizacion Legal", "Secretaria de Fiscalizacion Presupuestaria", "Prosecretaria de Fiscalizacion Presupuestaria", "Fiscalia"]

    funcionarios = dict(
        cargo = cargos,
        nombre = [nombre_presidente, nombre_vpmayoria, nombre_vpminoria, nombre_sdfl, nombre_pdfl, nombre_sdfp, nombre_pdfp, nombre_fiscalia],
        fecha = [str(datetime.date.today())] * 8
    )
    df_funcionarios_actuales = pd.DataFrame(funcionarios)

    
    # Logica comparacion
    listado_archivos = obtener_nombre_archivos_historicos()
    df_ultimo_relevamiento = obtener_ultimo_relevamiento_cargos(listado_archivos)

    df_comparacion = pd.concat([df_ultimo_relevamiento, df_funcionarios_actuales])

    print("Inicio de Comparacion para la Fecha: {}".format(datetime.date.today().isoformat()))
    
    for cargo in cargos:
        df_tmp = df_comparacion[df_comparacion.cargo == cargo]
              
        if df_tmp.iloc[0].nombre != df_tmp.iloc[1].nombre:
            print("Entre {} y {} el cargo de {} cambio de {} a {}".format(df_tmp.iloc[0].fecha, df_tmp.iloc[1].fecha, cargo, df_tmp.iloc[0].nombre, df_tmp.iloc[1].nombre))
        else:
            print("Entre {} y {} el cargo {} se mantiene sin cambios.".format(df_tmp.iloc[0].fecha, df_tmp.iloc[1].fecha, cargo))

    print("######## Fin Comparacion ###########")
    
    df_funcionarios_actuales.to_csv(os.path.join(PATH_DATA, datetime.date.today().isoformat() + '.csv'), index=False)
