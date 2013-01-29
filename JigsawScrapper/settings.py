# Scrapy settings for ypwp project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'ypwp'

SPIDER_MODULES = ['ypwp.spiders']
NEWSPIDER_MODULE = 'ypwp.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ypwp (+http://www.yourdomain.com)'

LOG_FILE='ypwp.log'
LOG_LEVEL='DEBUG'
CONCURRENT_REQUESTS=1
#DOWNLOAD_DELAY = 0.9

#DEPTH_PRIORITY = 1
#SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
