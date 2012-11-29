Project 3 for COMS E6111 Advanced Database Systems
-------------------------------------------------------------
a) Your name and your partner's name and Columbia UNI

Yuan Du (yd2234)
Akshai Sarma (as4107)

-------------------------------------------------------------
b) A list of all the files that you are submitting:
* Makefile		 (instructions on how to run the code)
* run.sh 		 (a shell script that runs all the codes)

-- src
* extract_Rule.py	(the main python script for finding association rules)

-- data
* TODO... (*.CSV) (CSV file containing the INTEGRATED-DATASET file)
* TODO... example-run.txt (output file of the interesting sample run)

-------------------------------------------------------------
c) A detailed description explaining: 
(a) which NYC Open Data data set(s) you used to generate the INTEGRATED-DATASET file:

We used "311 Service Requests 2009" dataset (from https://data.cityofnewyork.us/Service-Requests-311-/311-Service-Requests-2009/3rfa-3xsf).

-------------------------------------------------------------
(b) what (high-level) procedure you used to map the original NYC Open Data data set(s) into your INTEGRATED-DATASET file

Step 1. We sample the data by taking 10% of the whole data

Step 2. Since not all the columns have interesting attributes, so we selected those 5 attributes:

Created Date
Agency
Complaint Type
Location Type
Borough

-------------------------------------------------------------
(c) what makes your choice of INTEGRATED-DATASET file interesting (in other words, justify your choice of NYC Open Data data set(s))

TODO...

-------------------------------------------------------------
d) clear description of how to run your program 

Run the following from the directory where you put all the scripts (NOTE: you must cd to that directory before running this command):

sh run.sh <INTEGRATED-DATASET-FILE> <min_sup> <min_conf>

, where:
<INTEGRATED-DATASET-FILE> is the name of CSV file
<min_sup> is the value of minimun support
<min_conf> is the value of minimun confidence

For example, on a CLIC machine:
cd /home/yd2234/ADB/proj3/COMSW6111_P3
sh run.sh data/10k_5col.CSV 0.05 0.1 output.txt

TODO... change the CSV file name 

You can run our scripts directly by the commands above, since we have already put our scripts under that directory.

-------------------------------------------------------------
e) A clear description of the internal design of your project

We have only one python script: extract_Rule.py, with two main functions for large itemsets and association rules respectively.

Part 1. Large Itemsets

This part will extract large itemsets above the given minimum support. The main functions includes:
	* extractItemsets: A priori algorithm to extract the large itemsets
	* compute_L1: step 1 for A priori algorithm to compute L_1
	* getCandidate: candidate generation for A Priori Algorithm

Detailed description is as follows:

1. extractItemsets: the main function for A priori algorithm. Here we used the same A priori algorithm as described in Section 2.1 of the Agrawal and Srikant paper.

Our A priori algorithm is:

	Step 1. Genereate large 1-itemsets L_1 by calling function compute_L1.
	Step 2. As long as the previous L_{k-1} is non-empty, we compute the candidate C_k by calling function getCandidate. Then keep the candidates whose support is above min-sup as L_k.
	Step 3. Store all the large itemsets {L_k} and return

2. compute_L1: compute the first step of A priori algorithm to get L_1. To avoid reading the input file multiple times, we also store all the baskets in memory to speed up.

3. getCandidate: function to generate the candidates C_k for A priori algorithm. Here we used the similar Apriori Candidate Generation method as described in Section 2.1.1 of the Agrawal and Srikant paper. 

The slight difference is that we will never keep two items from the same column in one basket. For example, considering the column 'Month', no basket will have two months September and January. So we changed the join condition as "only the last items in the basket are from different columns".

Our Apriori Candidate Generation method is:

	* Data Structure: 
	Each item will contain two fields, the item value and the column number where this item is from. For example, one item is ('Bronx',5), which means the value for this item is 'Bronx', and it's from the 5-th column of the CSV file, indicating that's the Borough attribute. 
	So item.value = 'Bronx', and item.colNo = 5.
	
	The definitions for L_k and C_k are the same.

	* Join Step: 
	insert into C_k
	select p.item_1, p.item_2, ... , p.item_{k-1}, q.item_{k-1}
	from L_{k-1} p, L_{k-1} q
	where p.item_1 = q.item_1, ..., p.item_{k-2} = q.item_{k-2},
		p.item_{k-1}.colNo < q.item_{k-1}.colNo

	So our the items in each itemset are kept sorted in their column number, instead of lexicographic order. We have the assumption that items in different columns will never be the same (such as 'Month' and 'Complaint Type' columns will never share values). Therefore, it's ok to define such join condition "only the last items in p and q are from different columns". 

	* Prune Step: 
	Use the same prune method to remove candidates whose subsets are not in L_{k-1}. 

-------------------------------------------------------------
f) The command line specification of an interesting sample run

TODO...

-------------------------------------------------------------
g) Any additional information that you consider significant

TODO...
