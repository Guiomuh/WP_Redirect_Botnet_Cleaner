# WordPress Redirect Botnet Cleaner 

## Intro 

Recently I detected some waves of WordPress infections<br>
Based on XSS Stored vulnerabilities in various themes & plugins

This botnet use the following domain names:
- letsmakeparty3.ga
- lobbydesires.com
- train.developfirstline.com
- track.developfirstline.com
- ws.stivenfernando.com
- dontstopthismusics.com
- blackentertainments.com
- js.digestcolect.com

This malware is very invasive it can infect all js, php, html files and all articles in the database of your WordPress.

In some cases the `home_url` and `site_url` of your website are replaced by the malware domain causing redirections.

After some work I decided to make these scripts to easily detect & patch infected WordPress.

You can find the PART1 of my work on the "lobbydesires.com" version [HERE](https://medium.com/@guillaume.muh/lobbydesires-botnet-927bbc139457) (FRENCH)<br>
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
Then you can use this list with the `fix_infected_files.py` script to fix them.

This script also search for temp/log files used by the malware and raise an alert but this files aren't deleted in the `fix_infected_files.py` script due to the high risk of false positive.

#### fix_infected_files.py
```
./fix_infected_files.py <INFECTED_FILES_LIST>
```
This script use the file created by `detect_infected_files.py` to fix all infected files.<br><br>


#### detect_infected_database.py
```
./detect_infected_database.py
```
List all infected articles in the database and check if the `home_url` and `site_url` are infected

To use this script you need to open `config.py` and provide the WordPress database credentials 
<br>You can find them in the wp-config.php file

You need also to complete the domain value in the `config.py` file



#### fix_infected_database.py
```
./fix_infected_database.py
```
Fix all infected articles by removing the payload and replace the infected `home_url` and `site_url` in the database.

To use this script you need to open `config.py` and provide the WordPress database credentials 
<br>You can find them in the wp-config.php file

You need also to complete the domain value in the `config.py` file


#### payloads_file_to_test_fix.txt
This file contents all the raw payloads. You can use them to test the `fix_infected_files.py` script and improve it

#### config.py
This file contents some constants and the detection regex used to find infection in such a way that it's easy to scale up if the botnet migrate to a new domain.
