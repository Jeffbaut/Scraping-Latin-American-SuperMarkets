
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import datetime 
from time  import sleep
import pymysql
import json
import time

my_db_name = "compare_price"

def get_category(supermarket):
    my_db = pymysql.connect(host="localhost",user="root",password="",db=my_db_name)
    tables = my_db.cursor() 
    tables.execute("SELECT id, url FROM tbl_category WHERE supermarket = " + supermarket) 
    eanCodes = tables.fetchall()
    return eanCodes

def insert_data(my_table_name,data_col,data_type,data):
    my_db = pymysql.connect(host="localhost",user="root",password="",db=my_db_name)
    with my_db:
        my_cursor  = my_db.cursor()
        sql = "INSERT INTO " + my_table_name + " (" + data_col + ") VALUES (" + data_type + ")"
        my_cursor.executemany(sql, data)
    my_db.commit()    

    print("OK")
