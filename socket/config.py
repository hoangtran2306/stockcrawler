# database configuration
DB = {
    'HOST': '127.0.0.1',
    'USER': 'admin',
    'PWD': 'Anhhoang236',
    'DB': 'finance'
}
# memcached
MEMCACHE = {
    'HOST': '127.0.0.1',
    'PORT': 11211,
    'DEBUG': 0
}
# support API by saving realtime data to cache (memcached)
APIDATA = False
# timezone
TIMEZONE = 'Asia/Ho_Chi_Minh'
# database timezone
DBTZ = '+7:00'
# active time intervals (24h)
ACTIVE = {
    'START': '08:50',
    'END': '15:10'
}
# clear frequence data
FREDATA = {
    'ACTIVE': '1 days',
    'TABLE': [
        'vndc_crawl_hnx', 'vndc_crawl_hnx30', 'vndc_crawl_hose', 'vndc_crawl_upcom', 'vndc_crawl_vn30', 'vndc_crawl_markets',
        'vndc_hnx', 'vndc_hnx30', 'vndc_hose', 'vndc_upcom', 'vndc_vn30', 'vndc_markets'
    ],
    'DTABLE': {
        'NAME': 'vndc_hose',
        'FIELD': 'trading_date'
    }
}

# common tables
CMNTABLES = {
    'VNDCCMD': 'vndc_commands',
    'VNDCURL': 'vndc_urls'
}

# daily statistic table
DSTMARKET = 'vndc_market_daily'
DSTSTOCK = 'vndc_stock_daily'
# monthly statistic table
MSTMARKET = 'vndc_market_monthly'
MSTSTOCK = 'vndc_stock_monthly'
# annual statistic table
ASTMARKET = 'vndc_market_annual'
ASTSTOCK = 'vndc_stock_annual'

# keep script run forever
KEEPALIVE = True

# there are no transitions on these days
# day of week: monday is 0, sunday is 6
DAYOFF = [5, 6]

STATS = {
    # daily interval (minute)
    'DINTERVAL': 5, # 5 minutes
    # monthly interval (day)
    'MINTERVAL': 1, # days
    # annual interval (day)
    'AINTERVAL': 10, # days
}

# active sockets
SOCKETS = {
    'CFC': {
        'CMD': ['cfc'],
        'TABLE': 'vndc_cfc',
        'TABLEC': 'vndc_crawl_cfc',
        'ACTIVE': 'forever'
    },
    'MARKET': {
        'CMD': ['info', 'cfc', 'market'],
        'TABLE': 'vndc_markets',
        'TABLEC': 'vndc_crawl_markets',
        'MEMKEY': 'vndc_markets',
        'ACTIVE': '1 days',
        # temporary data sheets
        'TABLET': ['vndc_crawl_markets', 'vndc_markets'],
        # table/field as patterns to verity
        'FIELDT': ['vndc_markets', 'trading_date']
    },
    'HOSE': {
        'CMD': ['info', 'hose'],
        'TABLE': 'vndc_hose',
        'TABLEC': 'vndc_crawl_hose',
        'MEMKEY': 'vndc_hose',
        'FLOOR': '10',
        'ACTIVE': '1 days',
        # temporary data sheets
        'TABLET': ['vndc_crawl_hose', 'vndc_hose'],
        # table/field as patterns to verity, field must be milisecond unix timestamp
        'FIELDT': ['vndc_hose', 'trading_date']
    },
    'VN30': {
        'CMD': ['info', 'vn30'],
        'TABLE': 'vndc_vn30',
        'TABLEC': 'vndc_crawl_vn30',
        'MEMKEY': 'vndc_vn30',
        'FLOOR': '11',
        'ACTIVE': '1 days',
        # temporary data sheets
        'TABLET': ['vndc_crawl_vn30', 'vndc_vn30'],
        # table/field as patterns to verity, field must be milisecond unix timestamp
        'FIELDT': ['vndc_vn30', 'trading_date']
    },
    'HNX': {
        'CMD': ['info', 'hnx'],
        'TABLE': 'vndc_hnx',
        'TABLEC': 'vndc_crawl_hnx',
        'MEMKEY': 'vndc_hnx',
        'FLOOR': '02',
        'ACTIVE': '1 days',
        # temporary data sheets
        'TABLET': ['vndc_crawl_hnx', 'vndc_hnx'],
        # table/field as patterns to verity, field must be milisecond unix timestamp
        'FIELDT': ['vndc_hnx', 'trading_date']
    },
    'HNX30': {
        'CMD': ['info', 'hnx30'],
        'TABLE': 'vndc_hnx30',
        'TABLEC': 'vndc_crawl_hnx30',
        'MEMKEY': 'vndc_hnx30',
        'FLOOR': '12',
        'ACTIVE': '1 days',
        # temporary data sheets
        'TABLET': ['vndc_crawl_hnx30', 'vndc_hnx30'],
        # table/field as patterns to verity, field must be milisecond unix timestamp
        'FIELDT': ['vndc_hnx30', 'trading_date']
    },
    'UPCOM': {
        'NAME': 'UPCOM',
        'CMD': ['info', 'upcom'],
        'TABLE': 'vndc_upcom',
        'TABLEC': 'vndc_crawl_upcom',
        'MEMKEY': 'vndc_upcom',
        'FLOOR': '03',
        'ACTIVE': '1 days',
        # temporary data sheets
        'TABLET': ['vndc_crawl_upcom', 'vndc_upcom'],
        # table/field as patterns to verity, field must be milisecond unix timestamp
        'FIELDT': ['vndc_upcom', 'trading_date']
    }
}
# logging
LOG = {
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s]: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': 'logs/vnds-%s.log',
            'when': 'D',
            'backupCount': 30,
            'encoding': 'utf8'
        },

    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    },
    'levels': {
        'SQ': 55,
        'SA': 60
    }
}
