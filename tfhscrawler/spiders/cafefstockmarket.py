# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from scrapy.http import Request
from HTMLParser import HTMLParser
from dateutil import parser

import MySQLdb, sys, os, time, re, json
import logging

reload(sys)
sys.setdefaultencoding('utf8')

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class CafefstockmarketSpider(XMLFeedSpider):
    name = 'cafefstockmarket'
    allowed_domains = ['cafef.vn']
    iterator = 'iternodes'
    itertag = 'item'
    crawlid = ''

    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def _strtostamp(self, _str):
        if not _str:
            return ''
        try:
            _time = parser.parse(_str, None, dayfirst = True)
            return int(time.mktime(_time.timetuple()))
        except Exception, e:
            logging.warning('%s is not a valid time string?' % _str)
            logging.warning('exception: %s' % str(e))
            return ''

    def start_requests(self):
        self.config = self.settings.get('CAFEFSTOCKMARKET')
        self.config['NFC'] = self.settings.get('NFCONTENT')
        dbconfig = self.settings.get('DB')
        tz = self.settings.get('TIMEZONE')
        os.environ['TZ'] = tz
        time.tzset()
        dbtz = self.settings.get('DBTZ')

        #self.db = MySQLdb.connect(dbconfig['HOST'], dbconfig['USER'], dbconfig['PWD'], dbconfig['DB'])
        self.db = MySQLdb.connect(dbconfig['HOST'], dbconfig['USER'], dbconfig['PWD'], dbconfig['DB'], use_unicode=True, charset="utf8")
        if not self.db:
            print "cannot connect to database"
        self.dbc = self.db.cursor()
        self.dbc.execute('SET time_zone="%s"' % dbtz)
        self.db.commit()
        self.dbc.execute('SELECT url FROM %s' % self.config['TABLE'])
        dbdata = self.dbc.fetchall()
        self.urls = []
        if dbdata:
            for row in dbdata:
                self.urls.append(row[0])

        self.dbc.execute('SELECT symbol FROM %s GROUP BY symbol' % self.config['TABLECOM'])
        dbdata = self.dbc.fetchall()
        self.symbols = []
        if dbdata:
            for row in dbdata:
                self.symbols.append(row[0])

        self.dbc.execute('SELECT trade_center FROM %s GROUP BY trade_center' % self.config['TABLECOM'])
        dbdata = self.dbc.fetchall()
        self.tradecenters = []
        if dbdata:
            for row in dbdata:
                self.tradecenters.append(row[0])

        yield Request(self.config['URL'])

    def adapt_response(self, response):
        total = int(float(response.xpath('count(//item)').extract_first()))
        links = response.xpath('//item/link/text()').extract()
        new = 0
        for li, l in enumerate(links):
            if l:
                links[li] = l.strip()
            if not links[li] in self.urls:
                new += 1

        self.dbc.execute('INSERT INTO %s (`from`, `url`, `type`, `raw`, `total`, `new`, `created`) VALUES ("%s", "%s", "%s", "%s", "%d", "%s", NOW())' % (self.config['TABLEC'], self.config['FROM'], response.url, self.config['TYPE'], self.db.escape_string(response.body), total, new))
        self.db.commit()
        if self.dbc.lastrowid:
            self.crawlid = self.dbc.lastrowid
        return response

    def parse_node(self, response, selector):
        i = {}
        i['url'] = selector.xpath('link/text()').extract_first()
        i['title'] = selector.xpath('title/text()').extract_first()
        i['description'] = selector.xpath('description/text()').extract_first()
        i['pubDate'] = selector.xpath('pubDate/text()').extract_first()

        for k, j in i.iteritems():
            if j:
                i[k] = j.strip()

        if not i['url'] in self.urls:
            return Request(url=i['url'], callback=self.parse_, meta={'item': i})
        else:
            return i

    def parse_(self, response):
        i = response.meta['item']
        news = {}
        news['url'] = i['url']
        news['title'] = i['title']
        news['category'] = self.config['CATEGORY']
        news['published'] = i['pubDate']
        news['published_at'] = self._strtostamp(i['pubDate'])
        news['crawl_id'] = self.crawlid
        news['author'] = response.xpath('//p[contains(@class, "author")]/text()').extract_first()
        if not news['author']:
            news['author'] = response.xpath('//div[contains(@class, "credit-text")]/text()').extract_first()
        news['short_content'] = response.xpath('//h2[contains(@class, "sapo")]/text()').extract_first()
        if not news['short_content']:
            sc = re.search('<span>(.*?)<\/span>', i['description'])
            if sc:
                news['short_content'] = sc.group(1)

        news['html'] = response.xpath('//span[@id="mainContent"]').extract_first()
        if not news['html']:
            news['html'] = response.xpath('//div[contains(@class, "sp-detail-content")]').extract_first()
        if news['html']:
            content = {
                'body' : {
                    'type': self.config['NFC']['OBJECT']['VIEW'],
                    'align': self.config['NFC']['ALIGN']['CENTER'],
                    'children': [],
                    'color': self.config['NFC']['DFCOLOR']
                }
            }
            cstr = re.findall('(<p>.*?<\/p>|<img.*?>)', news['html'])
            for c in cstr:
                if "<img" in c:
                    tit_ = re.search('alt\s*=\s*["|\'](.*?)["|\']', c)
                    src_ = re.search('src\s*=\s*["|\'](.*?)["|\']', c)
                    if tit_:
                        tit_ = tit_.group(1)
                    if src_:
                        src_ = src_.group(1)
                    content['body']['children'].append({
                        'type': self.config['NFC']['OBJECT']['IMAGE'],
                        'align': self.config['NFC']['ALIGN']['CENTER'],
                        'image': src_
                    })
                    if tit_:
                        content['body']['children'].append({
                            'type': self.config['NFC']['OBJECT']['TEXT'],
                            'align': self.config['NFC']['ALIGN']['CENTER'],
                            'text': [{
                                'text': tit_,
                                'fontStyle': self.config['NFC']['FONTSTYLE']['ITALIC'],
                                #'fontSize': self.config['NFC']['DFIMGFS']
                            }],
                            'color': self.config['NFC']['ITCOLOR'],
                            'fontStyle': self.config['NFC']['FONTSTYLE']['ITALIC']
                        })
                else:
                    txt_ = self.strip_tags(c)
                    if txt_:
                        content['body']['children'].append({
                            'type': self.config['NFC']['OBJECT']['TEXT'],
                            'align': self.config['NFC']['ALIGN']['LEFT'],
                            'text': [{
                                'text': txt_,
                                'fontStyle': self.config['NFC']['FONTSTYLE']['NORMAL']
                            }]
                        })
            if content:
                news['content'] = json.dumps(content, ensure_ascii=False)

        figure = response.xpath('//div[contains(@class, "media")]/img/@src').extract_first()
        if figure:
            news['figure'] = figure
            news['figure_type'] = 'img'
        else:
            news['figure'] = response.xpath('//div[contains(@class, "sp-cover")]/img/@src').extract_first()
            if news['figure']:
                news['figure_type'] = 'img'
            else:
                news['figure'] = ""
        news['source'] = response.xpath('//p[contains(@class, "source")]/text()').extract_first()
        if not news['source']:
            news['source'] = response.xpath('//a[contains(@class, "ttvn-link")]/text()').extract_first()
        news['video_url'] = ""

        tags = response.xpath('//div[@id="ContentPlaceHolder1_pnShowTag"]/div[contains(@class, "row2")]/a/text()').extract()
        if tags:
            for ti, t in enumerate(tags):
                if t:
                    tags[ti] = t.replace(',', '').strip()
            news['tags'] = ", ".join(tags)
        else:
            news['tags'] = ""

        stock_tags = []
        for t in self.tradecenters:
            if re.search(r'\b%s\b' % t, news['html'], re.IGNORECASE):
                stock_tags.append(t)
            elif re.search(r'\b%s\b' % t, news['title'], re.IGNORECASE):
                stock_tags.append(t)
        if stock_tags:
            news['stock_tags'] = ", ".join(stock_tags)
        else:
            news['stock_tags'] = ""

        com_tags = []
        for s in self.symbols:
            if re.search(r'\b%s\b' % s, news['html']):
                com_tags.append(s)
            elif re.search(r'\b%s\b' % s, news['title']):
                com_tags.append(s)
        if com_tags:
            news['com_tags'] = ", ".join(com_tags)
        else:
            news['com_tags'] = ""

        fields_ = '('
        vals_ = '('
        for i, v in news.iteritems():
            fields_ += '%s, ' % i
            if not v:
                vals_ += '"", '
            else:
                v = str(v).strip()
                vals_ += '"%s", ' % self.db.escape_string(v)
        fields_ = fields_ + 'created, updated)'
        vals_ = vals_ + 'NOW(), NOW())'
        sql = 'INSERT INTO %s %s VALUES %s' % (self.config['TABLE'], fields_, vals_)
        self.dbc.execute(sql)
        self.db.commit()