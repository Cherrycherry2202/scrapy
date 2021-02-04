import scrapy,time
import json



class HemetSpider(scrapy.Spider):
	name ="hemet"
	start_urls =['https://www.hemnet.se/bostader?item_types%5B%5D=radhus&item_types%5B%5D=other']
	result= {}

	
	def parse(self,response):
		for ad in response.css("ul.normal-results > li.normal-results__hit > a::attr('href')"):
			yield scrapy.Request(url = ad.get(), callback= self.parseInnerPage)
		
		nextPage = response.css("a.next_page :: attr ('href')").get()
		if nextPage is not None:
			yield response.follow(nextPage,callback= self.parseInnerPage)


	def parseInnerPage(self,response):
		address = response.css("div.property-info__primary-container > div.property-info__address-container > div.property-address > h1.property-address__street::text").get()
		price = response.css("div.property-info__primary-container > div.property-info__price-container > p.qa-property-price::text").get()

		

		attrData = {}
		for attr in response.css("div.property-info__attributes-and-description > div.property-attributes > div.property-attributes-table > dl.property-attributes-table__area > div.property-attributes-table__row"):
			attrLabel = attr.css("dt.property-attributes-table__label::text").get()

			if attrLabel is not None:
				attrLabel = attrLabel.replace(u"\n", "")
			attrValue = attr.css("dd.property-attributes-table__value::text").get()
            
			if attrLabel != None :
				attrValue = attrValue.replace(u'\xa0', '')
				attrValue = attrValue.replace(u'\n', '')
				attrValue = attrValue.replace(u'\t', '')
				attrValue = attrValue.replace('kr/må', '')
				attrValue = attrValue.replace('kr/år', '')
				attrValue = attrValue.replace('kr/m²', '')
				attrValue = attrValue.replace('m²', '')
				attrValue = attrValue.strip()
			if attrLabel is not None:
				attrData[attrLabel] = attrValue
        
		print(attrData)

	
