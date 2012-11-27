# Author: Yuan Du (yd2234@columbia.edu)
# Date: Nov 23, 2012
# Function: generate INTEGRATED-DATASET CSV file 
# Usage: python generate_CSV.py <raw-CSV-file> <attr-list-file> <new-CSV-file> 


import sys
from sets import Set
import re

MAXROWS = 10 # use this to limit the num of rows (-1 if no limit)
# MAXROWS = -1 # use this to limit the num of rows (-1 if no limit)

class attribute_selection(object):

	def __init__(self, attr_list_file, CSV_input, CSV_output):
		self.attr_list = set()
		self.index_list = set()

		self.create_attr_list(attr_list_file)
		self.generate(CSV_input, CSV_output)

		# for i in self.index_list:
		# 	print 'i=',i

	def create_attr_list(self, attr_list_file):
		'''
		get the attribute list from attr_list_file
		'''
		l = attr_list_file.readline()
		while l:
			line = l.strip()
			if line:
				self.attr_list.add(line)

			l = attr_list_file.readline()

	def generate(self, CSV_input, CSV_output):
		'''
		Read the first line for attribute info,
		and re-generate CSV line by line with only attributes in the list
		'''
		# try:
		# 	CSV_output2 = file('first1000.CSV',"w")
		# except IOError:
		# 	sys.stderr.write("ERROR: Cannot write outputfile %s.\n" % (CSV_output2))
		# 	sys.exit(1)
		
		index = 0
		l = CSV_input.readline()
		while l:
			line = l.strip()
			line = re.sub(r"\"[^\"]*\"", "", line)
			if line:
				# check if this is the first line
				if index == 0:
					# this is the first line: each item is the name of attributes
					whole_attr_list = line.split(",")
					for i in range(len(whole_attr_list)):
						# check if this is valid attribute
						attr = whole_attr_list[i]
						if attr in self.attr_list:
							# print i
							self.index_list.add(i)
				else:
					# this is general row of the tables: each item is the value of attributes
					whole_attr_list = line.split(",")
					firstAttr = True
					for i in range(len(whole_attr_list)):
						# check if this is valid attribute
						if i in self.index_list:
							# general attributes
							attr = whole_attr_list[i]	
							# replace 'Unspecified' as ''
							if attr == 'Unspecified':
								attr = ''

							if i == 1:
								# this is "Created Date" attribute. we only need month
								# e.g., 01/01/2009 12:00 AM making it to M-01
								date_list = attr.split("/")

								if len(date_list) >= 3 and len(date_list[0])>0:
									attr = 'M-'+date_list[0] 
								else:
									attr = ''


							if firstAttr:
								CSV_output.write(attr)
								firstAttr = False
							else:
								CSV_output.write(','+attr)
					if firstAttr==False:
						CSV_output.write("\n")


				index = index + 1
				# CSV_output2.write(line)
				# CSV_output2.write("\n")

			if MAXROWS>0 and index >MAXROWS:
				break
				
			l = CSV_input.readline()



		


def usage():
	print """
	Usage:
	python generate_CSV.py <raw-CSV-file> <attr-list-file> <new-CSV-file> 
	where <raw-CSV-file> is the original CSV file downloaded from website,
		<attr-list-file> is the file with the list of attributes to
		be included in new CSV file, and
		<new-CSV-file> is generated CSV file.

	For example: python generate_CSV.py ../data/311_Service_Requests_2009.csv ../data/attr_list.txt ../data/new.CSV
	"""

if __name__ == "__main__":

	if len(sys.argv)!=4: # Expect exactly three arguments
		usage()
		sys.exit(2)

	try:
		CSV_input = file(sys.argv[1],"r")
		attr_list_file = file(sys.argv[2],"r")
	except IOError:
		sys.stderr.write("ERROR: Cannot read inputfile %s or %s.\n" % (sys.argv[1], sys.argv[2]))
		sys.exit(1)

	try:
		CSV_output = file(sys.argv[3],"w")
	except IOError:
		sys.stderr.write("ERROR: Cannot write outputfile %s.\n" % (sys.argv[3]))
		sys.exit(1)

	ge = attribute_selection(attr_list_file, CSV_input, CSV_output)
