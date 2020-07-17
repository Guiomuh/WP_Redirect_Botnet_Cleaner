# WP Database creds
DB_HOST = 'localhost'
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''

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



###############################
## Infection detection regex ##
###############################

# domain name
regex = "(lobbydesires\.com)"
regex += "|(stivenfernando\.com)"
regex += "|(letsmakeparty3\.ga)"
regex += "|(developfirstline\.com)"


## JS
# (general) "text/javascript" string offuscated 
regex += "|(116,101,120,116,47,106,97,118,97,115,99,114,105,112,116)"

regex += "|(function makemee)"

# "lobbydesires" string offuscated
regex += "|(108,111,98,98,121,100,101,115,105,114,101,115)"


## PHP
# (general) "base64_dec" string offuscated in PHP
regex += "|(chr\(98\)\.chr\(97\)\.chr\(115\)\.chr\(101\)\.chr\(54\)\.chr\(52\)\.chr\(95\)\.chr\(100\)\.chr\(101\)\.chr\(99\))"

# "https://letsmakeparty" string offuscated in PHP
regex += "|(chr\(104\)\.chr\(116\)\.chr\(116\)\.chr\(112\)\.chr\(115\)\.chr\(58\)\.chr\(47\)\.chr\(47\)\.chr\(108\)\.chr\(101\)\.chr\(116\)\.chr\(115\)\.chr\(109\)\.chr\(97\)\.chr\(107\)\.chr\(101\)\.chr\(112\)\.chr\(97\)\.chr\(114\)\.chr\(116\))"
