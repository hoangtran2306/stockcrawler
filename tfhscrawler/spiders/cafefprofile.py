# -*- coding: utf-8 -*-
import scrapy, MySQLdb, datetime, sys, pprint, time, os, re

reload(sys)
sys.setdefaultencoding('utf8')

class CafefProfileSpider(scrapy.Spider):
    name = 'cafefprofile'
    allowed_domains = ['s.cafef.vn']
    # should we crawl basic profiles or not?
    bcrawl = False

    def is_number(self, s):
        if s:
            s = s.strip().replace(',', '')
        else:
            return False
        if s == 'Infinity':
            return False
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def start_requests(self):
        self.config = self.settings.get('CAFEFPROFILE')
        self.download_delay = self.config['DOWNLOAD_DELAY']
        dbconfig = self.settings.get('DB')
        tz = self.settings.get('TIMEZONE')
        os.environ['TZ'] = tz
        time.tzset()
        dbtz = self.settings.get('DBTZ')

        bstime_ = self.config['BTIME']['START']
        # days
        interval_ = self.config['BTIME']['INTERVAL']
        bstime_ = datetime.datetime.strptime(bstime_, '%Y/%m/%d').date()
        now = datetime.datetime.now().date()
        if now >= bstime_ and (now - bstime_).days % int(interval_) == 0:
            self.bcrawl = True
        else:
            self.bcrawl = False

        #self.db = MySQLdb.connect(dbconfig['HOST'], dbconfig['USER'], dbconfig['PWD'], dbconfig['DB'])
        self.db = MySQLdb.connect(dbconfig['HOST'], dbconfig['USER'], dbconfig['PWD'], dbconfig['DB'], use_unicode=True, charset="utf8")
        if not self.db:
            print "cannot connect to database"
        self.dbc = self.db.cursor()
        self.dbc.execute('SET time_zone="%s"' % dbtz)
        self.db.commit()
        self.dbc.execute('SELECT symbol, profile_link FROM %s WHERE on_board = 1' % self.config['COMTABLE'])
        dbdata = self.dbc.fetchall()
        if dbdata:
            for row in dbdata:
                req = scrapy.Request(url=row[1])
                req.meta['symbol'] = row[0]
                yield req

    def parse(self, response):
        if 's.cafef.vn' in self.crawler.engine.downloader.slots:
            self.crawler.engine.downloader.slots['s.cafef.vn'].delay = self.config['API_DOWNLOAD_DELAY']
        v1 = response.xpath("//div[@id='contentV1']")
        # template version 1
        if v1:
            sitem = {}
            sitem['updated_time'] = response.xpath("//div[contains(@class, 'update')]/text()").extract_first()
            sitem['match_price'] = response.xpath("//div[contains(@class, 'pri')]/text()").extract_first()
            if not self.is_number(sitem['match_price']):
                sitem['match_price'] = 0
            pchange = response.xpath("//div[contains(@class, 'chan') or contains(@class, 'cno')]/text()").re('([-+]?\d*\.\d+|\d+)')
            if pchange:
                sitem['price_change'] = pchange[0]
                if not self.is_number(sitem['price_change']):
                    sitem['price_change'] = 0
                sitem['price_change_per'] = pchange[1]
                if not self.is_number(sitem['price_change_per']):
                    sitem['price_change_per'] = 0
            sitem['accumylated_vol'] = response.xpath("//div[contains(@class, 'vl')]/text()").extract_first()
            if not self.is_number(sitem['accumylated_vol']):
                sitem['accumylated_vol'] = 0
            # no data
            sitem['basic_price'] = 0
            # no data
            sitem['ceiling_price'] = 0
            # no data
            sitem['floor_price'] = 0
            sitem['open_price'] = response.xpath("//div[contains(@class, 'opri')]/text()").extract_first()
            if not self.is_number(sitem['open_price']):
                sitem['open_price'] = 0
            sitem['highest_price'] = response.xpath("(//div[contains(@class, 'opri')])[2]/text()").extract_first()
            if not self.is_number(sitem['highest_price']):
                sitem['highest_price'] = 0
            sitem['lowest_price'] = response.xpath("(//div[contains(@class, 'opri')])[3]/text()").extract_first()
            if not self.is_number(sitem['lowest_price']):
                sitem['lowest_price'] = 0
            sitem['nfi_trans'] = response.xpath("(//div[contains(@class, 'vl')])[2]/text()").re_first('([-+]?\d*\.\d+|\d+)')
            if not self.is_number(sitem['nfi_trans']):
                sitem['nfi_trans'] = 0
            sitem['remained_room'] = response.xpath("(//div[contains(@class, 'vl')])[3]/text()").re_first('([-+]?\d*\.\d+|\d+)')
            if not self.is_number(sitem['remained_room']):
                sitem['remained_room'] = 0
            sitem['basic_eps'] = response.xpath("//div[contains(@class, 'tidown')]/ul/li[1]/span[contains(@class, 'value')]/text()").extract_first()
            if not self.is_number(sitem['basic_eps']):
                sitem['basic_eps'] = 0
            sitem['diluted_eps'] = response.xpath("//div[contains(@class, 'tidown')]/ul/li[2]/span[contains(@class, 'value')]/text()").extract_first()
            if not self.is_number(sitem['diluted_eps']):
                sitem['diluted_eps'] = 0
            sitem['pe'] = response.xpath("//div[contains(@class, 'tidown')]/ul/li[3]/span[contains(@class, 'value')]/text()").extract_first()
            if not self.is_number(sitem['pe']):
                sitem['pe'] = 0
            sitem['book_value'] = response.xpath("//div[contains(@class, 'tidown')]/ul/li[4]/span[contains(@class, 'value')]/text()").extract_first()
            if not self.is_number(sitem['book_value']):
                sitem['book_value'] = 0
            sitem['the_beta'] = response.xpath("//div[contains(@class, 'tidown')]/ul/li[5]/span[contains(@class, 'value')]/text()").extract_first()
            if not self.is_number(sitem['the_beta']):
                sitem['the_beta'] = 0
            sitem['avg_trading_vol'] = response.xpath("//div[contains(@class, 'tidown')]/ul/li[6]/span[contains(@class, 'value')]/text()").extract_first()
            if not self.is_number(sitem['avg_trading_vol']):
                sitem['avg_trading_vol'] = 0
            sitem['listed_share_vol'] = response.xpath("//div[contains(@class, 'tidown')]/ul/li[7]/span[contains(@class, 'value')]/text()").extract_first()
            if not self.is_number(sitem['listed_share_vol']):
                sitem['listed_share_vol'] = 0
            sitem['circulation_vol'] = response.xpath("//div[contains(@class, 'tidown')]/ul/li[8]/span[contains(@class, 'value')]/text()").extract_first()
            if not self.is_number(sitem['circulation_vol']):
                sitem['circulation_vol'] = 0
            sitem['market_cap'] = response.xpath("//div[contains(@class, 'tidown')]/ul/li[9]/span[contains(@class, 'value')]/text()").extract_first()
            if not self.is_number(sitem['market_cap']):
                sitem['market_cap'] = 0
            sitem['symbol'] = response.meta['symbol']
            # template version 1
            sitem['template'] = 1

            if self.bcrawl:
                bitem = {}
                bitem['template'] = 1
                bitem['symbol'] = response.meta['symbol']
                bitem['financial_info'] = {}
                bitem['leadership_ownership'] = response.xpath('//div[@id="bCeoBox"]').extract_first()
                bitem['first_trading_date'] = response.xpath('//div[contains(@class, "dltr-other")]/div[1]/b/text()').extract_first()
                bitem['first_price'] = response.xpath('//div[contains(@class, "dltr-other")]/div[2]/b/text()').extract_first()
                if not self.is_number(bitem['first_price']):
                    bitem['first_price'] = 0
                else:
                    bitem['first_price'] = bitem['first_price'].replace(',', '')
                bitem['first_vol'] = response.xpath('//div[contains(@class, "dltr-other")]/div[3]/b/text()').extract_first()
                if not self.is_number(bitem['first_vol']):
                    bitem['first_vol'] = 0
                else:
                    bitem['first_vol'] = bitem['first_vol'].replace(',', '')

                # financial information
                yield scrapy.Request(url=self.config['BURLS']['V1']['FININF']['QUARTER'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_fininfq1)

        # template version 2
        else:
            sitem = {}
            sitem['updated_time'] = response.xpath("//div[contains(@class, 'dltlu-time')]/text()").extract_first()
            sitem['match_price'] = response.xpath("//div[contains(@class, 'dltlu-point')]/text()").extract_first()
            if not self.is_number(sitem['match_price']):
                sitem['match_price'] = 0
            pchange = response.xpath("//div[contains(@class, 'dltlu-down') or contains(@class, 'dltlu-up') or contains(@class, 'dltlu-nochange')]/text()").re('([-+]?\d*\.\d+|\d+)')
            if pchange:
                sitem['price_change'] = pchange[0]
                sitem['price_change_per'] = pchange[1]

            sitem['accumylated_vol'] = response.xpath("//div[@id='CV']/text()").extract_first()
            if not self.is_number(sitem['accumylated_vol']):
                sitem['accumylated_vol'] = 0
            sitem['basic_price'] = response.xpath("//div[@id='REF']/text()").extract_first()
            if not self.is_number(sitem['basic_price']):
                sitem['basic_price'] = 0
            sitem['ceiling_price'] = response.xpath("//div[@id='CE']/text()").extract_first()
            if not self.is_number(sitem['ceiling_price']):
                sitem['ceiling_price'] = 0
            sitem['floor_price'] = response.xpath("//div[@id='FL']/text()").extract_first()
            if not self.is_number(sitem['floor_price']):
                sitem['floor_price'] = 0
            sitem['open_price'] = response.xpath("//div[@id='FL']/following::li[1]/div[contains(@class, 'right')]/text()").extract_first()
            if not self.is_number(sitem['open_price']):
                sitem['open_price'] = 0
            sitem['highest_price'] = response.xpath("//div[@id='FL']/following::li[2]/div[contains(@class, 'right')]/text()").extract_first()
            if not self.is_number(sitem['highest_price']):
                sitem['highest_price'] = 0
            sitem['lowest_price'] = response.xpath("//div[@id='FL']/following::li[3]/div[contains(@class, 'right')]/text()").extract_first()
            if not self.is_number(sitem['lowest_price']):
                sitem['lowest_price'] = 0
            # GDNN (KL Bán)
            sitem['sell_foreign_qtty'] = response.xpath("//div[@id='FrSell']/text()").extract_first()
            if not self.is_number(sitem['sell_foreign_qtty']):
                sitem['sell_foreign_qtty'] = 0
            if sitem['sell_foreign_qtty']:
                # GDNN (KL Mua)
                sitem['buy_foreign_qtty'] = response.xpath("//li[@id='ctl00_ContentPlaceHolder1_ucTradeInfo_liFrSell']/preceding::li[1]/div[contains(@class, 'right')]/text()").extract_first()
                if not self.is_number(sitem['buy_foreign_qtty']):
                    sitem['buy_foreign_qtty'] = 0
            else:
                # GD ròng NĐTNN
                sitem['nfi_trans'] = response.xpath("//li[@id='ctl00_ContentPlaceHolder1_ucTradeInfo_divRoomNNConlai']/preceding::li[1]/div[contains(@class, 'right')]/text()").extract_first()
                if not self.is_number(sitem['nfi_trans']):
                    sitem['nfi_trans'] = 0
            sitem['remained_room'] = response.xpath("//li[@id='ctl00_ContentPlaceHolder1_ucTradeInfo_divRoomNNConlai']/div[contains(@class, 'right')]/text()").re_first('([-+]?\d*\.\d+|\d+)')
            if not self.is_number(sitem['remained_room']):
                sitem['remained_room'] = 0
            sitem['basic_eps'] = response.xpath('//div[@id="ctl00_ContentPlaceHolder1_ucTradeInfo_pnEPS"]/li[1]/div[contains(@class, "r")]/text()').extract_first()
            if not self.is_number(sitem['basic_eps']):
                sitem['basic_eps'] = 0
            sitem['diluted_eps'] = response.xpath('//div[@id="ctl00_ContentPlaceHolder1_ucTradeInfo_pnEPS"]/li[2]/div[contains(@class, "r")]/text()').extract_first()
            if not self.is_number(sitem['diluted_eps']):
                sitem['diluted_eps'] = 0
            sitem['pe'] = response.xpath('//div[@id="ctl00_ContentPlaceHolder1_ucTradeInfo_pnEPS"]/li[3]/div[contains(@class, "r")]/text()').extract_first()
            if not self.is_number(sitem['pe']):
                sitem['pe'] = 0
            sitem['book_value'] = response.xpath("//div[contains(@class, 'dltl-other')]/ul/li[1]/div[contains(@class, 'r')]/text()").extract_first()
            if not self.is_number(sitem['book_value']):
                sitem['book_value'] = 0
            sitem['the_beta'] = response.xpath("//div[contains(@class, 'dltl-other')]/ul/li[2]/div[contains(@class, 'r')]/text()").extract_first()
            if not self.is_number(sitem['the_beta']):
                sitem['the_beta'] = 0
            sitem['avg_trading_vol'] = response.xpath("//div[contains(@class, 'dltl-other')]/ul/li[3]/div[contains(@class, 'r')]/text()").extract_first()
            if not self.is_number(sitem['avg_trading_vol']):
                sitem['avg_trading_vol'] = 0
            sitem['listed_share_vol'] = response.xpath("//div[contains(@class, 'dltl-other')]/ul/li[4]/div[contains(@class, 'r')]/text()").extract_first()
            if not self.is_number(sitem['listed_share_vol']):
                sitem['listed_share_vol'] = 0
            sitem['circulation_vol'] = response.xpath("//div[contains(@class, 'dltl-other')]/ul/li[5]/div[contains(@class, 'r')]/text()").extract_first()
            if not self.is_number(sitem['circulation_vol']):
                sitem['circulation_vol'] = 0
            sitem['market_cap'] = response.xpath("//div[contains(@class, 'dltl-other')]/ul/li[6]/div[contains(@class, 'r')]/text()").extract_first()
            if not self.is_number(sitem['market_cap']):
                sitem['market_cap'] = 0
            sitem['symbol'] = response.meta['symbol']
            # template version 2
            sitem['template'] = 2

            if self.bcrawl:
                bitem = {}
                bitem['template'] = 2
                bitem['symbol'] = response.meta['symbol']
                bitem['financial_info'] = {}
                bitem['logo'] = response.xpath("//div[contains(@class, 'avartar')]/img/@src").extract_first()
                bitem['intro'] = response.xpath("//div[contains(@class, 'companyIntro')]/text()").extract_first()
                # div chứa chi tiết
                ddetail = response.xpath("//div[@id='ctl00_ContentPlaceHolder1_ucTradeInfo_divFirstInfo']").extract_first()
                if ddetail:
                    bitem['first_trading_date'] = response.xpath('//div[contains(@class, "dltr-other")]/div[2]/b/text()').extract_first()
                    bitem['first_price'] = response.xpath('//div[contains(@class, "dltr-other")]/div[3]/b/text()').extract_first()
                else:
                    bitem['first_trading_date'] = response.xpath('//div[contains(@class, "dltr-other")]/div[1]/b/text()').extract_first()
                    bitem['first_price'] = response.xpath('//div[contains(@class, "dltr-other")]/div[2]/b/text()').extract_first()
                if not self.is_number(bitem['first_price']):
                    bitem['first_price'] = 0
                else:
                    bitem['first_price'] = bitem['first_price'].replace(',', '')
                bitem['first_vol'] = response.xpath('//div[contains(@class, "dltr-other")]/div[3]/b/text()').extract_first()
                if not self.is_number(bitem['first_vol']):
                    bitem['first_vol'] = 0
                else:
                    bitem['first_vol'] = bitem['first_vol'].replace(',', '')

                # financial information
                yield scrapy.Request(url=self.config['BURLS']['V2']['FININF']['QUARTER'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_fininfq2)

        '''
            stock profile
        '''
        if sitem['updated_time']:
            sitem['updated_time'] = sitem['updated_time'].replace('Cập nhật lúc ', '')

        fields_ = '('
        vals_ = '('
        for i, v in sitem.iteritems():
            fields_ += '%s, ' % i
            if v and isinstance(v, basestring):
                v = v.replace(',','').strip()
            if v == '':
                vals_ += '"", '
            else:
                vals_ += '"%s", ' % v
        fields_ = fields_ + 'created)'
        vals_ = vals_ + 'NOW())'
        sql = 'INSERT INTO %s %s VALUES %s' % (self.config['STABLE'], fields_, vals_)
        self.dbc.execute(sql)
        self.db.commit()

    ########################################################-{V1}-

    def parse_fininfq1(self, response):
        if 's.cafef.vn' in self.crawler.engine.downloader.slots:
            self.crawler.engine.downloader.slots['s.cafef.vn'].delay = self.config['API_DOWNLOAD_DELAY']
        bitem = response.meta['item']
        bitem['financial_info']['QUATER'] = response.body
        # financial information
        yield scrapy.Request(url=self.config['BURLS']['V1']['FININF']['YEAR'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_fininfy1)

    def parse_fininfy1(self, response):
        bitem = response.meta['item']
        bitem['financial_info']['YEAR'] = response.body
        # financial information
        yield scrapy.Request(url=self.config['BURLS']['V1']['FININF']['6MONS'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_fininfm1)

    def parse_fininfm1(self, response):
        bitem = response.meta['item']
        bitem['financial_info']['6MONS'] = response.body
         # basic info
        yield scrapy.Request(url=self.config['BURLS']['V1']['BASINF'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_basinf1)

    def parse_basinf1(self, response):
        bitem = response.meta['item']
        bitem['basic_info'] = response.body
        bitem['website'] = response.body
        # leadership & ownership
        yield scrapy.Request(url=self.config['BURLS']['V1']['AFFINF'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_affinf1)

    def parse_affinf1(self, response):
        bitem = response.meta['item']
        bitem['affiliates'] = response.body
        # financial reports
        yield scrapy.Request(url=self.config['BURLS']['V1']['FINRPT'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_finrpt1)

    def parse_finrpt1(self, response):
        bitem = response.meta['item']
        bitem['financial_reports'] = response.body

        '''
            basic profile
        '''
        fields_ = '('
        vals_ = '('
        for i, v in bitem.iteritems():
            fields_ += '%s, ' % i
            if not v and v is not 0:
                vals_ += '"", '
            else:
                v = str(v).strip()
                vals_ += '"%s", ' % self.db.escape_string(v)
        fields_ = fields_ + 'created)'
        vals_ = vals_ + 'NOW())'
        sql = 'INSERT INTO %s %s VALUES %s' % (self.config['BTABLE'], fields_, vals_)
        self.dbc.execute(sql)
        self.db.commit()

    ########################################################-{V2}-

    def parse_fininfq2(self, response):
        if 's.cafef.vn' in self.crawler.engine.downloader.slots:
            self.crawler.engine.downloader.slots['s.cafef.vn'].delay = self.config['API_DOWNLOAD_DELAY']
        bitem = response.meta['item']
        bitem['financial_info']['QUARTER'] = response.body
        # financial information
        yield scrapy.Request(url=self.config['BURLS']['V2']['FININF']['YEAR'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_fininfy2)

    def parse_fininfy2(self, response):
        bitem = response.meta['item']
        bitem['financial_info']['YEAR'] = response.body
        # financial information
        yield scrapy.Request(url=self.config['BURLS']['V2']['FININF']['6MONS'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_fininfm2)

    def parse_fininfm2(self, response):
        bitem = response.meta['item']
        bitem['financial_info']['6MONS'] = response.body
         # basic info
        yield scrapy.Request(url=self.config['BURLS']['V2']['BASINF'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_basinf2)

    def parse_basinf2(self, response):
        bitem = response.meta['item']
        bitem['basic_info'] =  response.body
        bweb = re.search("Website:<\/b> <a href=['|\"](.*?)['|\"]", response.body)
        if bweb:
            bitem['website'] = bweb.group(1)
        else:
            bitem['website'] = ""
        # leadership & ownership
        yield scrapy.Request(url=self.config['BURLS']['V2']['LOINF'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_loinf2)

    def parse_loinf2(self, response):
        bitem = response.meta['item']
        bitem['leadership_ownership'] = response.body
        # affiliates
        yield scrapy.Request(url=self.config['BURLS']['V2']['AFFINF'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_affinf2)

    def parse_affinf2(self, response):
        bitem = response.meta['item']
        bitem['affiliates'] = response.body
        # financial reports
        yield scrapy.Request(url=self.config['BURLS']['V2']['FINRPT'] % bitem['symbol'], meta={'item': bitem}, callback=self.parse_finrpt2)

    def parse_finrpt2(self, response):
        bitem = response.meta['item']
        bitem['financial_reports'] = response.body

        '''
            basic profile
        '''
        fields_ = '('
        vals_ = '('
        for i, v in bitem.iteritems():
            fields_ += '%s, ' % i
            if not v and v is not 0:
                vals_ += '"", '
            else:
                v = str(v).strip()
                vals_ += '"%s", ' % self.db.escape_string(v)
        fields_ = fields_ + 'created)'
        vals_ = vals_ + 'NOW())'
        sql = 'INSERT INTO %s %s VALUES %s' % (self.config['BTABLE'], fields_, vals_)
        self.dbc.execute(sql)
        self.db.commit()