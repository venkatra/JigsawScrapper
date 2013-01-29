from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ypwp.items import JigsawSearchContactResultItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.http import FormRequest, Request
from scrapy import log
from selenium import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.http.cookies import CookieJar
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pprint
import re

class SearchAndRetrieveContactURLSpider(CrawlSpider):
   name = "SRContactURL"
   WEBDRIVER_PAGE_LOAD_TIME=10
   JIGSAW_USER_ID="????"
   JIGSAW_PWD="???"
   # Store response in a file for debugging purposes
   responseFile = 'response.html'
   lastNameIdx = 0   
   #List of last names to search on
   lastNames=["riyaz","khan","sekar","watson","clarkson"]  
   
   start_urls = []
   next_lnk_clicked = 'N'
   
   def __init__(self):
      CrawlSpider.__init__(self)
      self.verificationErrors = []
      
   def __del__(self):
      print self.verificationErrors
      CrawlSpider.__del__(self)

   def loadURLOnWebDriver(self,pageURL):
       self.driver.get(pageURL)
       try:
         WebDriverWait(self.driver, 10).until(lambda driver : driver.title)
       finally:
         print " i waited "
       time.sleep(self.WEBDRIVER_PAGE_LOAD_TIME)
   
   def start_requests(self):
         self.driver = webdriver.Firefox()
         self.driver.implicitly_wait(self.WEBDRIVER_PAGE_LOAD_TIME)
         self.loadURLOnWebDriver('https://www.jigsaw.com/Login.xhtml')
         input_email = self.driver.find_element_by_name("email")
         input_password = self.driver.find_element_by_name("password")
         input_rememberUser = self.driver.find_element_by_name("rememberUser")
         frm_LoginForm = self.driver.find_element_by_name("LoginForm")
         input_email.send_keys(self.JIGSAW_USER_ID)
         input_password.send_keys(self.JIGSAW_PWD)
         input_rememberUser.click()
         frm_LoginForm.submit()

         formdataMap={}
         formdataMap['opCode'] = 'login'
         formdataMap['targetURL'] = ''
         formdataMap['isPremium'] = 'false'
         formdataMap['isFromODI'] = 'false'
         formdataMap['migrateToCME'] = 'false'
         formdataMap['rememberUser'] = 'on'
         formdataMap['email'] = self.JIGSAW_USER_ID
         formdataMap['password'] = self.JIGSAW_PWD
         return [FormRequest('https://www.jigsaw.com/Login.xhtml',
                    formdata=formdataMap,
                    callback=self.after_login)]

   def after_login(self, response):
        open(self.responseFile, 'wb').write(response.body) 
        self.log("METHOD : after login")
        if "Log In" in response.body:
            self.log("Login failed", level=log.ERROR)
            return
        self.log("Login sucess")
        return Request('https://jigsaw.data.com/sso/redirect')

   def parse(self, response):
       self.log("[PARSE] response url " + response.url)
       open(self.responseFile, 'wb').write(response.body) 
       
       if "Logout" in response.body:
        return [Request(url=self.getLastNameSearchURL(),
                callback=self.parse_searchResult)]
                
       return super(JigSawSpider, self).parse(response)
       
   def getLastNameSearchURL(self):
        if self.lastNameIdx > len(self.lastNames):
            self.log('All searches completed.')
            return  ''
            
        lName = self.lastNames[self.lastNameIdx]
        self.log("Fetching for last names : " + lName)
        return 'https://www.jigsaw.com/SearchAcrossCompanies.xhtml?tok=1357953675345-3800739979356950870&opCode=search&rowsPerPage=200&cnCountry=9000&cnName=' + lName
        
   def parse_searchResult(self, response):
       open(self.responseFile, 'wb').write(response.body)    
       hxs = HtmlXPathSelector(response)
       
       self.log ("was next page traversed : " + self.next_lnk_clicked) 
       if self.next_lnk_clicked == 'N':
          self.loadURLOnWebDriver(response.url)
       
       self.next_lnk_clicked == 'N'
          
       elem_contactNames = self.driver.find_elements(By.XPATH,'//a[contains(@href,"showContact")]')
       items=[]
       for elem_contactName in elem_contactNames:
           contactId = re.search("javascript:showContact\('(.*?)'", elem_contactName.get_attribute("href")).group(1)
           item = JigsawSearchContactResultItem()
           item['personName'] = elem_contactName.text
           item['linkurl'] =  'https://www.jigsaw.com/BC.xhtml?&tabname=gc&contactId=' + contactId
           yield item
           
       nextPageLink = self.driver.find_elements(By.XPATH, '//div[@id="pageCountTop"]//a[contains(@href,"openPageURL")]')
       nextPageURL = ''
       for lnk in nextPageLink:
          if lnk.text == 'Next>':
            next_page_num = lnk.get_attribute("href") 
            self.log("Going to next page : " + next_page_num)
            lnk.click()
            time.sleep(self.WEBDRIVER_PAGE_LOAD_TIME)
            self.next_lnk_clicked = 'Y'
            nextPageURL = self.driver.current_url
       
       if nextPageURL == '':
         self.next_lnk_clicked = 'N'
         self.lastNameIdx = self.lastNameIdx + 1
         nextPageURL = self.getLastNameSearchURL()
         
       if nextPageURL == '':
          self.log('All searches completed.')
          yield items 
            
       self.log ("Going to page : " + nextPageURL)
       yield Request(url=nextPageURL,
                callback=self.parse_searchResult)
