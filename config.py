import re

# WP Database creds
DB_HOST = 'localhost'
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''

# In some cases this virus replace the host_url and site_url of your site in the database 
# So we need your full domain (ex: "https://www.yourdomain.com") to check & fix the infection
domain = ''


# Add Colors
class c:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



#######################################
##    Identified tmp & log files     ##
#######################################

# Relative path traces files
RTF = [ "e.log",
        "mn",
        "rebut.log",
        # letsmakeparty3.ga
        "sdfsd234",
        # train.developfirstline.com 
        "htht"]

# Absolute path traces files
ATF = ["/tmp/mn"]



###################
## Signature STR ##
###################

SIG_CLEAR = [ "lobbydesires.com",
              "letsmakeparty3.ga",
              "stivenfernando.com",
              "developfirstline.com" ]

## Auto generate PHP/JS offuscated payloads from signature str

SIG_PHP = []
SIG_JS = []


for sig in SIG_CLEAR:
    p_JS = ""
    p_PHP = ""
    for char in sig:
        p_JS += str(ord(char)) + ","
        p_PHP += "chr(" + str(ord(char)) + ")."
    SIG_JS.append(p_JS[:-1])
    SIG_PHP.append(p_PHP[:-1])

## Auto generate REGEX

p_CLEAR = ""
p_JS = ""
p_PHP = ""

for sig in SIG_CLEAR: 
    p_CLEAR += "|(" + re.escape(sig) + ")"
for sig in SIG_JS: 
    p_JS += "|(" + re.escape(sig) + ")"
for sig in SIG_PHP: 
    p_PHP += "|(" + re.escape(sig) + ")"



###############################
## Infection detection regex ##
###############################

regex = ""

# domain name
regex += p_CLEAR[1:]


########
## JS ##
########

# (general) "text/javascript" string offuscated 
regex += "|(116,101,120,116,47,106,97,118,97,115,99,114,105,112,116)"

# (autogen from sig)
regex += p_JS

# letsmakeparty3 special function name
regex += "|(function makemee)"


#########
## PHP ##
#########

# (general) "base64_dec" string offuscated in PHP
regex += "|(chr\(98\)\.chr\(97\)\.chr\(115\)\.chr\(101\)\.chr\(54\)\.chr\(52\)\.chr\(95\)\.chr\(100\)\.chr\(101\)\.chr\(99\))"

# (autogen from sig)
regex += p_PHP
