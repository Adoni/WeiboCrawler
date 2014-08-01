# Scrapy settings for WeiboScrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'WeiboScrawler'

SPIDER_MODULES = ['WeiboScrawler.spiders']
NEWSPIDER_MODULE = 'WeiboScrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'WeiboScrawler (+http://www.yourdomain.com)'
