# -*- coding: utf-8 -*-
import scrapy, os, time, MySQLdb, re, json
from HTMLParser import HTMLParser
from dateutil import parser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class NcdtBusSpider(scrapy.Spider):
    name = 'ncdtbus'
    allowed_domains = ['nhipcaudautu.vn']
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
        self.config = self.settings.get('NCDT')
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

        yield scrapy.Request(self.config['URL'])

    def parse(self, response):

        new = 0
        fnewstop = {}
        links = {'url':[], 'title': []}
        fnewstop['title'] = response.xpath('//div[contains(@class, "container-post-wrap")][1]//div[contains(@class, "post-thumbnail")]/a/@title').extract()
        fnewstop['link'] = response.xpath('//div[contains(@class, "container-post-wrap")][1]//div[contains(@class, "post-thumbnail")]/a/@href').extract()
        for fi, f in enumerate(fnewstop['link']):
            fnewstop['link'][fi] = "%s%s" % (self.config['ROOT'], f.strip())
            if not fnewstop['link'][fi] in self.urls:
                links['url'].append(fnewstop['link'][fi])
                links['title'].append(fnewstop['title'][fi])
                new += 1

        fnewslist = {}
        fnewslist['title'] = response.xpath('//div[contains(@class, "container-post-wrap")][2]//p[contains(@class, "entry-title")]/a/@title').extract()
        fnewslist['link'] = response.xpath('//div[contains(@class, "container-post-wrap")][2]//p[contains(@class, "entry-title")]/a/@href').extract()
        for fi, f in enumerate(fnewslist['link']):
            fnewslist['link'][fi] = "%s%s" % (self.config['ROOT'], f.strip())
            if not fnewslist['link'][fi] in self.urls:
                links['url'].append(fnewslist['link'][fi])
                links['title'].append(fnewslist['title'][fi])
                new += 1
        total = len(fnewstop['link']) + len(fnewslist['link'])

        self.dbc.execute('INSERT INTO %s (`from`, `url`, `type`, `raw`, `total`, `new`, `created`) VALUES ("%s", "%s", "%s", "%s", "%d", "%s", NOW())' % (self.config['TABLEC'], self.config['FROM'], response.url, self.config['TYPE'], self.db.escape_string(json.dumps({'top': fnewstop, 'list': fnewslist}, ensure_ascii=False)), total, new))
        self.db.commit()
        if self.dbc.lastrowid:
            self.crawlid = self.dbc.lastrowid
        for li, l in enumerate(links['url']):
            yield scrapy.Request(url=l, callback=self.parse_news, meta={'title': links['title'][li]})

    def parse_news(self, response):
        news = {}
        news['title'] = response.meta['title']
        news['url'] = response.url
        news['category'] = self.config['CATEGORY']
        lastpub = response.xpath('//span[contains(@class, "date-post")]/text()[last()]').extract_first()
        news['published'] = response.xpath('//span[contains(@class, "date-post")]/span/text()').extract_first() + lastpub
        news['published_at'] = self._strtostamp(lastpub)
        news['crawl_id'] = self.crawlid
        #news['author'] = response.xpath('//div[contains(@class, "bysource")]/preceding::p[@style="text-align: right;"]/strong/text()').extract_first()
        #if not news['author']:
        #    news['author'] = response.xpath('//div[@if="end-content"]/preceding::p[@style="text-align: right;"]/strong/text()').extract_first()
        news['author'] = response.xpath('//p[@style="text-align: right;" or @style="text-align:right"]/strong/text()').extract_first()
        news['short_content'] = response.xpath('//div[contains(@class, "des-small")]/text()[last()]').extract_first()
        news['html'] = response.xpath('//div[contains(@class, "content-detail")]').extract_first()
        # remove author
        if news['html']:
            news['html'] = re.sub('<p style="text-align: right;"><strong>(.*?)<strong><\/p>', '', news['html'])

            content = {
                'body': {
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
                    content['body']['children'].append({
                        'type': self.config['NFC']['OBJECT']['TEXT'],
                        'align': self.config['NFC']['ALIGN']['LEFT'],
                        'text': [{
                            'text': self.strip_tags(c),
                            'fontStyle': self.config['NFC']['FONTSTYLE']['NORMAL']
                        }]
                    })
            if content:
                news['content'] = json.dumps(content, ensure_ascii=False)

        figure = response.xpath('//div[contains(@class, "container-post-detail")]//div[contains(@class, "post-container")]//div[contains(@class, "col-lg-9")]/img/@src').extract_first()
        if figure:
            news['figure'] = figure
            news['figure_type'] = 'img'
        news['source'] = response.xpath('//div[contains(@class, "bysource")]').extract_first()
        if news['source']:
            news['source'] = self.strip_tags(news['source'])
        news['video_url'] = ''

        tags = response.xpath('//div[contains(@class, "post-tags")]/a/@title').extract()
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
                # a0, not space
                v = str(v).strip().replace(' ', '')
                vals_ += '"%s", ' % self.db.escape_string(v)
        fields_ = fields_ + 'created, updated)'
        vals_ = vals_ + 'NOW(), NOW())'
        sql = 'INSERT INTO %s %s VALUES %s' % (self.config['TABLE'], fields_, vals_)
        self.dbc.execute(sql)
        self.db.commit()