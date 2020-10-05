import pymssql 
from static.functions.sendMail import *
import asyncio
import threading
from static.functions.logger import logger
from static import settings

def Sync_sendMail(email,title,body):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        sendmail = send_mail_async([email],title,body,textType="plain")
        loop.run_until_complete(sendmail)
        # loop.close()
    except Exception as ex:
	    logger.error('Sync_sendMail - ERROR: {}'.format(ex))

def ReportLogByEmail(title,body):
    try:
        t = threading.Thread(target=Sync_sendMail,args=('dtson.vt@gmail.com',title,body,))
        t.start()
    except Exception as inst:
        print('ValueError: ',str(inst))

def ExucteSQLasDataTable(nameStore,**params):
    query = ""
    try:
        conn = pymssql.connect(server=settings.serverName, user=settings.AccountSQL, password=settings.Password, database=settings.DatabaseName)  
        cursor = conn.cursor()  
        # genera string query from list paramerters
        for key, value in params.items():
            if(query==""):
                query= "exec dbo.{} @{}=N'{}'".format(nameStore,key,value)
            else:
                query= "{} , @{}=N'{}'".format(query,key,value)
        if(query==""):
            query= "exec dbo.{}".format(nameStore)
        cursor.execute(query)  
         
        lst_Result = []
        columns = [column[0] for column in cursor.description]
        
        for row in cursor.fetchall():
            lst_Result.append(dict(zip(columns, row)))
        dataReturn = {"Table1":lst_Result}
        conn.commit()
        return  "",dataReturn
    except Exception as ex:
        logger.error("ERROR-API-FLASK","{} \r\n====================================\r\nERROR\r\n- {}".format(query,ex))
        Sync_sendMail("ERROR-API-FLASK","{} \r\n====================================\r\nERROR\r\n- {}".format(query,ex))
        return "ExucteSQLasDataTable:{}".format(str(ex)), {"Table1":''}

def ExucteSQLasDataSet(nameStore,**params):
    query = ""
    try:
        conn = pymssql.connect(server=settings.serverName, user=settings.AccountSQL, password=settings.Password, database=settings.DatabaseName)  
        cursor = conn.cursor()  
        for key, value in params.items():
            if(query==""):
                query= "exec dbo.{} @{}=N'{}'".format(nameStore,key,value)
            else:
                query= "{} , @{}=N'{}'".format(query,key,value)
        if(query==""):
            query= "exec dbo.{}".format(nameStore)

        cursor.execute(query)  

        lst_Result = []
        columns = [column[0] for column in cursor.description]
        
        for row in cursor.fetchall():
            lst_Result.append(dict(zip(columns, row)))
        dataReturn = {"Table1":lst_Result}

        tableName = ""
        i = 1
        while (cursor.nextset()):
            lst_Result = []
            i = i + 1
            tableName ="Table{}".format(i)
            for row in cursor.fetchall():
                lst_Result.append(dict(zip(columns, row)))
            dataReturn[tableName] = lst_Result

        return dataReturn
    except Exception as ex:
        logger.error("ERROR-API-FLASK","{} \r\n====================================\r\nERROR\r\n- {}".format(query,ex))
        Sync_sendMail("ERROR-API-FLASK","{} \r\n====================================\r\nERROR\r\n- {}".format(query,ex))
        return {"Table1":''}

