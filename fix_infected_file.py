#!/usr/bin/python3
import re, sys

# import detection regex & constants from constant.py file 
from config import *


if len(sys.argv) != 3:
    print("\nUsage:")
    print("    ./fix_infected_file.py <INFECTED_FILES_LIST> <FULL_DOMAIN_NAME>")
    print("")
    print("In some cases this virus replace the wp_host_url of your site with a bad one ! So this script need your full domain name (like 'https://example.com' ) to fix that\n")
    exit(1)

domain = sys.argv[2]

print("/!\ Be safe & make a backup before !")
k = input("Write 'yes' to continue: ")
if k != "yes":
    print("Ok bye !")
    exit(0)


## LOBBYDESIRES.COM VERSION PAYLOADS

# Small JS Payloads (html, index etc...)
regex = [[re.compile("""(<script[^<>]*['"]http[s]?:\/\/lobbydesires\.com\/location.js[^<>]*><\/script>)"""),""],

# PHP payload
[re.compile("""(<\?php \$c1 = [^?><]*lobbydesires.com[^>?<]*<\?php[^?><]*file_get_contents\(\$c1\)\)\); \?>)"""),""],

# Theme JS payload 1 
[re.compile("""(<script type=text\/javascript> Element\.prototype\.appendAfter[^><]*116,101,120,116,47,106,97,118,97,115,99,114,105,112,116[^><]*\[0\]\.appendChild\(elem\);}\)\(\);<\/script><\/head>)"""),'</head>'],

# Theme JS payload 2 
[re.compile("""(<head><script type=text\/javascript> Element\.prototype\.appendAfter[^><]*116,101,120,116,47,106,97,118,97,115,99,114,105,112,116[^><]*\[0\]\.appendChild\(elem\);}\)\(\);<\/script>)"""),"<head>"],

# Full JS payload
[re.compile("""(Element\.prototype\.appendAfter = function\(element\) {element\.parentNode\.insertBefore\(this, element\.nextSibling\);}, false;\(function\(\) { var elem = document\.createElement\(String\.fromCharCode\(115,99,114,105,112,116\)\); elem\.type = String\.fromCharCode\(116,101,120,116,47,106,97,118,97,115,99,114,105,112[^\n]*String\.fromCharCode\(104,101,97,100\)\)\[0\]\.appendChild\(elem\);}\)\(\);)"""),""],


## Payloads added in LETSMAKEPARTY3.GA VERSION 

# Domain replacement in includes
[re.compile("""https:\/\/letsmakeparty3.ga\/type\.js\?v=14ll"""),domain],

# PHP payload
[re.compile("""(<\?php function makemee\(\){[^}]*\$actual_link\);}\$lastRunLog.*\?>[\n]?<script[^<>]*['"]http[s]?:\/\/letsmakeparty3\.ga\/l.js[^<>]*><\/script>)"""),""],

# Small JS Payloads (html, index etc...)
[re.compile("""(<script[^<>]*['"]http[s]?:\/\/letsmakeparty3\.ga\/l.js[^<>]*><\/script>)"""),""],

# Full JS payload
[re.compile("""(%3C%3Fphp%20function%20makemee\(\)%7B%24n2%20%3D%20%22base64_decode%22%3B%24c1%20%3D%20chr\(104\)\.chr\(116\)\.chr\(116\)\.chr\(112\)\.chr\(115\)\.chr\(58\)\.chr\(47\)\.chr\(47\)\.chr\(108\)\.chr\(101\)\.chr[^<>]*letsmakeparty3\.ga%2Fl\.js%3Fq%3D1'%20type%3D'text%2Fjavascript'%3E%3C%2Fscript%3E)"""),""],
]

fixed = 0

with open (sys.argv[1], 'r+' ) as f_list:
    for infectedfile in f_list:
        infectedfile = infectedfile.rstrip('\n')
        if infectedfile != '':
            with open (infectedfile, 'r+' ) as f:
                content = f.read()
                for reg,rep in regex:
                    content = re.sub(reg, rep, content)
                f.seek(0)
                f.write(content)
                f.truncate()
                fixed += 1

print("\n"+c.GREEN+str(fixed)+c.ENDC+" files fixed :)")

