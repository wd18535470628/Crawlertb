#coding=utf-8
import MySQLdb
import time

class Mysql:
    # 数据库初始化
    def __init__(self):
        try:
            self.db = MySQLdb.connect('localhost', 'root', 'root', 'ceshi', 3306)
            self.cur = self.db.cursor()
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "连接数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    def dateFormat(self,msec):
        date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msec/1000))
        return date
    def insertData(self, cache_table,table, my_dict,kind_id,court_id,paimai_times):
	dataTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            self.db.set_character_set('utf8')
            for col in my_dict.keys():
                if type(col) == unicode:
                    col = col.decode("utf-8").encode("utf-8")
                    if col == 'end':
                        my_dict[col] = self.dateFormat(my_dict[col])
                    if col == 'start':
                        my_dict[col] = self.dateFormat(my_dict[col])
                    if col == 'itemUrl':
                        my_dict[col] = my_dict[col][2:]
            sqlCheck = 'SELECT count(*) FROM '+ cache_table +' where auction_id='+ str(my_dict['id'])
            self.cur.execute(sqlCheck)
            print str(my_dict['id'])
            print self.cur._rows[0][0]
            print sqlCheck
            if self.cur._rows[0][0] == 0:
                #缓存表
                sqlAche = "INSERT INTO "+ cache_table +" (auction_id) value ("+ str(my_dict['id'])  +")"
                sqlInfo = "insert into %s (%s) VALUES (%s)" % (table, "auction_id,status,current_price,start,end,kind_id,court_id,paimai_times,start_price,title,corporate_agent,phone,data_time,fare_increase,cash_deposit,access_price,biding_cycle,delay_cyle,enrollment,set_reminders,onlookers,bidding_rules,bidding_record,payment_advance,url,notice_Time,buyer_Name,buyer_AliasName,main_status,loan,payfirst,delaycnt,position",
                                                               str(my_dict['id'])+",'"+my_dict['status'].decode('utf-8').encode('utf-8')+"',"
                                                               + str(my_dict['currentPrice'])+",'"+ my_dict['start']+"','"+my_dict['end']+"',"
                                                               +str(kind_id)+","+str(court_id)+","+str(paimai_times)+",'"
                                                               +str(my_dict['start_price'])+"','"+str(my_dict['title'].encode('utf8'))
                                                               +"','"+str(my_dict['corporate_agent'].encode('utf8'))+"','"
                                                               +str(my_dict['phone'].encode('utf8'))+"','"+str(dataTime)+"','"
                                                               +str(my_dict['fare_increase'])+"','"+str(my_dict['cash_deposit'])+"','"
                                                               +str(my_dict['access_price'])+"','"+str(my_dict['biding_cycle'].encode('utf8'))+"','"
                                                               +str(my_dict['delay_cyle'].encode('utf8'))+"','"+str(my_dict['enrollment'])+"','"
                                                               +str(my_dict['set_reminders'])+"','"+str(my_dict['onlookers'])+"','"
                                                               +str(my_dict['bidding_rules'].encode('utf8'))+"','"
                                                               +str(my_dict['bidding_record'])+"','"+str(my_dict['payment_advance'])+"','"
                                                               +str(my_dict['url'])+"','"+my_dict['noticeTime']+"','"
                                                               +str(my_dict['buyerName'].decode('utf-8').encode('utf-8'))+"','"
                                                               +str(my_dict['buyerAliasName'].decode('utf-8').encode('utf-8'))+"','1','"
                                                               +str(my_dict['loan'].decode('utf-8').encode('utf-8'))+"','"
                                                               +str(my_dict['payfirst'].decode('utf-8').encode('utf-8'))+"','"
                                                               +str(my_dict['delaycnt'].decode('utf-8').encode('utf-8'))+"','"
                                                               +str(my_dict['position'].decode('utf-8').encode('utf-8'))+"'")
                #sqlInfo = "insert into %s (%s) VALUES (%s)" % (table, "auction_id,status,current_price,start,end,kind_id,court_id,paimai_times,start_price,title,corporate_agent,phone,data_time,url,notice_Time,buyer_Name,buyer_AliasName",str(my_dict['id'])+",'"+my_dict['status'].decode('utf-8').encode('utf-8')+"',"+ str(my_dict['currentPrice'])+",'"+ my_dict['start']+"','"+my_dict['end']+"',"+str(kind_id)+","+str(court_id)+","+str(paimai_times)+",'"+str(my_dict['start_price'])+"','"+str(my_dict['title'].encode('utf8'))+"','"+str(my_dict['corporate_agent'].encode('utf8'))+"','"+str(my_dict['phone'].encode('utf8'))+"','"+str(dataTime)+"','"+str(my_dict['url'])+"','"+my_dict['noticeTime']+"','"+str(my_dict['buyerName'].decode('utf-8').encode('utf-8'))+"','"+str(my_dict['buyerAliasName'].decode('utf-8').encode('utf-8'))+"'")
                print sqlInfo
                try:
                    self.cur.execute(sqlAche)
                    result = self.cur.execute(sqlInfo)
                    insert_id = self.db.insert_id()
                    self.db.commit()
                    # 判断是否执行成功
                    if result:
                        return insert_id
                    else:
                        return 0
                except MySQLdb.Error, e:
                    # 发生错误时回滚
                    self.db.rollback()
                    # 主键唯一，无法插入
                    if "key 'PRIMARY'" in e.args[1]:
                        print self.getCurrentTime(), "数据已存在，未插入数据"
                    else:
                        print self.getCurrentTime(), "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
            else:
                sqlUpdate = 'update %s set '%(table)
                sqlUpdate = sqlUpdate + 'status="' + str(my_dict['status']) + '",current_price='+str(my_dict['currentPrice'])+',start="'+ my_dict['start'] + '",end="'+my_dict['end']+'",kind_id='+ str(kind_id)+',court_id='+str(court_id)+',start_price="'+str(my_dict['start_price'])+'",title="'+str(my_dict['title'].encode('utf8'))+'",corporate_agent="'+str(my_dict['corporate_agent'].encode('utf8'))+'",phone="'+str(my_dict['phone'].encode('utf8'))+'",data_time="'+str(dataTime)+'",fare_increase="'+str(my_dict['fare_increase'])+'",cash_deposit="'+str(my_dict['cash_deposit'])+'",access_price="'+str(my_dict['access_price'])+'",biding_cycle="'+str(my_dict['biding_cycle'].encode('utf8'))+'",delay_cyle="'+str(my_dict['delay_cyle'].encode('utf8'))+'",enrollment="'+str(my_dict['enrollment'])+'",set_reminders="'+str(my_dict['set_reminders'])+'",onlookers="'+str(my_dict['onlookers'])+'",bidding_rules="'+str(my_dict['bidding_rules'].encode('utf8'))+'",bidding_record="'+str(my_dict['bidding_record'])+'",payment_advance="'+str(my_dict['payment_advance'])+'",url="'+str(my_dict['url'])+'",notice_Time="'+my_dict['noticeTime']+'",buyer_Name="'+str(my_dict['buyerName'])+'",buyer_AliasName="'+str(my_dict['buyerAliasName'])+'",main_status="2'+'",loan="'+str(my_dict['loan'])+''+'",payfirst="'+str(my_dict['payfirst'])+''+'",delaycnt="'+str(my_dict['delaycnt'])+''+'",position="'+str(my_dict['position'])+'" where auction_id='+str(my_dict['id'])
                #sqlUpdate = sqlUpdate + 'status="' + str(my_dict['status']) + '",current_price='+str(my_dict['currentPrice'])+',start="'+ my_dict['start'] + '",end="'+my_dict['end']+'",kind_id='+ str(kind_id)+',court_id='+str(court_id)+',start_price="'+str(my_dict['start_price'])+'",title="'+str(my_dict['title'].encode('utf8'))+'",corporate_agent="'+str(my_dict['corporate_agent'].encode('utf8'))+'",phone="'+str(my_dict['phone'].encode('utf8'))+'",data_time="'+str(dataTime)+'",url="'+str(my_dict['url'])+'",notice_Time="'+my_dict['noticeTime']+'",buyer_Name="'+str(my_dict['buyerName'])+'",buyer_AliasName="'+str(my_dict['buyerAliasName'])+'" where auction_id='+str(my_dict['id'])
                print sqlUpdate
                result = self.cur.execute(sqlUpdate)
                insert_id = self.db.insert_id()
                self.db.commit()
                # 判断是否执行成功
                if result:
                    return insert_id
                else:
                    return 0
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getCourtList(self):
        try:
            self.db.set_character_set('utf8')
            sqlGetData = "select id,user_id,court_name,city,province,table_name,cache_table_name from auction_court"
            #sqlGetData = "select id,user_id,court_name,city,province,table_name,cache_table_name from auction_court where table_name='auction_info_guangxi'"
            #sqlGetData = "select id,user_id,court_name,city,province,table_name,cache_table_name from auction_court where id>='1196' and id<='3304'"
            self.cur.execute(sqlGetData)
            return list(self.cur._rows)
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def insertAuctionCourt(self,sql):
        try:
            self.db.set_character_set('utf8')
            result = self.cur.execute(sql)
            insert_id = self.db.insert_id()
            self.db.commit()
            # 判断是否执行成功
            if result:
                return insert_id
            else:
                return 0
        except MySQLdb.Error, e:
            # 发生错误时回滚
            self.db.rollback()
            # 主键唯一，无法插入
            if "key 'PRIMARY'" in e.args[1]:
                print sql
                print self.getCurrentTime(), "数据已存在，未插入数据"
            else:
                print self.getCurrentTime(), "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
    def getKindList(self):
        try:
            self.db.set_character_set('utf8')
            sqlGetData = "select id,kind_id from tb_auction_kind "
            self.cur.execute(sqlGetData)
            return list(self.cur._rows)
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getStatusList(self):
        try:
            self.db.set_character_set('utf8')
            sqlGetData = "select id,auction_status from auction_status"
            self.cur.execute(sqlGetData)
            return list(self.cur._rows)
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    
    def getSendMailData(self,table,my_dict):
        try:
            self.db.set_character_set('utf8')
            sqlGetData = 'SELECT count(*) FROM '+ table +' where auction_id='+ str(my_dict['id'])
            self.cur.execute(sqlGetData)
            if self.cur._rows[0][0] == 0:
                return 0
            else:
                return 1
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    
    
