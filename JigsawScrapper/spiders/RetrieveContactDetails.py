from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ypwp.items import JigsawContactItem
from scrapy import log
import re
import csv

class RetrieveContactDetailSpider(BaseSpider):
   name = "RetrieveContactDetail"
   contactsDataFile = 'ContactsToURL.csv'
   start_urls = []
   
   def __init__(self):
      BaseSpider.__init__(self)
      self.verificationErrors = []
      with open(self.contactsDataFile, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        self.log('Initialing with contact urls from file : ' + self.contactsDataFile + ' ...')
        for row in csvreader:
           if row[1].startswith('https') == True:
              self.start_urls.append(row[1])
              
      self.log('Total contacts loaded : %d' % len(self.start_urls))
        
   def getElementData(self,elementList):
      data = ''
      if len(elementList) > 0:
        data = elementList[0]
      
      return data
   
   def parse(self, response):
       hxs = HtmlXPathSelector(response)
       items = []
       
       item = JigsawContactItem()
       item['linkurl'] = response.url
       item['contactID'] = re.search("&contactId=(.*?)$", response.url).group(1)
       item['firstName'] = self.getElementData(hxs.select('//span[@id="firstname"]/text()').extract())
       item['lastName'] =  self.getElementData(hxs.select('//span[@id="lastname"]/text()').extract())
       item['title'] =  self.getElementData(hxs.select('//span[@id="title"]/text()').extract())
       item['companyName'] = self.getElementData(hxs.select('//*[@id="companyname"]/a/text()').extract()) 
       item['addressLine1'] = self.getElementData(hxs.select('//span[@id="address"]/text()').extract()) 
       item['addressLine2'] = self.getElementData(hxs.select('//span[@id="address2"]/text()').extract()) 
       item['city'] = self.getElementData(hxs.select('//span[@id="city"]/text()').extract())
       item['state'] = self.getElementData(hxs.select('//span[@id="state"]/text()').extract())
       item['zip'] = self.getElementData(hxs.select('//span[@id="zip"]/text()').extract())
       item['country'] = self.getElementData(hxs.select('//span[@id="country"]/text()').extract())
       item['refferedBy'] = self.getElementData(hxs.select('//*[@id="currVersion"]/div/p/em/a/text()').extract())
       items.append(item)
           
       return items

   