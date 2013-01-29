# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class JigsawSearchContactResultItem(Item):
    personName = Field()
    linkurl = Field()
    
class JigsawContactItem(Item):
    contactID = Field()
    linkurl = Field()
    firstName = Field()
    lastName = Field()
    title = Field()
    companyName = Field()
    addressLine1 = Field()
    addressLine2 = Field()
    city = Field()
    state = Field()
    zip = Field()
    country = Field()
    refferedBy = Field()
    
    
        