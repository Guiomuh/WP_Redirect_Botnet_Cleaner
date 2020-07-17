#!/usr/bin/python3
# requirements:
# python -m pip install tqdm

import re, sys, codecs
from os.path import isfile
from pathlib import Path
from tqdm import tqdm

# import detection regex & constants from constant.py file 
from config import *


if len(sys.argv) != 2:
    print("Usage:")
    print("    ./detect_infected_files.py <PATH>")
    exit(1)

p = sys.argv[1]

print("\n[*] Search for JS, HTML & PHP files..")
myfiles = list(Path(p).rglob("*.js")) + list(Path(p).rglob("*.ph*")) + list(Path(p).rglob("*.htm*"))
print("\n[*] "+c.GREEN+str(len(myfiles))+c.ENDC+" files found")

INFECTED = []


print("\n[*] Search inside files for infection..")
for input_file in tqdm(myfiles):
    try:
        with codecs.open(str(input_file), "r", encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if bool(re.search(regex, content, flags = re.M)):
                INFECTED.append(str(input_file))

    except OSError as e:
        # Handle File Not Found (wordpress temp files)
        #print(e)
        continue


print("\n[*] "+c.FAIL+str(len(INFECTED))+c.ENDC+" infected files found")

# Write the infected files list
if len(INFECTED) != 0:
    with open('infected_list.txt', 'w') as f:
        for i in INFECTED:
            f.write("%s\n" % i)
    print("\n[*] infected file list written to: "+c.BOLD+"infected_list.txt"+c.ENDC)



print("\n[*] Search for temp/log files used by the virus..")
relative_traces_files = RTF
absolute_traces_files = ATF
L = []

for rtf in relative_traces_files:
    absolute_traces_files += list(Path(p).rglob(rtf))
            
for atf in absolute_traces_files:
    if isfile(str(atf)):
        L.append(str(atf))



# Print the tmp/log files search result 
if (len(L) != 0):
    print("\n[*] "+c.FAIL+str(len(L))+c.ENDC+" possible tmp/log files used by the virus have been found:"+c.WARNING)
    for l in L:
        print("    - {}".format(str(l)))
    print(c.FAIL+"\n    /!\\"+c.ENDC+" Theses tmp/log files aren't deleted by the fix script\n        check them and delete them manually if needed\n")
else:
    print("\n[*] "+c.GREEN+"0"+c.ENDC+" tmp/log files used by the virus have been found")
