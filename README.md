# WordPress Redirect Botnet Cleaner 
(letsmakeparty3.ga, lobbydesires.com)

## Intro 

Recently I detected some waves of WordPress infections<br>
Based on XSS Stored vulnerabilities in various themes & plugins

This botnet use the following domain names:
- letsmakeparty3.ga
- lobbydesires.com
- train.developfirstline.com
- ws.stivenfernando.com

This malware is very invasive it can infect all js, php, html files and even the database of your WordPress.

After some work I decided to make these scripts to easily detect & patch infected WordPress.

You can find the PART1 of my work on the "lobbydesires.com" version [HERE](https://medium.com/@guillaume.muh/lobbydesires-botnet-927bbc139457)<br>
The PART2 on the more complex version "letsmakeparty3.ga" is coming soon.. 


## Requirements
To use these scripts you need to install `mysql-connector-python` and `tqdm` modules
```
python3 -m pip install tqdm mysql-connector-python
```

## Usage

#### detect_infected_files.py
```
./detect_infected_files.py <PATH>
```
Search all js, php & html files recursively in the given path and list the infected ones in the file `infected_list.txt`<br>
Then you can use this list with the `fix_infected_file.py` script to fix them.


#### fix_infected_file.py
```
./fix_infected_file.py <INFECTED_FILES_LIST> <FULL_DOMAIN_NAME>
```
This script use the file created by `detect_infected_files.py` to fix all infected files.<br>
In some cases the malware replace the `wp_host_url` of your site with a bad one !<br>
That's why this script need your full domain name (like 'https://example.com') to fix that


#### detect_infected_database.py
```
./detect_infected_database.py
```
List all infected articles in the database

To use this script you need to open it and provide the WordPress database credentials
<br>You can find them in the wp-config.php file


#### fix_infected_database.py
```
./fix_infected_database.py
```
Fix all infected articles by removing the payload.

To use this script you need to open it and provide the WordPress database credentials
<br>You can find them in the wp-config.php file


#### payloads_file_to_test_fix.txt
This file contents all the raw payloads. You can use them to test the `fix_infected_file.py` script and improve it
