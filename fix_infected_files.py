#!/usr/bin/python3
import re, sys, codecs
from tqdm import tqdm

# import detection regex & constants from constant.py file 
from config import *

if len(sys.argv) != 2:
    print("\nUsage:")
    print("    ./fix_infected_files.py <INFECTED_FILES_LIST>")
    exit(1)


print("/!\ Be safe & make a backup before !")
k = input("Write 'yes' to continue: ")
if k != "yes":
    print("Ok bye !")
    exit(0)


fixregex = []

## General Small JS Payloads (html, index etc...)
for URL in SIG_CLEAR:
    fixregex.append([re.compile("""(<script[^<>]*"""+re.escape(URL)+"""[^<>]*><\/script>)"""),""])


## General PHP Payload
fixregex.append([re.compile("""(<\?php \$c = chr\(98\)\.chr\(97\)\.chr\(115\)\.chr\(101\)\.chr\(54\)\.chr\(52\)\.chr\(95\)\.chr\(100\)\.chr\(101\)[^<>]* \?>)"""),""])

# General Theme JS payload 1
fixregex.append([re.compile("""(<script type=text\/javascript> Element\.prototype\.appendAfter[^><]*116,101,120,116,47,106,97,118,97,115,99,114,105,112,116[^><]*\[0\]\.appendChild\(elem\);}\)\(\);<\/script><\/head>)"""),'</head>'])

# General Theme JS payload 2
fixregex.append([re.compile("""(<head><script type=text\/javascript> Element\.prototype\.appendAfter[^><]*116,101,120,116,47,106,97,118,97,115,99,114,105,112,116[^><]*\[0\]\.appendChild\(elem\);}\)\(\);<\/script>)"""),"<head>"])

# PHP payload
for URL in SIG_CLEAR:
    fixregex.append([re.compile("""(<\?php \$c1 = [^?><]*"""+re.escape(URL)+"""[^>?<]*<\?php[^?><]*file_get_contents\(\$c1\)\)\); \?>)"""),""])


# Full JS payload
fixregex.append([re.compile("""(Element\.prototype\.appendAfter = function\(element\) {element\.parentNode\.insertBefore\(this, element\.nextSibling\);}, false;\(function\(\) { var elem = document\.createElement\(String\.fromCharCode\(115,99,114,105,112,116\)\); elem\.type = String\.fromCharCode\(116,101,120,116,47,106,97,118,97,115,99,114,105,112[^\n]*String\.fromCharCode\(104,101,97,100\)\)\[0\]\.appendChild\(elem\);}\)\(\);)"""),""])


## Payloads added in LETSMAKEPARTY3.GA VERSION 

# PHP payload
fixregex.append([re.compile("""(<\?php function makemee\(\){[^}]*\$actual_link\);}\$lastRunLog[^}]*}} else[^}]*}\?><\?php[^}]*} \?>)"""),""])

# Full JS payload
fixregex.append([re.compile("""(%3C%3Fphp%20function%20makemee\(\)%7B%24n2%20%3D%20%22base64_decode%22%3B%24c1%20%3D%20chr\(104\)\.chr\(116\)\.chr\(116\)\.chr\(112\)\.chr\(115\)\.chr\(58\)\.chr\(47\)\.chr\(47\)\.chr\(108\)\.chr\(101\)\.chr[^<>]*letsmakeparty3\.ga%2Fl\.js%3Fq%3D1'%20type%3D'text%2Fjavascript'%3E%3C%2Fscript%3E)"""),""])

# ws.stivenfernando.com
fixregex.append([re.compile("""(var gfhfghfhfgj[^<>{}]*47,47,119,115,46,115,116,105,118,101,110[^<>{}]*[^<>{}]*if[^<>{}]*{[^<>{}]*} else {[^<>{}]*})"""),""])

for URL in SIG_CLEAR:
    fixregex.append([re.compile("""(<tr><td class="aws"><a href="[^"<>]*"""+re.escape(URL)+"""[^?\\n%]*%<\/td><\/tr>)"""),""])


fixed = 0

# read file list
infectedfiles = []
with open (sys.argv[1], 'r+' ) as f_list:
    for f in f_list:
        f = f.rstrip('\n')
        if f != '':
            infectedfiles.append(f)



print("\n[*] Fix infected files..")
for infectedfile in tqdm(infectedfiles):
    try:
        with codecs.open(infectedfile, "r+", encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for reg,rep in fixregex:
                content = re.sub(reg, rep, content)
            f.seek(0)
            f.write(content)
            f.truncate()
            fixed += 1
    except OSError as e:
        # Handle File Not Found (wordpress temp files)
        print(e)
        continue


print("\n[*] Search if somes files are still infected..")
INFECTED = []
for input_file in tqdm(infectedfiles):
    try:
        with codecs.open(str(input_file), "r", encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if bool(re.search(regex, content, flags = re.M)):
                INFECTED.append(str(input_file))

    except OSError as e:
        # Handle File Not Found (wordpress temp files)
        continue

# Write the still infected files list
if len(INFECTED) != 0:
    with open('still_infected_list.txt', 'w') as f:
        for i in INFECTED:
            f.write("%s\n" % i)
    print("\n[*] still infected file list written to: "+c.BOLD+"still_infected_list.txt"+c.ENDC)

print("\n[*] "+c.GREEN+str(fixed-len(INFECTED))+c.ENDC+" files fixed :)")
print("\n[*] "+c.FAIL+str(len(INFECTED))+c.ENDC+" files  still infected")
