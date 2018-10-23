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

        for reparticion in response.css('#menu-item-68614 ul li'):
            rep_nombre = reparticion.css('a::text').extract_first()
            rep_url = reparticion.css('a::attr(href)').extract_first()
            # esta caida y no tiene la estructura que buscamos
            if rep_url in self.bad_urls:
                self.logger.info('Ignorando ministerio {}'.format(rep_url))
            else:
                next_page = response.urljoin(rep_url)
                yield scrapy.Request(next_page, callback=self.parse_ministerio, meta={'web_url': rep_url})

    def parse_ministerio(self, response):
        
        cargo = response.css('h4.cargo::text').extract_first()
        ministro = response.css('h3.autoridad::text').extract_first()
        
        self.logger.info(' *** INICIANDO MINISTERIO {}**** '.format(cargo))

        # div class fotoaut -> img src foto del funcionario
        foto = response.xpath('//div[@class="fotoaut"]/img/@src').extract_first()

        cargo = cargo.replace('\t', '').replace('\r', '').replace('\n', '')

        funcionario = {'funcionario': ministro,
                        'cargo_generico': cargo,
                        'cargo_ocupado': cargo,
                        'ministerio': cargo,
                        'web_url': response.meta['web_url'],
                        'foto_url': [] if foto is None else [foto]
                        }

        # yield funcionario
        yield FuncionariosProvCbaItem(**funcionario)
        

        # ver la organica del ministerio
        organica = response.xpath("//a[contains(@title, 'Enlace permanente a Estructura')]/@href").extract_first()
        if organica is None:
            err = '********\nNo hay organica en {}\n********'.format(funcionario)
            # raise ValueError(err)
            self.logger.info(err)
        else:
            self.logger.info('Organica en {}'.format(organica))

            # esta caida y no tiene la estructura que buscamos
            if organica in self.bad_urls:
                self.logger.info('Ignorando dentro de ministerio {}'.format(rep_url))
            else:
                next_page = response.urljoin(organica)
                yield scrapy.Request(next_page, callback=self.parse_estructura_ministerio, meta={'ministerio': cargo, 'web_url': response.meta['web_url']})

    def parse_estructura_ministerio(self, response):
        self.logger.info(' *** EN ESTRUCTURA MINISTERIO {} **** '.format(response.meta['ministerio']))

        autoridades = response.css('#secciones div.autoridad')
        for autoridad in autoridades:
            
            a2 = autoridad.xpath('.//div')
            
            '''
            <div class="autoridad">
                <div style="margin-left:16%;background:#fff;overflow:hidden;padding:8px 8px;">
                    <label onclick="jQuery('.desp_1710').fadeToggle();" class="clic">
                    <h4>
                        <img src="http://www.cba.gov.ar/wp-content/themes/evolucion/img/btn_ul_5.gif" width="14" height="11">
                        Presidente del Consejo de Seguridad Deportiva Provincial	
                    </h4>
                    </label>
                    <div style="display: none;" class="desplega desp_1710">
                        <div class="fotoaut"><img width="200" height="150" src="http://www.cba.gov.ar/wp-content/4p96humuzp/2012/06/rody-guerreiro.jpg" class="attachment-post-thumbnail size-post-thumbnail wp-post-image" alt=""></div>				<h3>Rody Wilson Guerreiro</h3>
                        <h5 class="bullet">
        Presidente del Consejo de Seguridad Deportiva Provincial				</h5>
                    <div class="acceder_largue">
                        <a href="http://www.cba.gov.ar/reparticion/ministerio-de-gobierno/secretaria-de-seguridad/presidente-del-consejo-de-seguridad-deportiva-provincial/">Acceder a Presidente del Consejo de Seguridad Deportiva Provincial</a>
                    </div>
                    </div> 
                </div>		 
            </div>
            '''


            # hay un label + h4 donde se ve el nombre del cargo y ...
            a3b = a2.xpath('.//label')
            cargo_generico = a3b.xpath('.//h4/text()').extract()[1]

            # un div con el nombre especifico, por ejemplo "Directora" en las mujeres 
            a3 = a2.xpath('.//div')

            func = a3.xpath('.//h3/text()').extract_first()
            cargo_ocupado = a3.xpath('.//h5/text()').extract_first()

            # div class fotoaut -> img src foto del funcionario
            foto = a3.xpath('.//div[@class="fotoaut"]/img/@src').extract_first()
            
            # aparece a veces un link (quizas sea nuevo)
            # div class acceder_largue -> a href link fijo a este funcionario solo
            web_url = a3.xpath('.//div[@class="acceder_largue"]/a/@href').extract_first()
            if web_url in self.bad_urls:
                self.logger.info('Ignorando funcionario {}'.format(rep_url))
                web_url = ''
            if func is None:
                err = 'Autoridad no identificada: {} en {}. Cargo: {} / {}'.format(a3,
                                                                                response.meta['web_url'],
                                                                                cargo_generico,
                                                                                cargo_ocupado)
                # raise ValueError(err)
                self.logger.info(err)
                func = ''  # no hay funcionario designado
            
            func = func.replace('\t', '').replace('\r', '').replace('\n', '')
            cargo_generico = cargo_generico.replace('\t', '').replace('\r', '').replace('\n', '')
            cargo_ocupado = cargo_ocupado.replace('\t', '').replace('\r', '').replace('\n', '')
            funcionario = {'funcionario': func,
                            'cargo_generico': cargo_generico,
                            'cargo_ocupado': cargo_ocupado,
                            'ministerio': response.meta['ministerio'],
                            'web_url': web_url,  # response.meta['web_url'],
                            'foto_url': [] if foto is None else [foto]
                            }
            # yield funcionario
            yield FuncionariosProvCbaItem(**funcionario)
