#!/usr/bin/python3
# requirements:
# python -m pip install mysql-connector-python

import re, sys, mysql.connector
from mysql.connector import Error

# import detection regex & constants from constant.py file
from config import *

error = False

if (DB_NAME == '' or DB_HOST == '' or DB_USER == '' or DB_PASSWORD == ''):
    print("\n /!\ NO DATABASE CREDS \n Open the 'config.py' file and please provide the WordPress database credentials\n You can find them in the wp-config.php file\n")
    error = True
if (domain == ''):
    print("\n /!\ NO Domain given in the configuration\n Open 'config.py' and please provide the WordPress domain (like 'https://www.yourdomain.com')\n In some cases this virus replace in the database the host_url and site_url of your site\n")
    error = True
if error:
    exit(1)

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
    
    # Find wp_option table if renamed
    cur.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE `TABLE_NAME` LIKE '%wp_options%' LIMIT 1")
    opt_table = cur.fetchone()[0]

    # Get the site_url and host_url values
    cur.execute("SELECT option_value FROM "+opt_table+" WHERE option_name='siteurl'")
    site_url = cur.fetchone()[0]
    cur.execute("SELECT option_value FROM "+opt_table+" WHERE option_name='home'")
    home_url = cur.fetchone()[0]

    # Fix site_url & home_url if infected
    if (home_url!=domain or site_url!=domain):
        cur.execute("UPDATE "+opt_table+" SET option_value='"+domain+"' WHERE option_name='home' OR option_name='siteurl'")
        print("\n> Infected home_url and site_url replaced with: "+c.GREEN+domain+c.ENDC)

except Error as e:
    print("MySQL Error : ",e)
    sys.exit(1)

finally:
    if (conn.is_connected()):
        cur.close()
        conn.close()

print( "\n> {} cleaned articles".format(CLEANED_POSTS))

