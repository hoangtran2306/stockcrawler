# -*- coding: utf-8 -*-

# Scrapy settings for tfhscrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tfhscrawler'

SPIDER_MODULES = ['tfhscrawler.spiders']
NEWSPIDER_MODULE = 'tfhscrawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tfhscrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tfhscrawler.middlewares.TfhscrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'tfhscrawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'tfhscrawler.pipelines.TfhscrawlerPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DB = {
    'HOST': '10.3.0.102',
    'USER': 'root',
    'PWD': '',
    'DB': 'stock24h_masterdb'
}

# timezone
TIMEZONE = 'Asia/Ho_Chi_Minh'
DBTZ = '+7:00'

CAFEFPROFILE = {
    'COMTABLE': 'vcme_companies',
    'STABLE': 'scff_sprofiles',
    'BTABLE': 'scff_bprofiles',
    # second
    'DOWNLOAD_DELAY': 1,
    # second
    'API_DOWNLOAD_DELAY': .25,
    # urls of basic type
    'BURLS': {
        'V1': {
            'FININF' : {
                'QUARTER': 'http://s.cafef.vn/Ajax/Bank/BHoSoCongTy.aspx?symbol=%s&Type=1&PageIndex=0&PageSize=4&donvi=1',
                'YEAR': 'http://s.cafef.vn/Ajax/Bank/BHoSoCongTy.aspx?symbol=%s&Type=2&PageIndex=0&PageSize=4&donvi=1',
                '6MONS': 'http://s.cafef.vn/Ajax/Bank/BHoSoCongTy.aspx?symbol=%s&Type=3&PageIndex=0&PageSize=4&donvi=1'
            },
            'BASINF': 'http://s.cafef.vn/Ajax/Bank/BThongTinChung.aspx?sym=%s',
            'AFFINF': 'http://s.cafef.vn/Ajax/Bank/BCongTyCon.aspx?sym=%s',
            'FINRPT': 'http://s.cafef.vn/Ajax/Bank/BBaoCaoTaiChinh.aspx?sym=%s'
        },
        'V2': {
            'FININF' : {
                'QUARTER': 'http://s.cafef.vn/Ajax/HoSoCongTy.aspx?symbol=%s&Type=1&PageIndex=0&PageSize=4',
                'YEAR': 'http://s.cafef.vn/Ajax/HoSoCongTy.aspx?symbol=%s&Type=2&PageIndex=0&PageSize=4',
                '6MONS': 'http://s.cafef.vn/Ajax/HoSoCongTy.aspx?symbol=%s&Type=3&PageIndex=0&PageSize=4'
            },
            'BASINF': 'http://s.cafef.vn/Ajax/CongTy/ThongTinChung.aspx?sym=%s',
            # leadership & ownership
            'LOINF': 'http://s.cafef.vn/Ajax/CongTy/BanLanhDao.aspx?sym=%s',
            'AFFINF': 'http://s.cafef.vn/Ajax/CongTy/CongTyCon.aspx?sym=%s',
            'FINRPT': 'http://s.cafef.vn/Ajax/CongTy/BaoCaoTaiChinh.aspx?sym=%s'
        }
    },
    # basic-crawler scheduled points (basic profiles)
    'BTIME': {
        'START': '2018/09/02',
        # days
        'INTERVAL': '2'
    }
}

CAFEFSTOCKMARKET = {
    'URL': 'http://cafef.vn/thi-truong-chung-khoan.rss',
    'TABLE': 'articles',
    'TABLEC': 'crawl_articles',
    'TABLECOM': 'vcme_companies',
    'FROM': 'cafef',
    'TYPE': 'xml',
    'CATEGORY': 'stock'
}

VTVECO = {
    'URL': 'http://vtv.vn/kinh-te.rss',
    # video prefix
    'VPREFIX': 'https://hls.mediacdn.vn/',
    # video key index
    'VKINDEX': 'FileName',
    # video key prefix
    'VKPREFIX': 'vtv',
    # video type
    'VTYPE': 'mp4',
    # video thumbnail type
    'VTTYPE': 'jpg',
    # video thumbnail prefix
    'VTPREFIX': 'http://video-thumbs.vcmedia.vn/thumb_w/600/',
    'TABLE': 'articles',
    'TABLEC': 'crawl_articles',
    'TABLECOM': 'vcme_companies',
    'FROM': 'vtv',
    'TYPE': 'xml',
    'CATEGORY': 'economy'
}

NCDT = {
    'ROOT': 'http://nhipcaudautu.vn',
    'URL': 'http://nhipcaudautu.vn/doanh-nghiep/tin-tuc/',
    'TABLE': 'articles',
    'TABLEC': 'crawl_articles',
    'TABLECOM': 'vcme_companies',
    'FROM': 'ncdt',
    'TYPE': 'html',
    'CATEGORY': 'business'
}

VCMEDIA = {
    'URL': 'http://solieu6.vcmedia.vn/ProxyHandler.ashx?RequestName=CompanyInfo&TradeId=-2&IndustryId=0&Keyword&PageIndex=1&PageSize=%s&Type=0',
    # page counter
    'PURL': 'http://solieu6.vcmedia.vn/ProxyHandler.ashx?RequestName=CompanyInfo&TradeId=-2&IndustryId=0&PageIndex=1&Type=0',
    # default page size
    'DPS': 10000,
    'REFERRER': 'http://s.cafef.vn/du-lieu-doanh-nghiep.chn',
    'TABLE': 'vcme_companies',
    'TABLEC': 'vcme_crawl_companies',
    'LINK': {
        'PREFIX': 'http://s.cafef.vn',
        'SUFFIX': '.chn'
    }
}

VNDIRECT = {
    'URL': 'https://finfoapi-hn.vndirect.com.vn/stocks',
    'TABLE': 'vndc_companies',
    'TABLEC': 'vndc_crawl_companies'
}

# formatted content should be used by native app
NFCONTENT = {
    'OBJECT': {
      'VIEW':   0, # là kiểu body, div, thẻ p mà không chứa text, chỉ chứa element.
      'TEXT':   1, # là kiểu chứa text và định dạng style, color.
      'IMAGE':  2, # là kiểu chứa ảnh, twentytwenty.
      'LINK':   3, # là kiểu chứa link dạng text hoặc ảnh.
      'VIDEO':  4  # là kiểu video.
    },
    'ALIGN': {
      'LEFT':  -1,
      'CENTER': 0,
      'RIGHT':  1
    },
    'FONTSTYLE': {
      'NORMAL': 0,
      'ITALIC': 1,
      'BOLD':   2,
      'UNDERLINE': 3
    },
    'DFCOLOR': '#252525',
    # image title color
    'ITCOLOR': '#9E9E9E',
    'DFIMGFS': 16
}