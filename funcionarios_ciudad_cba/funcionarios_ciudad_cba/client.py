import requests


class FuncionariosCiudad(object):

    @staticmethod
    def _get(url, image=False):
        response = requests.get(url)
        if response.ok and not image:
            return response.json()
        elif response.ok and image:
            return response.content

    def get_image(self, url):
        return self._get(url, image=True)

    def get_employees(self):
        url = 'https://gobiernoabierto.cordoba.gob.ar/api/funciones/'
        response =  self._get(url)
        results = response['results']

        while True:
            response = self._get(response['next'])
            results += response['results']

            if not response['next']:
                break
        return results
