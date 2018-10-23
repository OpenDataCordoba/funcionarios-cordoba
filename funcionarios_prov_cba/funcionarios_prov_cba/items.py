# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FuncionariosProvCbaItem(scrapy.Item):
    # define the fields for your item here like:
    funcionario = scrapy.Field()
    cargo_generico = scrapy.Field()
    cargo_ocupado = scrapy.Field()
    ministerio = scrapy.Field()
    web_url = scrapy.Field()
    foto_url = scrapy.Field()
    foto_img = scrapy.Field()