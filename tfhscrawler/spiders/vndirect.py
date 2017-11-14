# -*- coding: utf-8 -*-
import scrapy, pprint, json, MySQLdb, re, unicodedata


class VndirectSpider(scrapy.Spider):
    name = 'vndirect'
    allowed_domains = ['vndirect.com.vn']
    #start_urls = ['http://vndirect.com.vn/']

    db = None
    dbc = None
    config = None

    def urlstr(self, s):
        s = s.decode('utf-8')
        s = re.sub(u'Đ', 'D', s)
        s = re.sub(u'đ', 'd', s)
        ns = unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')
        return ns.replace(' ', '-').lower()

    def start_requests(self):
        self.config = self.settings.get('VNDIRECT')
        dbconfig = self.settings.get('DB')
        tz = self.settings.get('TIMEZONE')
        dbtz = self.settings.get('DBTZ')
        #self.db = MySQLdb.connect(dbconfig['HOST'], dbconfig['USER'], dbconfig['PWD'], dbconfig['DB'])
        self.db = MySQLdb.connect(dbconfig['HOST'], dbconfig['USER'], dbconfig['PWD'], dbconfig['DB'], use_unicode=True, charset="utf8")
        if not self.db:
            print "cannot connect to database"
        self.dbc = self.db.cursor()
        self.dbc.execute('SET time_zone="%s"' % dbtz)
        self.db.commit()

        return [scrapy.Request(url=self.config['URL'])]
    def parse(self, response):
        data = json.loads(response.body)
        sql = "INSERT INTO %s (url, response, created) VALUES ('%s', '%s', NOW())" % (self.config['TABLEC'], self.config['URL'], self.db.escape_string(response.body))
        self.dbc.execute(sql)
        self.db.commit()
        if self.dbc.lastrowid:
            crawlid = self.dbc.lastrowid
        else:
            crawlid = 'null'

        sql = ''
        if len(data['data']):
            for ci in data['data']:
                sql += '("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %s, NOW(), NOW()),' % (ci['symbol'], ci['company'], ci['companyName'], ci['companyNameEng'], ci['shortName'], ci['listedDate'], ci['floor'], ci['industryName'], ci['indexCode'], crawlid)
        if sql:
            sql = u'INSERT INTO %s (symbol, company, company_name, company_name_eng, short_name, listed_date, floor, industry_name, index_code, crawl_id, created, updated) VALUES %s ON DUPLICATE KEY UPDATE `company` = VALUES(`company`), `company_name` = VALUES(`company_name`), `company_name_eng` = VALUES(`company_name_eng`), `short_name` = VALUES(`short_name`), `listed_date` = VALUES(`listed_date`), `floor` = VALUES(`floor`), `industry_name` = VALUES(`industry_name`), `index_code` = VALUES(`index_code`), `crawl_id` = VALUES(`crawl_id`), `updated` = NOW()' % (self.config['TABLE'], sql[:-1])
            self.dbc.execute(sql)
            self.db.commit()
            print "updated successfully!"
        else:
            print "sql in empty"