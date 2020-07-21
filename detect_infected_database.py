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
INFECTED_POSTS = []

try:
    # connect to MySQL DB
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cur = conn.cursor()
except Error as e:
    print("MySQL connection error: ",e)
    exit(1)


try:
    # Search POSTS table like the virus 
    cur.execute("SELECT TABLE_SCHEMA,TABLE_NAME FROM information_schema.TABLES WHERE `TABLE_NAME` LIKE '%post%'")
    rows = cur.fetchall()
    #print(rows)
    for row in rows:
        TABLE_SCHEMA = row[0]
        TABLE_NAME = row[1]

        # view table infos 
        #cur.execute("DESCRIBE " + TABLE_SCHEMA + "." + TABLE_NAME)
        #print(cur.fetchall())

        # Check the presence of the needed columns
        cur.execute("SHOW COLUMNS FROM "+TABLE_SCHEMA+"."+TABLE_NAME+" LIKE 'post_content'");
        c1_found = (cur.fetchall()) != []
        cur.execute("SHOW COLUMNS FROM "+TABLE_SCHEMA+"."+TABLE_NAME+" LIKE 'post_title'");
        c2_found = (cur.fetchall()) != []
        if (c1_found and c2_found):

            # Check if the post_content is infected
            cur.execute("SELECT post_title, post_content FROM "+TABLE_SCHEMA+"."+TABLE_NAME)
            posts = cur.fetchall()
            for post in posts:
                if bool(re.search(regex, post[1], flags = re.M)):
                    INFECTED_POSTS.append(post[0])

    # Find wp_option table if renamed
    cur.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE `TABLE_NAME` LIKE '%wp_options%' LIMIT 1")
    opt_table = cur.fetchone()[0]

    # Get the site_url and host_url values
    cur.execute("SELECT option_value FROM "+opt_table+" WHERE option_name='siteurl'")
    site_url = cur.fetchone()[0]
    cur.execute("SELECT option_value FROM "+opt_table+" WHERE option_name='home'")
    home_url = cur.fetchone()[0]


except Error as e:
    print("MySQL Error : ",e)
    exit(1)

finally:
    if (conn.is_connected()):
        cur.close()
        conn.close()


# Print infected posts names
print("\n[*] {} infected articles".format(len(INFECTED_POSTS)))
for i in INFECTED_POSTS:
    print("  - {}".format(i))

# Print alert if site_url or home_url changed:
if (site_url!=domain):
    print("\n/!\\ changements detected in site_url database values:")
    print("-> '"+c.FAIL+site_url+c.ENDC+"' instead of '"+domain+"'")
else:
    print("\n[*] site_url: "+c.GREEN+"OK"+c.ENDC+" ("+site_url+")")

if (home_url!=domain):
    print("\n/!\\ changements detected in home_url database values:")
    print("-> '"+c.FAIL+home_url+c.ENDC+"' instead of '"+domain+"'")
else:
    print("\n[*] home_url: "+c.GREEN+"OK"+c.ENDC+" ("+home_url+")")

if (home_url!=domain or site_url!=domain):
    print("\nTheses values will be replaced in the './fix_infected_database.py'")

