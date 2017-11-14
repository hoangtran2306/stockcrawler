# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from scrapy.http import Request
from HTMLParser import HTMLParser
from dateutil import parser

import MySQLdb, sys, os, time, re, json, hashlib

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

reload(sys)
sys.setdefaultencoding('utf8')

class VTVEcoSpider(XMLFeedSpider):
    name = 'vtveco'
    allowed_domains = ['vtv.vn']
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
        self.config = self.settings.get('VTVECO')
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
        news['short_content'] = response.xpath('//h2[contains(@class, "sapo")]/text()').extract_first()

        figure = response.xpath('//img[contains(@class, "news-avatar")]/@src').extract_first()
        video_url = None
        if figure:
            figure_type = 'img'
        else:
            figure_key = re.search('%s[\'|"]:[\'|"](%s\/){0,1}(.*?)[\'|"],' % (self.config['VKINDEX'], self.config['VKPREFIX']), response.body)
            if figure_key:
                figure_key = '%s/%s' % (self.config['VKPREFIX'], figure_key.group(2))
                figure_type = 'video'
                figure = re.sub(r'(.*)%s' % ('.%s' % self.config['VTYPE']),r'\1%s'  % ('.%s' % self.config['VTTYPE']), '%s%s' % (self.config['VTPREFIX'], figure_key))

                video_url = '%s%s' %(self.config['VPREFIX'], figure_key)

        if figure:
            news['figure'] = figure
            news['figure_type'] = figure_type
        else:
            news['figure'] = ""

        if video_url:
            news['video_url'] = video_url
        else:
            news['video_url'] = ""

        news['html'] = response.xpath('//div[contains(@class, "ta-justify")]').extract_first()
        if news['html']:
            html = re.search(ur'(.*)<p>(.*)Mời quý độc giả(.*)<\/p>', news['html'])
            if html:
                news['html'] = html.group(1)
            html = re.search('(.*)<div type="Related(One){0,1}News"(.*)<\/div>', news['html'])
            if html:
                news['html'] = html.group(1)
            content = {
                'body': {
                    'type': self.config['NFC']['OBJECT']['VIEW'],
                    'align': self.config['NFC']['ALIGN']['CENTER'],
                    'children': [],
                    'color': self.config['NFC']['DFCOLOR']
                }
            }
            if news['video_url']:
                content['video'] = []
                content['video'].append({
                    'file_url': news['video_url'],
                    'file_url_md5': hashlib.md5(news['video_url']).hexdigest(),
                    'position': 0,
                    'order': 0
                })
                content['body']['children'].append({
                    'type': self.config['NFC']['OBJECT']['VIDEO'],
                    'align': self.config['NFC']['ALIGN']['CENTER'],
                    'videoIndex': 0
                })
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

        tags = response.xpath('//div[contains(@class, "news_keyword")]/a/text()').extract()
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