import csv
from datetime import datetime
from os import path, makedirs
import logging

from funcionarios_tribunal_de_cuentas_provincia.client import FuncionariosTribunalDeCuentasProvincia


class ResultsHandler(object):
    def __init__(self):
        # Define paths
        self.base_path = path.dirname(path.dirname(__file__))
        self.pp_path = path.join(self.base_path, 'post_process')

        # Configure logging
        logging.basicConfig(
            filename=path.join(self.base_path, 'all.log'),
            level=logging.INFO,
            format='%(asctime)s %(levelname)s:%(message)s'
        )

        # Run
        self.client = FuncionariosTribunalDeCuentasProvincia()
        self.results = self.client.get_employees()
        self.parse_results()
        self.save_to_csv()

    def parse_results(self):
        setattr(self, 'parsed_results', self.results)

    def save_to_csv(self):
        logging.info('Savig file')
        file_name = 'funcionarios-{:%Y-%m-%d}.csv'.format(datetime.now())
        file_path = path.join(self.pp_path, 'data', file_name)

        keys = ['funcionario', 'DNI', 'cargo_generico', 'cargo_ocupado', 'foto_img', 'foto_url', 'secretaria', 'web_url']
        funcionarios = getattr(self, 'parsed_results', [])

        print(list(zip(*[funcionarios[key] for key in keys])))

        with open("test.csv", "wb") as outfile:
            writer = csv.writer(outfile, delimiter = "\t")
            writer.writerow(keys)
            writer.writerows([list(row) for row in zip(*[funcionarios[key] for key in keys])])


if __name__ == '__main__':
    ResultsHandler()
