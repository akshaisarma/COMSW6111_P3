# Author: Yuan Du (yd2234@columbia.edu)
# Date: Nov 23, 2012
# Function: extract large itemsets and association rules
# Usage: python extract_Rule.py <CSV-file> <min-sup> <min-conf> <output-file> <num-col>


import sys
from sets import Set
from collections import defaultdict

def getCandidate(L_previous):
	# 

class extract_Rule(object):

	def __init__(self, n, min_sup, min_conf, CSV_file, output_file):
		self.n = n
		self.min_sup = min_sup
		self.min_conf = min_conf

		self.L_dict = defaultdict(defaultdict) # store each L_k
		self.col_list = defaultdict(set) # each set is the set of all possible values in the column
		# initialize each column list by empty
		for i in range(self.n):
			value_set = set()
			self.col_list[i] = value_set

		self.nRow = 0 # num of rows

		self.extractItemsets(CSV_file)
		# self.extractRules(CSV_file)

		self.writeFile(output_file)

	def extractItemsets(self, CSV_file):
		'''
		A priori algorithm to extract the large itemsets
		'''
		# get L1
		self.compute_L1(CSV_file)

		# start with k=2
		k = 2
		while(True):
			L_previous = L_dict[k-1]
			# check if L_{k-1} is empty
			if (len(L_previous)<=0)
				break

			# get the candidate C_k (this is a dictionary)
			C_k = getCandidate(L_previous)
			L_k = defaultdict(float)

			# compute the support of each candidate
			for line in open(CSV_file):
				line = line.strip()
				whole_attr_list = line.split(",")

				# try each candidate if it's contained in this row
				for c in C_k:
					# c is a list which contains (k-1) items
					ifContained = True
					for item in c:
						# one attr in c is not in this row, break
						if item not in whole_attr_list:
							ifContained = False
							break
					# it's contained in this row, increase the count
					if ifContained:
						C_k[c] = C_k[c] + 1.0

			# after checking all the rows, get the support
			for c in C_k:
				value = C_k[c]/self.nRow
				# print c, ";", value
				if value >= self.min_sup:
					L_k[attr] = value

			# store L_k in L_dict[k] and update L_previous
			L_dict[k] = L_k
			L_previous = L_k

			k = k + 1


	def compute_L1(self, CSV_file):
		'''
		Get the set of possible values in each column,
		and stored in col_list.
		Also compute the first step L1 of A priori algorithm when k=1
		'''
		C1 = defaultdict(float)
		L1 = defaultdict(float)

		nRow = 0
		for line in open(CSV_file):
			line = line.strip()
			nRow = nRow + 1 # count the number of rows
			whole_attr_list = line.split(",")
			for i in range(len(whole_attr_list)):
				# store this value to 
				attr = whole_attr_list[i]
				# ignore empty item
				if len(attr)<=0:
					continue
				C1[attr] = C1[attr] + 1.0
				if len(attr)>0:
					self.col_list[i].add(attr)

		# compute the support for each item in C1, picking large items in L1
		for attr in C1:
			value = C1[attr]/nRow
			print attr, ";", value
			if value >= self.min_sup:
				L1[attr] = value

		# get the number of rows in the table
		self.nRow = nRow

		# store L1 in L_dict[1]
		self.L_dict[1] = L1


	def writeFile(self, output_file):
		# write L1
		L1 = self.L_dict[1]
		for attr in L1:
			value = L1[attr]
			output_file.write("[%s], %f\n" % (attr, value))

def usage():
	print """
	Usage:
	python extract_Rule.py <CSV-file> <min-sup> <min-conf> <output-file> <num-col>
	where <CSV-file> is INTEGRATED-DATASET file,
		<min-sup> is the value of minimun support,
		<min-conf> is the value of minimun confidence,
		<output-file> is the output of the large itemsets and rules,
		<num-col> is the number of columns in the table.

	For example: python extract_Rule.py new.CSV 0.1 0.1 output.txt 2
	"""

if __name__ == "__main__":

	if len(sys.argv)!=6: # Expect exactly three arguments
		usage()
		sys.exit(2)

	# try:
	# 	CSV_input = file(sys.argv[1],"r")
	# except IOError:
	# 	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % (sys.argv[1]))
	# 	sys.exit(1)
	CSV_file = sys.argv[1]

	try:
		output_file = file(sys.argv[4],"w")
	except IOError:
		sys.stderr.write("ERROR: Cannot write outputfile %s.\n" % (sys.argv[4]))
		sys.exit(1)

	n = int(sys.argv[5])
	min_sup = float(sys.argv[2])
	min_conf = float(sys.argv[3])
	ex = extract_Rule(n, min_sup, min_conf, CSV_file, output_file)

