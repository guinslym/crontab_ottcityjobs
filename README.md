# Download of the job list 

Script to download all the jobs available on Ottawacityjobs.ca

Execute the following commands:

> Fork this github application

> git clone .. your fork...

> cd crontab_ottcityjobs

> Open crontab.txt and change the location of your application i.e. /home/your_laptop/crontab_ottcityjobs/fetch.py

> In your Terminal type **crontab crontab.txt** this will add a crontab that will execute **each day at 5pm **

> chmod +x fetch.py

> touch /var/log/daily.log && chmod +x /var/log/daily.log

> **python fetch.py** to try it

##About
This script will download the list of jobs available in the city of Ottawa and it will insert all new jobs in a database.

