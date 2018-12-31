from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd


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

    # Historico de Funcionarios
    df_historico = pd.read_csv("./data/historia_funcionarios.csv", parse_dates=[2])

    # Usando pandas creo csv y guardo datos
    df_funcionarios_actuales = pd.DataFrame(funcionarios)

    # Logica comparacion
    df_ultimo_relevamiento = df_historico[df_historico.fecha == max(df_historico.fecha)]
    df_comparacion = pd.concat([df_historico, df_funcionarios_actuales])
    
    for cargo in cargos:
        df_tmp = df_comparacion[df_comparacion.cargo == cargo]
              
        if df_tmp.iloc[0].nombre != df_tmp.iloc[1].nombre:
            print("Entre {} y {} el cargo de {} cambio de {} a {}".format(df_tmp.iloc[0].fecha, df_tmp.iloc[1].fecha, cargo, df_tmp.iloc[0].nombre, df_tmp.iloc[1].nombre))
        else:
            print("Entre {} y {} el cargo {} se mantiene sin cambios.".format(df_tmp.iloc[0].fecha, df_tmp.iloc[1].fecha, cargo))

    pd.concat([df_historico, df_funcionarios_actuales]).to_csv("./data/historia_funcionarios.csv", index=False)
