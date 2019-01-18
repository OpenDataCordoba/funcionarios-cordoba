from bs4 import BeautifulSoup
import requests
import datetime


class FuncionariosTribunalDeCuentasProvincia(object):

    @staticmethod
    def _get(url):
        return requests.get(url)
        
    def get_employees(self):
        url = "http://www.tcpcordoba.gov.ar/tc/index.php/institucional/autoridades"
        response =  self._get(url)
        data = response.text
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

        # Datos: ['funcionario', 'DNI', 'cargo_generico', 'cargo_ocupado', 'foto_img', 'foto_url', 'secretaria', 'web_url'] 
        funcionarios = dict(
            funcionario = [nombre_presidente, nombre_vpmayoria, nombre_vpminoria, nombre_sdfl, nombre_pdfl, nombre_sdfp, nombre_pdfp, nombre_fiscalia],
            DNI = [""] * 8,
            cargo_generico = [""] * 8,
            cargo_ocupado = cargos,
            foto_img = [""] * 8,
            foto_url = [""] * 8,
            secretaria = [""] * 8,
            web_url = [""] * 8
        )

        return funcionarios
