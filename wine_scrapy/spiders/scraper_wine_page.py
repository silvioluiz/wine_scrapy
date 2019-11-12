import re
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class WineSpider(scrapy.Spider):
    name = 'wine_page_spider'
    custom_settings = {
        'download_delay': 2
    }

    def start_requests(self):
         cookies = {}
         #cookies['__cfduid'] = 'd01155621c4fe7807b6b042bdb24055de1572997108'
         '''
         cookies['_fbp'] = 'fb.2.1572997101155.1226198458'
         cookies['_ga'] = 'GA1.3.1695951520.1572997100'
         cookies['_gaexp'] = 'GAX1.3.I6oZ9RivS8-S-4lc3qnASQ.18301.1'
         cookies['_gcl_au'] = '1.1.137662246.1572997101'
         cookies['_gid'] = 'GA1.3.628304828.1573400069'
         cookies['_hjid'] = '76e0250f-ebf6-4dd2-8fa2-c49b59682ca3'
         cookies['_pm_id'] = '740141572997100895'
         cookies['_pm_sid'] = '855401573409573927'
         cookies['advcake_trackid'] = '5bdd98c8-8b13-503a-5675-b01c74dc3199'
         cookies['cto_lwid'] = '3e0f1c60-ae0d-457a-94fe-fd5dfd0f6ce4'
         cookies['incap_ses_684_2052873'] = 'wiurbjpxNBzyIqlCnw9+CZpRyF0AAAAAU3+dp9p3483GeacI7X5veg=='
         cookies['nlbi_2052873'] = 'aFaGYTU8iG214rmc4GeghwAAAADCwyxC4im8cS/X3ooBnnKL'
         cookies['rr_rcs'] = 'eF4Nx7ERgDAIBdAmlbtw9yGQwAbOkQTvLOzU-fV1r2zXe58LrO7E1qsiAtb-NSXi8sxdwmePaJQjFymYKaFCh9iwRBWEf3QkEUU'
         cookies['user_unic_ac_id'] = '154ced23-e605-541b-44b9-9d753f1014e0'
         cookies['visid_incap_2052873'] = 'zf6ocI4gRryEs9LIu4OBOOsHwl0AAAAAQUIPAAAAAADbSTQ14kO954mrGp85NLxa'
         cookies['voxusmediamanager__ip'] = '177.45.238.203'
         cookies['voxusmediamanager_acs'] = 'true'
         cookies['voxusmediamanager_id'] = '15729971072000.6204713203751624c2mnv2059ap'
         cookies['GTMCampaignLP'] = 'https%3A%2F%2Fwww.wine.com.br%2F'
         cookies['GTMCampaignReferrer'] = ''
         cookies['GTMUtmMedium'] = '(none)'
         cookies['GTMUtmSource'] = '(direct)'
         cookies['GTMUtmTimestamp'] = '1572997100594'
         '''
         
         for page in self.start_urls:
             yield SeleniumRequest(
                 url=page,
                 cookies = cookies,
                 callback=self.parse,
                 wait_time=6#,
                 #wait_until=EC.visibility_of_element_located((By.CSS_SELECTOR,'.Comments-header-quantity'))
             )

    def __init__(self, category=None, *args, **kwargs):
        super(WineSpider, self).__init__(*args, **kwargs)
        self.pattern_star = '^(([\d]\.[\d])|[\d])'
        self.pattern_desconto = '^([\d]{1,})'
        #options = webdriver.ChromeOptions()
        #options.add_argument("--start-maximized")
        #options.add_argument('--disable-extensions')
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        #options.add_argument('--no-sandbox')
        #driver = webdriver.Chrome(chrome_options=options)
        #driver.implicitly_wait(2)
        #self.driver = webdriver.Chrome(options=options)
        #self.driver.implicitly_wait(30)
        wine_urls = 'wine_urls.txt'
        with open(wine_urls, 'r') as outfile:
            lines = outfile.readlines()
            for line in lines:
                self.start_urls.append(line)    
        
    def parse(self, response):
        vinho = {}

        #PRINCIPAL
        vinho['link_wine'] = response.url
        vinho['titulo'] = response.css('h1.PageHeader-title::text').get()
        vinho['comentario_sommelier'] = response.css('blockquote.ReadMore-text::text').get()

        if(vinho['comentario_sommelier']):
            vinho['comentario_sommelier'] = vinho['comentario_sommelier'].strip()

        #Quando o Produto está esgotado, precos estao ficam com valor -1
        precos = response.css('div.ProductPage-priceBox > div.PriceBox-content span.Price.Price--salePrice > span.Price-raw::text').getall()
        vinho['preco_total'] = -1
        vinho['preco_associado'] = -1
        
        if (precos):
            vinho['preco_total'] = precos[0]
            vinho['preco_associado'] = precos[1]
        #exclusivo = response.css('div.ClubPrice-value-productPage::text')
        vinho['desconto'] = response.css('div.PriceBox-full-price-area > div> span.DiscountTag >span::text').get()
        if(vinho['desconto']):
            vinho['desconto'] = re.search(self.pattern_desconto, vinho['desconto']).group()
        
        #Detalhes Tecnicos
        detalhes = response.css('.TechnicalDetails-list')
        vinho['tipo'] = detalhes.css('li.TechnicalDetails-description--grape > div.Right > dt::text').get()
        vinho['uvas'] = detalhes.css('li.TechnicalDetails-description--grape > div.Right > dd::text').get()
        vinho['pais'] = detalhes.css('li.TechnicalDetails-description--location > div.Right > dt::text').get()
        vinho['regiao'] = detalhes.css('li.TechnicalDetails-description--location > div.Right > dd::text').get()
        vinho['vinicola'] = detalhes.css('li.TechnicalDetails-description--winery > div.Right > dd::text').get()
        vinho['teor_alcoolico'] = detalhes.css('li.TechnicalDetails-description--alcoholic_strength > div.Right > dd::text').get()
        vinho['amadurecimento'] = detalhes.css('li.TechnicalDetails-description--ageing > div.Right > dd::text').get()
        vinho['classificacao'] = detalhes.css('li.TechnicalDetails-description--classification >div.Right > dd::text').get()
        vinho['visual'] = detalhes.css('li.TechnicalDetails-description--appearance > div.Right > dd::text').get()
        vinho['aroma'] = detalhes.css('li.TechnicalDetails-description--aroma > div.Right > dd::text').get()
        vinho['gustativo'] = detalhes.css('li.TechnicalDetails-description--taste >div.Right > dd::text').get()
        vinho['temperatura_servico'] = detalhes.css('li.TechnicalDetails-description--temperature > div.Right>dd::text').get()
        vinho['potencial_guarda'] = detalhes.css('li.TechnicalDetails-description--ageing_potential>div.Right>dd::text').get()
        
        vinho['harmonizacao'] = response.css('article.TechnicalDetails-matching--right > dd::text').get()
        
        #AVALIACOES
        vinho['quantidade_avaliacoes'] = response.css('span.Comments-header-quantity::text').get()
        if (vinho['quantidade_avaliacoes']):
            vinho['quantidade_avaliacoes'] = vinho['quantidade_avaliacoes'].replace('(','').replace(')','')
        vinho['nota'] = response.css('span.Comments-header-star-text::text').get()
        if(vinho['nota']):
            vinho['nota'] = re.search(self.pattern_star, vinho['nota']).group()
        
        yield vinho
        