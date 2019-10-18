import scrapy
from funcionarios_prov_cba.items import FuncionariosProvCbaItem


class FuncionariosCordobaProvinciaSpider(scrapy.Spider):
    name = "funcionarios"

    bad_urls = ['http://www.upc.edu.ar']

    def start_requests(self):
        urls = [
            'http://www.cba.gov.ar/reparticiones/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info(' *** BUSCANDO MINISTERIOS **** ')

        for reparticion in response.xpath('//a//@href[contains(.,"/reparticion/")]'):
            rep_url = reparticion.get()
            # esta caida y no tiene la estructura que buscamos
            if rep_url in self.bad_urls:
                self.logger.info('Ignorando ministerio {}'.format(rep_url))
            else:
                next_page = response.urljoin(rep_url) + '?view=estructura'
                yield scrapy.Request(next_page, callback=self.parse_ministerio, meta={'web_url': rep_url})

    def parse_ministerio(self, response):
        ministerio = response.xpath('//section[contains(@class,"content")]/h2/a/text()').get()
        self.logger.info(' *** INICIANDO MINISTERIO {}**** '.format(ministerio))

        secciones = response.xpath('.//section[contains(@class,"esencial")]')
        for seccion in secciones:
            cargo_generico = seccion.xpath('.//section[contains(@class,"info")]/h1/text()').get()
            cargo_ocupado = seccion.xpath('.//section[contains(@class,"autoridad-maxima")]/h2/text()').get()
            persona = seccion.xpath('.//section[contains(@class,"autoridad-maxima")]/h1/text()').get()
            foto = seccion.xpath('.//section[contains(@class,"autoridad-maxima")]/img/@src').get()
        
            if cargo_generico is not None:
                cargo_generico = cargo_generico.strip()
            if persona is not None:
                persona = persona.replace('\t', '').replace('\r', '').replace('\n', '')

            funcionario = {'funcionario': persona,
                            'cargo_generico': cargo_generico,
                            'cargo_ocupado': cargo_ocupado,
                            'ministerio': ministerio,
                            'web_url': response.meta['web_url'],
                            # c763ov8 es el nombre de la foto generica con el escudo
                            'foto_url': [] if foto is None or 'c763ov8' in foto else [foto]
                            }

            yield FuncionariosProvCbaItem(**funcionario)
