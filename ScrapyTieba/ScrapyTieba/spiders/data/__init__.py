# coding=utf-8
import sys
import MySQLdb

sys.path.append('D:/Work/PythonProject/ScrapyLearn/ScrapyTieba/ScrapyTieba')
from spiders.secret.a import DATABASE_USER_PASSWORD

# Open database
db = MySQLdb.connect(
    host="localhost",
    user="sora",
    passwd=DATABASE_USER_PASSWORD,
    db="sorashiro",
    charset='utf8',
)


