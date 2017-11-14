# -*- coding: utf-8 -*-
import scrapy, pprint, json, MySQLdb, re, unicodedata, os, time

class VcmediaSpider(scrapy.Spider):
    name = 'vcmedia'
    allowed_domains = ['vcmedia.vn']
    #start_urls = ['http://vcmedia.vn/']
    db = None
    dbc = None
    config = None
    pagesize = None

    def urlstr(self, s):
        s = s.decode('utf-8')
        s = re.sub(u'Đ', 'D', s)
        s = re.sub(u'đ', 'd', s)
        ns = unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')
        return ns.replace(' ', '-').replace('&', '').replace('(', '').replace(')', '').lower()

    def start_requests(self):
        self.config = self.settings.get('VCMEDIA')
        dbconfig = self.settings.get('DB')
        tz = self.settings.get('TIMEZONE')
        os.environ['TZ'] = tz
        time.tzset()
        dbtz = self.settings.get('DBTZ')
        self.pagesize = self.config.get('DPS')
        #self.db = MySQLdb.connect(dbconfig['HOST'], dbconfig['USER'], dbconfig['PWD'], dbconfig['DB'])
        self.db = MySQLdb.connect(dbconfig['HOST'], dbconfig['USER'], dbconfig['PWD'], dbconfig['DB'], use_unicode=True, charset="utf8")
        if not self.db:
            print "cannot connect to database"
        self.dbc = self.db.cursor()
        self.dbc.execute('SET time_zone="%s"' % dbtz)
        self.db.commit()

        return [scrapy.Request(url=self.config['URL'], headers={'referer': self.config['REFERRER']}, callback=self.parse_purl)]

    def parse_purl(self, response):
        data = json.loads(response.body)
        if (data['RecordCount']):
            self.pagesize = data['RecordCount']

        return [scrapy.Request(url=self.config['URL'] % self.pagesize, headers={'referer': self.config['REFERRER']}, callback=self.parse_url)]

    def parse_url(self, response):
        data = json.loads(response.body)
        sql = "INSERT INTO %s (url, response, created) VALUES ('%s', '%s', NOW())" % (self.config['TABLEC'], self.config['URL'] % self.pagesize, response.body)
        self.dbc.execute(sql)
        self.db.commit()
        if self.dbc.lastrowid:
            crawlid = self.dbc.lastrowid
        else:
            crawlid = 'null'

        sql = ''
        if data['CompanyInfos']:
            for ci in data['CompanyInfos']:
                link_ = '%s/%s/%s-%s%s' % (self.config['LINK']['PREFIX'], ci['TradeCenter'].lower(), ci['Symbol'], self.urlstr(ci['CompanyName'].encode('utf-8')), self.config['LINK']['SUFFIX'])
                if ci['Price'] != 0 or ci['PE'] != 0 or ci['EPS'] != 0:
                    onboard = 1
                else:
                    onboard = 0
                sql += '("%s", "%s", "%s", "%s", %s, %s, NOW(), NOW()),' % (ci['Symbol'], ci['CompanyName'], ci['TradeCenter'], link_, crawlid, onboard)
        if sql:
            sql = 'INSERT INTO %s (symbol, company_name, trade_center, profile_link, crawl_id, on_board, created, updated) VALUES %s ON DUPLICATE KEY UPDATE `company_name` = VALUES(`company_name`), `trade_center` = VALUES(`trade_center`), `profile_link` = VALUES(`profile_link`), `crawl_id` = VALUES(`crawl_id`), `on_board` = VALUES(`on_board`), `updated` = NOW()' % (self.config['TABLE'], sql[:-1])
            self.dbc.execute(sql)
            self.db.commit()
            print "updated successfully!"
        else:
            print "sql in empty"