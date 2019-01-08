import csv
from datetime import datetime
from os import path, makedirs
import logging

from funcionarios_ciudad_cba.client import FuncionariosCiudad


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
        self.client = FuncionariosCiudad()
        self.results = self.client.get_employees()
        self.parse_results()
        self.save_to_csv()

    def process_images(self, foto_result):
        images_data = []
        base_path = path.join(self.pp_path, 'imagenes')

        for key, url in foto_result.items():
            image_name = url.split('/')[-1]
            relative_path = path.join(key, image_name)
            full_path = path.join(base_path, relative_path)

            if not path.exists(full_path):
                logging.info('Get image from {}'.format(url))
                makedirs(path.dirname(full_path), exist_ok=True)
                with open(full_path, 'wb') as image_file:
                    image_response = self.client.get_image(url)
                    image_file.write(image_response)

            images_data.append(
                {'url': url, 'path': relative_path}
            )
        return images_data

    def parse_results(self):
        logging.info('Parsing results')
        rows = [['cargo_generico', 'cargo_ocupado', 'foto_img', 'foto_url', 'funcionario', 'ministerio', 'web_url']]
        for result in self.results:
            logging.info('Parsing funcionario id: {}'.format(result['id']))
            rows.append([
                result['cargo']['oficina'],
                result['cargo']['nombre'],
                self.process_images(result['funcionario']['foto']),
                result['funcionario'].get('foto', {}).get('original', ''),
                result['funcionario']['nombrepublico'],
                'Sin definir',  #TODO analizar como obtenerlo
                result['funcionario']['url'],
            ])
        setattr(self, 'parsed_results', rows)

    def save_to_csv(self):
        logging.info('Savig file')
        file_name = 'funcionarios-{:%Y-%m-%d}.csv'.format(datetime.now())
        file_path = path.join(self.pp_path, 'data', file_name)

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(getattr(self, 'parsed_results', []))


if __name__ == '__main__':
    ResultsHandler()
