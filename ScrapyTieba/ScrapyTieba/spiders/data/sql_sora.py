# coding=utf-8
# filename: sql_sora.py

import sys

import MySQLdb

sys.path.append('D:/Work/PythonProject/ScrapyLearn/ScrapyTieba/ScrapyTieba')
from spiders.data import db

class SqlSora():

    def __init__(self, table_name):
        self.table_name = table_name

    def insert_value(self, item):
        cursor = db.cursor()

        sql = "INSERT INTO %s" \
              "(UNIVERSITY, TITLE, HREF, PROVINCE, AUTHOR, DATE) \
               VALUES ('%s', '%s', '%s', '%s', '%s' ,'%s')" % \
              (self.table_name, item['university'], item['title'],
               item['href'], item['province'], item['author'], item['date'])
        try:
            cursor.execute(sql)
            db.commit()
            print 'item inserted: ' + item
        except MySQLdb.Warning, w:
            sql_warn = "Warning:%s" % str(w)
            print sql_warn
            db.rollback()
        except MySQLdb.Error, e:
            sql_error = "Error:%s" % str(e)
            print sql_error
            db.rollback()

    def close_db(self):
        # Close database
        db.close()

# Example
# test = SqlSora('ask_table')
# my={
#     'university': u'广东工业大学',
#     'title': u'高考722分，能不能来贵校学点东西',
#     'href': u'https://tieba.baidu.com/p/12345468',
#     'province': u'江苏省',
#     'author': u'Sora',
#     'date': u'2015-06-13 12:42',
# }
# test.insert_value(my)
