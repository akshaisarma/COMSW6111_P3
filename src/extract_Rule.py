# Author: Yuan Du (yd2234@columbia.edu)
# Author: Akshai Sarma (as4107@columbia.edu)
# Date: Nov 23, 2012
# Function: extract large itemsets and association rules
# Usage: python extract_Rule.py <CSV-file> <min-sup> <min-conf> <output-file> <num-col>

import sys
from sets import Set
from collections import defaultdict

def getCandidate(L_previous):
	'''
	A Priori Algorithm candidate generation
	'''
	# get the list of all the large itemsets in L_{k-1}
	L_list = []
	for (l, value) in L_previous:
		L_list.append(l)

	# for l in L_list:
	# 	print ','.join(l)

	# STEP 1. Join
	L_join = [] # the list of all the itemsets after join
	# try any pair of two itemsets in L_list
	for i in range(0, len(L_list)):
		for j in range(i+1, len(L_list)):
			# print L_list[i], L_list[j]

			# try if (k-2) items in L_list[i] are in L_list[j]
			errNum = 0 # num of different items in two rows
			errItem = '' # store the different item in L_list[i]
			for item in L_list[i]:
				if item not in L_list[j]:
					errNum = errNum + 1
					# if there are >1 different items between L_list[i] and L_list[j]
					if errNum > 1:
						break
					# keep track of the only item that is not in L_list[j]
					errItem = item

			if (errNum == 1):
				# only one item different between L_list[i] and L_list[j]
				# find the errItem in L_list[j], add to joined_list
				joined_list = []
				for item in L_list[j]:
					if item not in L_list[i]:
						joined_list.append(item)
						break
				# add all the items in L_list[i]
				joined_list.extend(L_list[i])
				# sort by lexicographic order
				joined_list = sorted(joined_list)
				# store this itemset if not in L_join
				if joined_list not in L_join:
					L_join.append(joined_list)


	# STEP 2. prune
	L_k = []
	for l in L_join:
		# try if any (k-1) subset is in L_{k-1}
		ifValid = True
		for i in range(len(l)):
			# new_l contains k-1 items, and sorted
			new_l = list(l)
			del new_l[i]

			# new_l should be in L_{k-1}
			if new_l not in L_list:
				ifValid = False
				break

		if ifValid:
			# this is valid candidate
			L_k.append((l,0.0))

	return L_k

def getRules(itemset):
	'''
	Generates all possible rules LHS => RHS from attributes in item set
	such that there is at least one attribute in the LHS and exactly one in
	RHS, where LHS is a set and LHS intersect RHS is empty
	'''
	rules = []
	for rhs in itemset:
		C_LHS = list(itemset)
		C_LHS.remove(rhs)
		subsets = all_subsets(C_LHS)
		for lhs in subsets:
			rules.append([lhs, rhs, 0, 0])
	return rules

def all_subsets(c_lhs):
	'''
	Generates all subsets of input list
	'''
	num_elements = len(c_lhs)
	num_subsets = 2**num_elements

	subsets = []
	# Take each i as a bitvector for including the jth element if the jth bit
	# of i is 1. Don't include the empty set
	for i in range(1, num_subsets):
		subset = []
		for j in range(num_elements):
			if (i >> j & 1):
				subset.append(c_lhs[j])
		subsets.append(subset)
	return subsets

class extract_Rule(object):

	def __init__(self, n, min_sup, min_conf, CSV_file, output_file):
		self.n = n
		self.min_sup = min_sup
		self.min_conf = min_conf

		self.L_dict = defaultdict(list) # store each L_k (is a list of (itemset-list,sup) tuples)
		self.col_list = defaultdict(set) # each set is the set of all possible values in each column
		self.rule_list = [] # each rule is ([LHS], RHS, confidence, support)

		# initialize each column list by empty
		for i in range(self.n):
			value_set = set()
			self.col_list[i] = value_set

		self.nRow = 0 # num of rows
		self.maxK = 0 # largest itemset

		self.extractItemsets(CSV_file)
		self.extractRules(CSV_file)

		self.writeFile(output_file)

	def extractItemsets(self, CSV_file):
		'''
		A priori algorithm to extract the large itemsets
		'''
		# get L1
		self.compute_L1(CSV_file)

		# start with k=2
		k = 2
		L_previous = self.L_dict[k-1]
		while(True):
			# L_previous = self.L_dict[k-1]
			# check if L_{k-1} is empty
			if len(L_previous)<=0:
				self.maxK = k-1
				break

			# get the candidate C_k (this is a list of (itemset-list,sup) tuples)
			C_k = getCandidate(L_previous)
			L_k = []

			# compute the support of each candidate
			for line in open(CSV_file):
				line = line.strip()
				whole_attr_list = line.split(",")

				# try each candidate if it's contained in this row
				for i in range(len(C_k)):
					(c, value) = C_k[i]
					# c is a set which contains (k-1) items
					ifContained = True
					for item in c:
						# one attr in c is not in this row, break
						if item not in whole_attr_list:
							ifContained = False
							break
					# it's contained in this row, increase the count
					if ifContained:
						value = value + 1.0
						C_k[i] = (c, value)

			# after checking all the rows, get the support
			for (c, value) in C_k:
				value = value/self.nRow
				# print c, ";", value
				if value >= self.min_sup:
					L_k.append((c,value))

			# store L_k in L_dict[k] and update L_previous
			self.L_dict[k] = list(L_k)
			L_previous = list(L_k)

			k = k + 1


	def compute_L1(self, CSV_file):
		'''
		Get the set of possible values in each column,
		and stored in col_list.
		Also compute the first step L1 of A priori algorithm when k=1
		'''
		C1 = defaultdict(float)
		L1 = [] # L1 is the list of k=1 large itemsets, each is a (itemset-list,sup) tuple

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
			# print attr, ";", value
			if value >= self.min_sup:
				l = [attr]
				L1.append((l, value))

		# get the number of rows in the table
		self.nRow = nRow

		# store L1 in L_dict[1]
		self.L_dict[1] = L1


	def extractRules(self, CSV_file):
		'''
		Generates all rules for all itemsets of >=2.
		Computes confidence for all rules (in one pass over data file)
		'''
		f = open(CSV_file)

		# For each item set starting from 2, rule_dict will store all rules
		# for the item set, with its support. rule_dict[k] = [ ([Rules], support), ...]
		# Rules is [[LHS], RHS, tuplesWithLHSANDRHS, tuplesWithLHS]
		rule_dict = defaultdict(list)
		k = 2 # Start with item set of size 2

		while (k <= self.maxK):
			k_rules = []
			k_sets = self.L_dict[k]
			for (itemset, sup) in k_set:
				rules = getRules(itemset)
				k_rules.append((rules, sup))
			rule_dict[k] = k_rules
			k += 1

		for line in f:
			line = line.strip()
			values = set(line.split(","))
			# For now treat it as a set, will not work if same values in
			# different columns. Our code is agnostic to columns.
			k = 2
			while (k <= self.maxK):
				k_rules = rule_dict[k]
				for (rules, sup) in k_rules:
					for rule in rules:
						lhs = set(rule[0])
						rhs = set(rule[1])
						if lhs.issubset(values):
							rule[3] += 1
							if rhs in values:
								rule[2] += 1

		k = 2
		while (k <= self.maxK):
			k_rules = rule_dict[k]
			for (rules, sup) in k_rules:
				for rule in rules:
					conf = float(rule[2])/rule[3]
					if (conf >= self.min_conf):
						self.rule_dict.append((rule[0], rule[1], conf, sup)
		return

	def writeFile(self, output_file):
		# print "TODO... need to sort the output by support"
		# for k in self.L_dict:
		# 	# write L1
		# 	L1 = self.L_dict[k]
		# 	for (l, value) in L1:
		# 		# output_file.write("[%s], %f\n" % (attr, value))
		# 		output_file.write("["+",".join(l)+"], "+str(value)+"\n")

		sup = self.min_sup*100
		output_file.write("==Large itemsets (min_sup=%.0f%%)\n" % sup)

		# make all L_k into one list
		all_itemsets = []
		for k in self.L_dict:
			all_itemsets.extend(self.L_dict[k])

		# sort by support
		sorted_itemsets = sorted(all_itemsets, key=lambda student: student[1], reverse=True)
		for (l, value) in sorted_itemsets:
			output_file.write("["+",".join(l)+"], "+str(value)+"\n")

		conf = self.min_conf*100
		output_file.write("==High-confidence association rules (min_conf=%.0f%%)\n" % conf)
		sorted_rules = sorted(self.rule_list, key=lambda x: x[2], reverse=True)
		for rule in sorted_rules:
			output_file.write("[" + ",".join(rule[0]) + "] => [" + rule[1] + "]" +
								"(Conf: %.0f%%, Supp: %.0f%%)\n" % (rule[2]*100, rule[3]*100) )
		return

def usage():
	print """
	Usage:
	python extract_Rule.py <CSV-file> <min-sup> <min-conf> <output-file> <num-col>
	where <CSV-file> is INTEGRATED-DATASET file,
		<min-sup> is the value of minimun support,
		<min-conf> is the value of minimun confidence,
		<output-file> is the output of the large itemsets and rules,
		<num-col> is the number of columns in the table.

	For example: python extract_Rule.py ../data/new.CSV 0.01 0.1 output.txt 2
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
