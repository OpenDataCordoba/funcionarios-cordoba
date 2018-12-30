from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd
from pathlib import Path
import os


class Funcionario:
    def __init__(self, cargo, fecha, nombre):
        self.cargo = cargo
        self.fecha = fecha
        self.nombre = nombre    

    def __str__(self):
        return "A la fecha {}, el {} es {}".format(self.fecha, self.cargo, self.nombre)


if __name__ == "__main__":
    # Obtener HTML
    r  = requests.get("http://www.tcpcordoba.gov.ar/tc/index.php/institucional/autoridades")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    # Obtener Datos
    fecha_scrapping = datetime.date.today()
    nombre_presidente = soup.select("div.white_mainbox")[0].text.strip()
    nombre_vpmayoria = soup.select("div.white_box > div.txt")[0].text.strip()
    nombre_vpminoria = soup.select("div.white_box1 > div.txt")[0].text.strip()
    nombre_sdfl = soup.select("div.whitebox_item_solo")[0].text.strip()
    nombre_pdfl = soup.select("div.greybox_item")[0].text.strip()
    nombre_sdfp = soup.select("div.whitebox_item_solo")[1].text.strip()
    nombre_pdfp = soup.select("div.greybox_item")[1].text.strip()
    nombre_fiscalia = soup.select("div.whitebox_item_solo")[2].text.strip()

    # Crear Funcionarios
    presidente = Funcionario("Presidente", fecha_scrapping, nombre_presidente)
    print(presidente)    
    vpmayoria = Funcionario("Vocal por la Mayoria", fecha_scrapping, nombre_vpmayoria)
    print(vpmayoria)
    vpminoria = Funcionario("Vocal por la Minoria", fecha_scrapping, nombre_vpminoria)
    print(vpminoria)
    sdfl = Funcionario("Secretaria de Fiscalizacion Legal", fecha_scrapping, nombre_sdfl)
    print(sdfl)
    pdfl = Funcionario("Prosecretaria de Fiscalizacion Legal", fecha_scrapping, nombre_pdfl)
    print(pdfl)
    sdfp = Funcionario("Secretaria de Fiscalizacion Presupuestaria", fecha_scrapping, nombre_sdfp)
    print(sdfp)
    pdfp = Funcionario("Prosecretaria de Fiscalizacion Presupuestaria", fecha_scrapping, nombre_pdfp)
    print(pdfp)
    fiscalia = Funcionario("Fiscalia", fecha_scrapping, nombre_fiscalia)
    print(fiscalia)

    # Funcionarios
    funcionarios = dict(
        cargo = ["Presidente", "Vocal por la Mayoria", "Vocal por la Minoria", "Secretaria de Fiscalizacion Legal", "Prosecretaria de Fiscalizacion Legal", "Secretaria de Fiscalizacion Presupuestaria", "Prosecretaria de Fiscalizacion Presupuestaria", "Fiscalia"],
        nombre = [nombre_presidente, nombre_vpmayoria, nombre_vpminoria, nombre_sdfl, nombre_pdfl, nombre_sdfp, nombre_pdfp, fiscalia],
        fecha = [str(datetime.date.today())] * 8
    )

    # Historico de Funcionarios
    df_historico = pd.read_csv("./data/historia_funcionarios.csv")
    
    # Usando pandas creo csv y guardo datos
    df_funcionarios = pd.DataFrame(funcionarios)
    
