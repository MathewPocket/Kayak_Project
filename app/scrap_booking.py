# Import os => Library used to easily manipulate operating systems
## More info => https://docs.python.org/3/library/os.html
import os 

# Import logging => Library used for logs manipulation 
## More info => https://docs.python.org/3/library/logging.html
import logging

# Import scrapy and scrapy.crawler 
import scrapy
from scrapy.crawler import CrawlerProcess

from math import *

class BookingSpider(scrapy.Spider):

    # Name of your spider
    name = "bookingspider"
    #Nombre de résulat par page proposé par Booking
    nb_result_page = 25
    #Limiteur manuel du nombre de page par ville
    counter = 5

    def start_requests(self):
        
        for i in self.list_ville:
            #PARAM
            #ss = recherche
            #checkin = date de début
            #checkout = date de fin 
            #group_adults=2 // recherche pour deux personnes
            #order = review_score_and_price mixe entre prix et note
            logging.info('>>>>URL POUR LA VILLE DE '+i)
            url = f'https://www.booking.com/searchresults.fr.html?ss={i.replace(" ","%20")}&checkin={self.date_in}&checkout={self.date_out}&group_adults=2&ac_langcode=fr&order=review_score_and_price'
            logging.info(url)
            yield scrapy.Request(url, cb_kwargs={'ville': i,'url':url,'refresh_mode':self.refresh_mode}, callback=self.getPage)
    
    #permet de mettre du delais entre les requests
    custom_settings = {
        'DOWNLOAD_DELAY': 2, # 10 seconds of delay
        'RANDOMIZE_DOWNLOAD_DELAY': True, # By default, when you set DOWNLOAD_DELAY = 2 for example, Scrapy will introduce random delays of between: 
                                          # Lower Limit: 0.5 * DOWNLOAD_DELAY
                                          # Upper Limit: 1.5 * DOWNLOAD_DELAY
        'HTTPCACHE_ENABLED': False
    }

    #Appel de toutes les pages pour une ville
    def getPage(self, response,ville,url,refresh_mode):
        try:
            #Calule du nombre de page
            nb_page = response.xpath('//*[@id="right"]/div[1]/div/div/h1/text()').get()
            nb_page = nb_page.split(":")[1]
            nb_page = float(nb_page.strip().split(" ")[0])
            nb_page = ceil(nb_page/25)
            #Si le parametre counter est différent de zero on ne scrappera que X page
            if self.counter != 0 and nb_page > self.counter:
                nb_page=self.counter
            #Si le nombre de page dépasse 40 on tronque
            if nb_page > 40:
                #Booking limite à 40 pages de résultat
                nb_page = 40
            logging.info('Ville : ' +ville+ ' Le nombre de page à scrapper : ' + str(nb_page))
        except:
            nb_page = 1
            logging.info('Ville : ' +ville+ ' Le nombre de page à scrapper a été forcé à 1')

        #Boucle sur les pages
        for page in range(0,nb_page):
            url_page = url+"&offset="+str(self.nb_result_page*page)
            yield scrapy.Request(url_page, cb_kwargs={'ville': ville,'url':url,'refresh_mode':refresh_mode}, callback=self.parse_result)


    # Parse function 
    def parse_result(self,response,ville,url,refresh_mode):
        #récupération des hotels
        quotes = response.xpath('//*[@id="search_results_table"]//div[@data-testid="property-card"]')
        logging.info('Nombre de property-card pour la ville '+ville+' : '+str(len(quotes)))

        for quote in quotes: 
            #Récupération et nettoyage de l'URL de l'hotel, en effet booking rajoute bcp de paramètre inutile pour nous
            url_clean = quote.xpath('div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a').attrib["href"]
            url_clean = url_clean.split("?")[0]
            
            #Récupération du prix pour les hotels et la période (deux emplacements, ca dépend des hotels...)
            prx = quote.xpath('div[1]/div[2]/div/div[last()]/div[2]/div/div[1]//span[@data-testid="price-and-discounted-price"]/text()').get()
            if prx == None: 
                prx = quote.xpath('div[1]/div[2]/div/div[last()]/div[2]/div/div[1]//div[@data-testid="price-and-discounted-price"]/span/text()').get()

            #Création d'un dictionnaire d'infos sur l'hotel, mais il nous manque la position 
            info_hotel =  {
                    'ville' : ville,
                    'nom': quote.xpath('div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a/div[1]/text()').get(),
                    'url': url_clean,
                    'prix': prx,
                    'note': quote.xpath('div[1]/div[2]/div/div[1]/div/div[2]/div/div/div/a/span/div/div[1]/text()').get(),
                    'distance_center': quote.xpath('div[1]/div[2]/div/div[1]/div/div[1]/div/div[2]/div/span[1]/span/span/text()').get()
                }
            
            #Appel de l'URL pour afficher la page de l'hotel si on est en mode full sinon on écrit dans le fichier
            if refresh_mode == 'full':
                yield scrapy.Request(url_clean, cb_kwargs=info_hotel, callback=self.parse_hotel)
            else:
                #on écrit dans le fichier résultat
                yield info_hotel

    #fonction de récupération de la position sur la page de l'hotel
    def parse_hotel(self, response, ville,nom,url,prix,note,distance_center): # Notice it will receive a new arg here, as passed in cb_kwargs
        try:
            
            #Récupération de la position
            latlon = response.xpath('//*[@id="hotel_sidebar_static_map"]').attrib["data-atlas-latlng"]
            #Parsing des infos
            lat = float(latlon.split(',')[0])
            lon = float(latlon.split(',')[1])

            #Récupération de la description
            description =  response.xpath('//*[@id="property_description_content"]/p/text()').getall()
            desc_final = ''
            for i in description:
                desc_final += i.replace('</p>','</br>').replace('<p>','')

            #écriture dans le fichier
            yield {
                'ville': ville,
                'nom': nom,
                'url': url,
                'prix': prix,
                'note': note,
                'distance_center': distance_center,         
                'latitude': lat,
                'longitude': lon,
                'description': desc_final
            }
        except:
            logging.info('Un problème a eu lieu pour l\'hotel : '+nom)