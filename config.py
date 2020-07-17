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



##########################################
## JS Payloads links (without get args) ##
##########################################

JS_Payload_links = [ "https://lobbydesires.com/location.js",
                     "https://letsmakeparty3.ga/type.js",
                     "https://letsmakeparty3.ga/l.js",
                     "https://ws.stivenfernando.com/stm.js"]


###################
## Signature STR ##
###################

SIG = [ "lobbydesires.com",
        "letsmakeparty3.ga",
        "stivenfernando.com",
        "developfirstline" ]

## Auto generate PHP/JS offuscated payloads from signature str

p_JS = ""
p_PHP = ""

for sig in SIG:
    p_JS += "|("
    p_PHP += "|("

    for char in sig:
        p_JS += str(ord(char)) + ","
        p_PHP += "chr\\(" + str(ord(char)) + "\\)\\."

    p_JS = p_JS[:-2] + ")"
    p_PHP = p_PHP[:-2] + ")"


###############################
## Infection detection regex ##
###############################

# domain name
regex = "(lobbydesires\.com)"
regex += "|(stivenfernando\.com)"
regex += "|(letsmakeparty3\.ga)"
regex += "|(developfirstline\.com)"


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
