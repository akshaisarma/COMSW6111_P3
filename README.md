COMSW6111_P3
============

 COMS E6111-Advanced Database Systems -- Project 3

1. Download the 311 datasets in 2009 from 
[here](https://data.cityofnewyork.us/Service-Requests-311-/311-Service-Requests-2009/3rfa-3xsf)

2. Put the CSV file under the directory `data` to be `data/311_Service_Requests_2009.csv`

3. Run generate_CSV.py in scr/.

For example:
python generate_CSV.py ../data/311_Service_Requests_2009.csv ../data/attr_list.txt ../data/new.CSV

This will write two columns <Complaint-type> and <Borough> from first 1000 rows in the whole table into the output file `data/new.CSV`