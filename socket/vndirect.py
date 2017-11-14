# -*- coding: utf-8 -*-
import MySQLdb, memcache, websocket, thread, datetime, time, sys, os, random, string, json, pprint
import logging, logging.config
import config, calendar

reload(sys)
sys.setdefaultencoding('utf8')
os.environ['TZ'] = config.TIMEZONE
time.tzset()

# websocket-client commands
CMD = None
# current servers
SERVERS = None

# last daily time
LDTIME = None
# last monthly time
LMTIME = None
# last annualy time
LATIME = None

_MINS = False
_MINSD = None
_AINS = False
_AINSD = None

# logging
logger = logging.getLogger()
SA = config.LOG['levels']['SA']
SQ = config.LOG['levels']['SQ']

# get current trading time
# date int: miliseconds unix timestamp
# time string: in %H:%M:%S time format
def getcttime(date, time):
    s = int(date) / 1000.0
    dt = datetime.datetime.fromtimestamp(s)
    st = datetime.datetime.strptime(time, "%H:%M:%S")
    return dt.replace(hour=st.time().hour, minute=st.time().minute, second=st.time().second, microsecond=0)

# get last active ending time
def getcaetime():
    now = datetime.datetime.now()
    etime = datetime.datetime.strptime(config.ACTIVE['END'], "%H:%M")
    return now.replace(hour=etime.time().hour, minute=etime.time().minute, second=0, microsecond=0)

# get different between two datetime by seconds
def gettdiff(dt1, dt2):
    return int((dt1 - dt2).total_seconds())

def _memconnect(host, port, dflag):
    global mc
    if not host:
        logger.error('memcached host is empty')
        sys.exit()
    if not port:
        post = 11211
    mc = memcache.Client(['%s:%s' % (host, port)], debug=dflag)
    mc.set('connected', '1')

    if not mc.get('connected'):
        logger.error('error occurred when trying to initilize memcached connection')
        sys.exit()
    else:
        logger.info('memcached connection created successfuly')

# get current server(s)
def getcs(newday = False):
    global SERVERS, _MINS, _AINS
    # reset global variables
    if newday:
        if _MINSD is not None:
            _diff = (datetime.datetime.now().date() - _MINSD).days
            if _diff >= config.STATS['MINTERVAL']:
                _MINS = False
        if _AINSD is not None:
            _diff = (datetime.datetime.now().date() - _AINSD).days
            if _diff >= config.STATS['AINTERVAL']:
                _AINS = False
    if SERVERS == None:
        SERVERS = []
        _dbselect("SELECT url FROM %s" % config.CMNTABLES['VNDCURL'])
        for row in dbdata:
            SERVERS.append(row[0])
    if not SERVERS:
        logger.error('cannot get server list, halt')
        sys.exit()

    config._SOCKET['SERVER'] = random.choice(SERVERS)
    param1 = random.randint(100, 999)
    param2 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    config._SOCKET['URL'] = 'wss://' + config._SOCKET['SERVER'] + '/realtime/' + str(param1) + '/' + param2 + '/websocket'

def nowunix():
    now = datetime.datetime.now()
    current = time.mktime(now.timetuple())*1e3 + now.microsecond/1e3
    return current

def _dbopen():
    global db, dbc
    logger.info('open database connection to %s' % config.DB['HOST'])
    # open database connection
    db = MySQLdb.connect(config.DB['HOST'], config.DB['USER'], config.DB['PWD'], config.DB['DB'])
    if not db:
        logger.error('cannot connect to database, halt')
        sys.exit()
    # prepare a cursor object using cursor() method
    dbc = db.cursor()
    # set session timezone
    logger.info('set database timezone to %s', config.DBTZ)
    dbc.execute('SET time_zone="%s"' % config.DBTZ)
    db.commit()
    if (config._SOCKET['ACTIVE'] == 'forever'):
        logger.info('data to process is set to keep forever')
    else:
        # clear old data
        _dbselect('SELECT MAX(%s) FROM %s' % (config._SOCKET['FIELDT'][1], config._SOCKET['FIELDT'][0]))
        if dbdata[0][0]:
            m, _ = divmod(dbdata[0][0] / 1000, 1)
            # last data date (trading time)
            m = datetime.datetime.fromtimestamp(m).strftime('%Y-%m-%d')
            logger.info('last trading time: %s', m)
            # clear point
            atime = strtodelta(config._SOCKET['ACTIVE']).date()
            logger.info('clear point: %s', atime)
            if (str(atime) >= m):
                logger.info('clear point is greater than or equal to last trading date, do clean up')
                clearfredata()
            else:
                logger.info('clear point is less than last trading date, keep current data sheet')
        else:
            logger.info('no previous data found on frequence tables, keep cleaning task')

def clearfredata():
    for t in config._SOCKET['TABLET']:
        logger.info('clear %s table...', t)
        #dbc.execute('TRUNCATE TABLE `%s`' % t)
        dbc.execute('DELETE FROM `%s` WHERE id > 0' % t)
    db.commit()
    logger.info('done')

def _dbselect(q):
    global dbc, dbdata
    # execute SQL query using execute() method.
    try:
        dbc.execute(q)
        # Fetch a single row using fetchone() method.
        dbdata = dbc.fetchall()
    except Exception as ex:
        logger.error(str(ex))
        _dbclose()
        _dbopen()
        dbc.execute(q)
        dbdata = dbc.fetchall()

def _dbinsert(q):
    global dbc
    # execute SQL query using execute() method.
    try:
        dbc.execute(q)
        db.commit()
    except Exception as ex:
        logger.error(str(ex))
        _dbclose()
        _dbopen()
        dbc.execute(q)
        db.commit()

def _dbclose():
    global db
    # disconnect from database
    db.close()

def wscmd(cmd):
    global CMD, dbdata
    if CMD == None:
        CMD = {}
        _dbselect("SELECT type, command FROM %s" % config.CMNTABLES['VNDCCMD'])
        for row in dbdata:
            CMD[row[0]] = row[1]
    if cmd not in CMD:
        logger.error('command %s not found', cmd)
    else:
        return CMD[cmd]

def _wsmsg(ws, message):
    global LDTIME, _MINS, _MINSD, _AINS, _AINSD, dbdata
    logger.log(SA, message)

    laetime = getcaetime()
    if laetime <= datetime.datetime.now():
        if not _MINS:
            _mins = False
            if config._SOCKET['TABLE'] == 'vndc_markets':
                _dbselect('SELECT vmk.floor_code, vmk.market_index, vmk.total_value_traded, vmk.trading_date FROM (SELECT floor_code, MAX(trading_time) AS mtt FROM {0} GROUP BY floor_code) AS tbl INNER JOIN {1} vmk ON vmk.floor_code = tbl.floor_code AND tbl.mtt = vmk.trading_time'.format(config._SOCKET['TABLE'], config._SOCKET['TABLE']))
                _sql = 'INSERT INTO `{0}` (`code`, `index`, `share`, `trading_date`, `created`) VALUES '.format(config.MSTMARKET)
                for row in dbdata:
                    if row[3] > 0:
                        _mins = True
                        _sql = _sql + '("{0}","{1}","{2}","{3}",NOW()), '.format(row[0], row[1], row[2], str(row[3])[:-3])
            else:
                _dbselect("SELECT vmk.code, IF(vmk.match_price, vmk.match_price, vmk.basic_price), vmk.accumylated_vol, vmk.`time`, vmk.trading_date FROM (SELECT `code`, MAX(`time`) AS mtt FROM {0} GROUP BY `code`) AS tbl INNER JOIN {1} vmk ON vmk.code = tbl.code AND tbl.mtt = vmk.time".format(config._SOCKET['TABLE'], config._SOCKET['TABLE']))
                _sql = 'INSERT INTO `{0}` (`floor`, `code`, `match_price`, `match_qtty`, `trading_date`, `created`) VALUES '.format(config.MSTSTOCK)
                for row in dbdata:
                    if row[4] > 0:
                        _mins = True
                        _sql = _sql + '("{0}","{1}","{2}","{3}","{4}",NOW()), '.format(config._SOCKET['FLOOR'], row[0], row[1], row[2], str(row[4])[:-3])

            if _mins:
                _sql = _sql[:-2]
                _dbinsert(_sql)
                _MINS = True
                _MINSD = datetime.datetime.now().date()

        if not _AINS:
            _ains = False
            if config._SOCKET['TABLE'] == 'vndc_markets':
                _dbselect('SELECT vmk.floor_code, vmk.market_index, vmk.total_value_traded, vmk.trading_date FROM (SELECT floor_code, MAX(trading_time) AS mtt FROM {0} GROUP BY floor_code) AS tbl INNER JOIN {1} vmk ON vmk.floor_code = tbl.floor_code AND tbl.mtt = vmk.trading_time'.format(config._SOCKET['TABLE'], config._SOCKET['TABLE']))
                _sql = 'INSERT INTO `{0}` (`code`, `index`, `share`, `trading_date`, `created`) VALUES '.format(config.ASTMARKET)
                for row in dbdata:
                    if row[3] > 0:
                        _ains = True
                        _sql = _sql + '("{0}","{1}","{2}","{3}",NOW()), '.format(row[0], row[1], row[2], str(row[3])[:-3])
            else:
                _dbselect("SELECT vmk.code, IF(vmk.match_price, vmk.match_price, vmk.basic_price), vmk.accumylated_vol, vmk.`time`, vmk.trading_date FROM (SELECT `code`, MAX(`time`) AS mtt FROM {0} GROUP BY `code`) AS tbl INNER JOIN {1} vmk ON vmk.code = tbl.code AND tbl.mtt = vmk.time".format(config._SOCKET['TABLE'], config._SOCKET['TABLE']))
                _sql = 'INSERT INTO `{0}` (`floor`, `code`, `match_price`, `match_qtty`, `trading_date`, `created`) VALUES '.format(config.ASTSTOCK)
                for row in dbdata:
                    if row[4] > 0:
                        _ains = True
                        _sql = _sql + '("{0}","{1}","{2}","{3}","{4}",NOW()), '.format(config._SOCKET['FLOOR'], row[0], row[1], row[2], str(row[4])[:-3])
            if _ains:
                _sql = _sql[:-2]
                _dbinsert(_sql)
                _AINS = True
                _AINSD = datetime.datetime.now().date()
    if message == 'h':
        hb = wscmd('heartbeat')
        ws.send(hb)
        logger.log(SQ, hb)
    elif "MARKETINFO" in message:
        sj = message.replace('\\', '')[3:-2]
        obj = json.loads(sj)
        ma = obj["data"].split('|')
        if config.APIDATA:
            # floor code
            if ma[11]:
                mem_ = mc.get(config._SOCKET['MEMKEY'])
                if mem_:
                    memo_ = json.loads(mem_)
                else:
                    memo_ = {}
                if ma[11] not in memo_:
                    memo_[ma[11]] = [''] * len(ma)

            for i, m in enumerate(ma):
                if m == '':
                    ma[i] = '0'
                elif ma[11]:
                    memo_[ma[11]][i] = m
            mc.set(config._SOCKET['MEMKEY'], json.dumps(memo_))
        else:
            for i, m in enumerate(ma):
                if m == '':
                    ma[i] = '0'

        _dbinsert("INSERT INTO {2} (url, command, response, created) VALUES ('{0}', 'market', '{1}', NOW())".format(config._SOCKET['URL'], message, config._SOCKET['TABLEC']))

        if dbc.lastrowid:
            ma[20] = dbc.lastrowid
        else:
            ma[20] = '0'
        _dbinsert("INSERT INTO {21} (market_id, total_trade, total_share_traded, total_value_traded, advance, decline, no_change, index_value, changed, trading_time, trading_date, floor_code, market_index, prior_market_index, highest_index, lowest_index, share_traded, status, sequence, prediction_market_index, crawl_id, created) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, '{9}', {10}, '{11}', {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, NOW())".format(ma[0], ma[1], ma[2], ma[3], ma[4], ma[5], ma[6], ma[7], ma[8], ma[9], ma[10], ma[11], ma[12], ma[13], ma[14], ma[15], ma[16], ma[17], ma[18], ma[19], ma[20], config._SOCKET['TABLE']))

        if ma[10] != '0' and float(ma[12]) > 0:
            # trading date, trading time
            cltime = getcttime(ma[10], ma[9])
            _dins = False

            if LDTIME:
                if not ma[11] in LDTIME:
                    LDTIME[ma[11]] = cltime
                    _dins = True
                else:
                    if gettdiff(cltime, LDTIME[ma[11]]) >= config.STATS['DINTERVAL'] * 60:
                        LDTIME[ma[11]] = cltime
                        _dins = True
            else:
                LDTIME = {}
                LDTIME[ma[11]] = cltime
                _dins = True

            if _dins:
                _sql = 'INSERT INTO `{0}` (`code`, `index`, `share`, `trading_date`, `time`, `created`) VALUES '.format(config.DSTMARKET)
                _sql = _sql + '("{0}","{1}","{2}","{3}","{4}",NOW())'.format(ma[11], ma[12], ma[2], ma[10][:-3], int(time.mktime(cltime.timetuple())))
                _dbinsert(_sql)

    elif 'STOCK' in message:
        sj = message.replace('\\', '')[3:-2]
        obj = json.loads(sj)
        if "data" in obj["data"]:
            data = obj["data"]["data"]
            dtype = 'many'
        else:
            data = obj["data"]
            dtype = 'one'

        if type(data) is not dict:
            data = {'data': data}

        _dbinsert("INSERT INTO {2} (url, command, response, created) VALUES ('{0}', 'stock', '{1}', NOW())".format(config._SOCKET['URL'], message, config._SOCKET['TABLEC']))

        if dbc.lastrowid:
            crawlid = dbc.lastrowid
        else:
            crawlid = '0'

        sql_ = "INSERT INTO {0} (floor_code, trading_date, time, code, company_name, stock_type, totalroom, current_room, basic_price, open_price, close_price, current_price, current_qtty, hieghest_price, lowest_price, ceiling_price, floor_price, total_offer_qtty, total_bid_qtty, match_price, match_qtty, match_value, average_price, bid_price01, bid_qtty01, bid_price02, bid_qtty02, bid_price03, bid_qtty03, offer_price01, offer_qtty01, offer_price02, offer_qtty02, offer_price03, offer_qtty03, accumulated_val, accumylated_vol, buy_foreign_qtty, sell_foreign_qtty, project_open, sequence, crawl_id, type, created) VALUES ".format(config._SOCKET['TABLE'])

        cnt_ = 0;
        _dins = False
        _dsql = 'INSERT INTO `{0}` (`floor`, `code`, `match_price`, `match_qtty`, `trading_date`, `time`, `created`) VALUES '.format(config.DSTSTOCK)
        if config.APIDATA:
            mem_ = mc.get(config._SOCKET['MEMKEY'])
            if mem_:
                memo_ = json.loads(mem_)
            else:
                memo_ = {}

            for sk, s in data.iteritems():
                sa = s.split('|')
                minx = None
                if sk == 'data':
                    if sa[3]:
                        minx = sa[3]
                else:
                    minx = sk
                if minx and minx not in memo_:
                    memo_[minx] = [''] * len(sa)
                if minx:
                    for i, m in enumerate(sa):
                        if m == '':
                            if i not in [0, 2, 3, 4, 5]:
                                sa[i] = '0'
                        else:
                            memo_[minx][i] = m
                else:
                    for i, m in enumerate(sa):
                        if m == '':
                            if i not in [0, 2, 3, 4, 5]:
                                sa[i] = '0'
                if cnt_ > 0:
                    sql_ += ','
                sql_ += "('{0}', {1}, '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, {22}, {23}, {24}, {25}, {26}, {27}, {28}, {29}, {30}, {31}, {32}, {33}, {34}, {35}, {36}, {37}, {38}, {39}, {40}, {41}, '{42}', NOW())".format(sa[0], sa[1], sa[2], sa[3], sa[4], sa[5], sa[6], sa[7], sa[8], sa[9], sa[10], sa[11], sa[12], sa[13], sa[14], sa[15], sa[16], sa[17], sa[18], sa[19], sa[20], sa[21], sa[22], sa[23], sa[24], sa[25], sa[26], sa[27], sa[28], sa[29], sa[30], sa[31], sa[32], sa[33], sa[34], sa[35], sa[36], sa[37], sa[38], sa[39], sa[40], crawlid, dtype)
                cnt_ += 1

                if sa[1] != '0' and float(sa[19]) > 0:
                    # trading date, trading time
                    cltime = getcttime(sa[1], sa[2])

                    if LDTIME:
                        if not sa[0] in LDTIME:
                            LDTIME[sa[0]] = {}
                            LDTIME[sa[0]][sa[3]] = cltime
                            _dins = True
                        else:
                            if not sa[3] in LDTIME[sa[0]]:
                                LDTIME[sa[0]][sa[3]] = cltime
                                _dins = True
                            elif gettdiff(cltime, LDTIME[sa[0]][sa[3]]) >= config.STATS['DINTERVAL'] * 60:
                                LDTIME[sa[0]][sa[3]] = cltime
                                _dins = True
                    else:
                        LDTIME = {}
                        LDTIME[sa[0]] = {}
                        LDTIME[sa[0]][sa[3]] = cltime
                        _dins = True
                    if _dins:
                        _dsql = _dsql + '("{0}","{1}","{2}","{3}","{4}","{5}",NOW()), '.format(config._SOCKET['FLOOR'], sa[3], sa[19], sa[20], sa[1][:-3], int(time.mktime(cltime.timetuple())))

            mc.set(config._SOCKET['MEMKEY'], json.dumps(memo_))
        else:
            for sk, s in data.iteritems():
                sa = s.split('|')
                for i, m in enumerate(sa):
                    if m == '':
                        if i not in [0, 2, 3, 4, 5]:
                            sa[i] = '0'

                if cnt_ > 0:
                    sql_ += ','
                sql_ += "('{0}', {1}, '{2}', '{3}', '{4}', '{5}', {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, {22}, {23}, {24}, {25}, {26}, {27}, {28}, {29}, {30}, {31}, {32}, {33}, {34}, {35}, {36}, {37}, {38}, {39}, {40}, {41}, '{42}', NOW())".format(sa[0], sa[1], sa[2], sa[3], sa[4], sa[5], sa[6], sa[7], sa[8], sa[9], sa[10], sa[11], sa[12], sa[13], sa[14], sa[15], sa[16], sa[17], sa[18], sa[19], sa[20], sa[21], sa[22], sa[23], sa[24], sa[25], sa[26], sa[27], sa[28], sa[29], sa[30], sa[31], sa[32], sa[33], sa[34], sa[35], sa[36], sa[37], sa[38], sa[39], sa[40], crawlid, dtype)
                cnt_ += 1
                if sa[1] != '0' and float(sa[19]) > 0:
                    # trading date, trading time
                    cltime = getcttime(sa[1], sa[2])

                    if LDTIME:
                        if not sa[0] in LDTIME:
                            LDTIME[sa[0]] = {}
                            LDTIME[sa[0]][sa[3]] = cltime
                            _dins = True
                        else:
                            if not sa[3] in LDTIME[sa[0]]:
                                LDTIME[sa[0]][sa[3]] = cltime
                                _dins = True
                            elif gettdiff(cltime, LDTIME[sa[0]][sa[3]]) >= config.STATS['DINTERVAL'] * 60:
                                LDTIME[sa[0]][sa[3]] = cltime
                                _dins = True
                    else:
                        LDTIME = {}
                        LDTIME[sa[0]] = {}
                        LDTIME[sa[0]][sa[3]] = cltime
                        _dins = True
                    if _dins:
                        _dsql = _dsql + '("{0}","{1}","{2}","{3}","{4}","{5}",NOW()), '.format(config._SOCKET['FLOOR'], sa[3], sa[19], sa[20], sa[1][:-3], int(time.mktime(cltime.timetuple())))
        _dbinsert(sql_)
        if _dins:
            _dbinsert(_dsql[:-2])

    elif 'CEILING_FLOOR_COUNT' in message:
        _dbinsert("INSERT INTO {2} (url, command, response, created) VALUES ('{0}', 'cfc', '{1}', NOW())".format(config._SOCKET['URL'], message, config.SOCKETS['CFC']['TABLEC']))

        if dbc.lastrowid:
            crawlid = dbc.lastrowid
        else:
            crawlid = '0'

        sj = message.replace('\\', '')[3:-2]
        obj = json.loads(sj)
        if "data" in obj["data"]:
            data = obj["data"]["data"]
        else:
            logger.info('do not follow seperated cfc item')
            return 0

        sql_ = "INSERT INTO {0} (floor_code, ceiling, floor, crawl_id, created) VALUES ".format(config.SOCKETS['CFC']['TABLE'])

        cnt_ = 0
        for sk, s in data.iteritems():
            if cnt_ > 0:
                sql_ += ','
            sql_ += "({0}, '{1}', '{2}', {3}, NOW())".format(sk, json.dumps(s['ceiling']), json.dumps(s['floor']), crawlid)
            cnt_ += 1
        _dbinsert(sql_)

    if not ontime():
        print "we are now in out of working time"
        logger.critical("we are now in out of working time")
        logger.info("close socket connection")
        ws.finish = 1
        ws.close()

def _wserror(ws, error):
    logger.error('socket error: %s', error)

def _wsclose(ws):
    if not ws.finish:
        logger.info('websocket server: %s', config._SOCKET['SERVER'])
        logger.info('websocket url: %s', config._SOCKET['URL'])
        logger.warning('socket closed')
        logger.info('create new socket connection')
        getcs()
        wsinit()
    else:
        if config.KEEPALIVE:
            ntime = datetime.datetime.now()
            ttime = datetime.datetime.now() + datetime.timedelta(days=1)
            stime = datetime.datetime.strptime(config.ACTIVE['START'], "%H:%M")
            stime = ttime.replace(hour=stime.time().hour, minute=stime.time().minute)
            if (stime > ntime):
                while not ontime():
                    ntime = datetime.datetime.now()
                    wtime = int((stime - ntime).total_seconds()) + 5
                    print "waiting for %s seconds..." % wtime
                    logger.warning("waiting for %s seconds...", wtime)
                    time.sleep(wtime)
            while onvacation():
                ntime = datetime.datetime.now()
                print "today is {0}. we are now on vacation".format(calendar.day_name[ntime.weekday()].lower())
                logger.warning("today is {0}. we are now on vacation".format(calendar.day_name[ntime.weekday()].lower()))
                ttime = datetime.datetime.now() + datetime.timedelta(days=1)
                stime = datetime.datetime.strptime(config.ACTIVE['START'], "%H:%M")
                stime = ttime.replace(hour=stime.time().hour, minute=stime.time().minute)
                wtime = int((stime - ntime).total_seconds()) + 5
                print "waiting for %s seconds..." % wtime
                logger.warning("waiting for %s seconds...", wtime)
                time.sleep(wtime)
            logger.info('create new socket connection')
            getcs(True)
            wsinit()
        else:
            print "byebye"
            logger.info('byebye')

def _wsopen(ws):
    logger.info('socket connected')
    def run(*args):
        for cmd in config._SOCKET['CMD']:
            if cmd == 'info':
                c = wscmd('info') % '{0:.0f}'.format(nowunix())
                ws.send(c)
                logger.log(SQ, c)
            else:
                c = wscmd(cmd)
                ws.send(c)
                logger.log(SQ, c)

    thread.start_new_thread(run, ())

def wsinit():
    logger.info('websocket server: %s', config._SOCKET['SERVER'])
    logger.info('websocket url: %s', config._SOCKET['URL'])
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        config._SOCKET['URL'],
        on_message = _wsmsg,
        on_error = _wserror,
        on_close = _wsclose
    )
    ws.on_open = _wsopen
    ws.finish = 0
    ws.run_forever()

def ontime():
    now = datetime.datetime.now()
    stime = datetime.datetime.strptime(config.ACTIVE['START'], "%H:%M")
    etime = datetime.datetime.strptime(config.ACTIVE['END'], "%H:%M")
    stime = now.replace(hour=stime.time().hour, minute=stime.time().minute, second=0, microsecond=0)
    etime = now.replace(hour=etime.time().hour, minute=etime.time().minute, second=0, microsecond=0)

    return (now >= stime and now <= etime)

def onvacation():
    return datetime.datetime.now().weekday() in config.DAYOFF

def strtodelta(_str):
    value, unit = _str.split()
    return datetime.datetime.now() - datetime.timedelta(**{unit: float(value)})

if __name__ == "__main__":
    print "script started"

    st = None
    if len(sys.argv) > 1:
        st = sys.argv[1]
    if not st:
        print 'socket agrument is missing. halt'
        sys.exit()
    stu = st.upper()
    if stu not in config.SOCKETS:
        print 'socket agrument does not exist. halt'
        sys.exit()

    config.LOG['handlers']['default']['filename'] %= st.lower()

    print "see %s for detail" % config.LOG['handlers']['default']['filename']
    for li, l in config.LOG['levels'].iteritems():
        logging.addLevelName(l, li)
    logging.config.dictConfig(config.LOG)

    while onvacation():
        ntime = datetime.datetime.now()
        print "today is {0}. we are now on vacation".format(calendar.day_name[ntime.weekday()].lower())
        logger.warning("today is {0}. we are now on vacation".format(calendar.day_name[ntime.weekday()].lower()))
        ttime = datetime.datetime.now() + datetime.timedelta(days=1)
        stime = datetime.datetime.strptime(config.ACTIVE['START'], "%H:%M")
        stime = ttime.replace(hour=stime.time().hour, minute=stime.time().minute)
        wtime = int((stime - ntime).total_seconds()) + 5
        print "waiting for %s seconds..." % wtime
        logger.warning("waiting for %s seconds...", wtime)
        time.sleep(wtime)

    if not ontime():
        print "we are now in out of working time"
        logger.warning("we are now in out of working time")

    ntime = datetime.datetime.now()
    stime = datetime.datetime.strptime(config.ACTIVE['START'], "%H:%M")
    stime = ntime.replace(hour=stime.time().hour, minute=stime.time().minute)
    etime = datetime.datetime.strptime(config.ACTIVE['END'], "%H:%M")
    etime = ntime.replace(hour=etime.time().hour, minute=etime.time().minute)
    if (stime > ntime):
        while not ontime():
            ntime = datetime.datetime.now()
            stime = datetime.datetime.strptime(config.ACTIVE['START'], "%H:%M")
            stime = ntime.replace(hour=stime.time().hour, minute=stime.time().minute)
            wtime = int((stime - ntime).total_seconds()) + 5
            print "waiting for %s seconds..." % wtime
            logger.warning("waiting for %s seconds...", wtime)
            time.sleep(wtime)
    elif (ntime > etime):
        if config.KEEPALIVE:
            ntime = datetime.datetime.now()
            ttime = datetime.datetime.now() + datetime.timedelta(days=1)
            stime = datetime.datetime.strptime(config.ACTIVE['START'], "%H:%M")
            stime = ttime.replace(hour=stime.time().hour, minute=stime.time().minute)
            if (stime > ntime):
                while not ontime():
                    ntime = datetime.datetime.now()
                    wtime = int((stime - ntime).total_seconds()) + 5
                    print "waiting for %s seconds..." % wtime
                    logger.warning("waiting for %s seconds...", wtime)
                    time.sleep(wtime)
        else:
            print "halt"
            logger.warning('halt')
            sys.exit()

    config._SOCKET = config.SOCKETS[stu]
    config._SOCKET['NAME'] = stu
    # open database
    _dbopen()
    if config.APIDATA:
        # memcached connection
        _memconnect(config.MEMCACHE['HOST'], config.MEMCACHE['PORT'], config.MEMCACHE['DEBUG'])
    # get a server to work with
    getcs()
    # initialize socket
    wsinit()