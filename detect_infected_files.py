#!/usr/bin/python3
# requirements:
# python -m pip install tqdm

import re, sys, codecs
from os.path import isfile
from pathlib import Path
from tqdm import tqdm

class c:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# REGEX to detect infection
regex = """(lobbydesires\.com)|(String\.fromCharCode\(104,116,116,112,115,58,47,47,108,111,98,98,121,100,101,115,105,114,101,115,46,99,111,109,47,108,111,99,97,116,105,111,110,46,106,115,63,115,61,49\))|(107,46,100,101,118,101,108,111)|(108,111,98,98,121,100,101,115,105,114,101,115)|(116,101,120,116,47,106,97,118,97,115,99,114,105,112,116)|(function makemee)|(chr\(104\)\.chr\(116\)\.chr\(116\)\.chr\(112\)\.chr\(115\)\.chr\(58\)\.chr\(47\)\.chr\(47\)\.chr\(108\)\.chr\(101\)\.chr\(116\)\.chr\(115\)\.chr\(109\)\.chr\(97\)\.chr\(107\)\.chr\(101\)\.chr\(112\)\.chr\(97\)\.chr\(114\)\.chr\(116\))|(letsmakeparty3.ga)|(104,116,116,112,115,58,47,47,108,101,116,115,109,97,107,101,112,97,114,116,121,51,46,103,97,47,108,46,106,115,63,100,61,49)"""


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
    print("\n[*] infected file list written to: infected_list.txt")



print("\n[*] Search for temp/log files used by the virus")
relative_traces_files = ["e.log","mn","rebut.log"]
absolute_traces_files = ["/tmp/mn"]
L = []

for rtf in relative_traces_files:
    absolute_traces_files += list(Path(p).rglob(rtf))
            
for atf in absolute_traces_files:
    if isfile(str(atf)):
        L.append(str(atf))



# Print the tmp/log files search result 
if (len(L) != 0):
    print("\n[*] "+c.WARNING+str(len(L))+c.ENDC+" possible tmp/log files used by the virus have been found:")
    for l in L:
        print("  - {}".format(str(l)))
else:
    print("\n[*] "+c.GREEN+str(len(L))+c.ENDC+" tmp/log files used by the virus have been found:")
