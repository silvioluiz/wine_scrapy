# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class WineScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class WinePagePipeline(object):
    def open_spider(self, spider):
      if(spider.name == 'wine_page_spider'):
        self.file = open('all_wines.csv', 'w')
        #Ver melhor forma de capturar colunas do cabecalho
        fieldnames = ['link_wine', 'titulo', 'comentario_sommelier', 'preco_total', 
        'preco_associado', 'desconto', 'tipo', 'uvas', 'pais', 'regiao', 'vinicola', 
        'teor_alcoolico', 'amadurecimento', 'classificacao', 'visual', 'aroma', 'gustativo', 
        'temperatura_servico', 'potencial_guarda', 'harmonizacao', 'quantidade_avaliacoes', 'nota']
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()
      
    def process_item(self, item, spider):
      if(spider.name == 'wine_page_spider'):
        self.writer.writerow(item)
      return item

    def close_spider(self, spider):
      if(spider.name == 'wine_page_spider'):
        self.file.close()
