import scrapy
from datetime import datetime
from shutil import copyfile

class PagesSpider(scrapy.Spider):
    name = 'wines_spider'
    
    def __init__(self, category=None, *args, **kwargs):
        super(PagesSpider, self).__init__(*args, **kwargs)
        search_url_base = 'https://www.wine.com.br/browse.ep?cID=100851&exibirEsgotados=false&pn=%d&sorter=price-desc&filters=cVINHOS prBRL__1000000'
        self.wine_url_filename = 'wine_urls'
        #Capturar o last page, e somar 1 no ultimo parametro do range:
        #div.Pagination ul li:last-child a::text
        #06-11-2019: 101
        #11-11-2019: 95
        last_page = 2#95
        last_range = last_page + 1
        self.start_urls =[search_url_base %(n) for n in range(1, last_range)]


    def parse(self, response):
        lista_wine_urls = []
        domain_url = 'https://www.wine.com.br'
        links = response.css('.ProductDisplay-name > a.js-productClick')
        for link in links:
            lista_wine_urls.append(domain_url+link.attrib['href'])
        
        with open(f'{self.wine_url_filename}.txt', 'a+') as outfile:
            outfile.write('\n'.join(lista_wine_urls))
            outfile.write('\n')

    def closed(self, reason):
        now = datetime.strftime(datetime.now(),'%Y%m%d-%H%M%S')
        copyfile(f'{self.wine_url_filename}.txt',f'{self.wine_url_filename}_{now}.txt')