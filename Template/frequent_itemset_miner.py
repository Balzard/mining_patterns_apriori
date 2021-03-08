"""
Skeleton file for the project 1 of the LINGI2364 course.
Use this as your submission file. Every piece of code that is used in your program should be put inside this file.

This file given to you as a skeleton for your implementation of the Apriori and Depth
First Search algorithms. You are not obligated to use them and are free to write any class or method as long as the
following requirements are respected:

Your apriori and alternativeMiner methods must take as parameters a string corresponding to the path to a valid
dataset file and a double corresponding to the minimum frequency.
You must write on the standard output (use the print() method) all the itemsets that are frequent in the dataset file
according to the minimum frequency given. Each itemset has to be printed on one line following the format:
[<item 1>, <item 2>, ... <item k>] (<frequency>).
Tip: you can use Arrays.toString(int[] a) to print an itemset.

The items in an itemset must be printed in lexicographical order. However, the itemsets themselves can be printed in
any order.

Do not change the signature of the apriori and alternative_miner methods as they will be called by the test script.

__authors__ = "<write here your group, first name(s) and last name(s)>"
"""

import itertools, time
from marisa_trie import Trie

class Dataset:
	"""Utility class to manage a dataset stored in a external file."""

	def __init__(self, filepath):
		"""reads the dataset file and initializes files"""
		self.transactions = list()
		self.items = set()

		try:
			lines = [line.strip() for line in open(filepath, "r")]
			lines = [line for line in lines if line]  # Skipping blank lines
			for line in lines:
				transaction = list(map(int, line.split(" ")))
				self.transactions.append(transaction)
				for item in transaction:
					self.items.add(item)
		except IOError as e:
			print("Unable to read dataset file!\n" + e)

	def trans_num(self):
		"""Returns the number of transactions in the dataset"""
		return len(self.transactions)

	def items_num(self):
		"""Returns the number of different items in the dataset"""
		return len(self.items)

	def get_transaction(self, i):
		"""Returns the transaction at index i as an int array"""
		return self.transactions[i]


# code taken from : https://www.geeksforgeeks.org/python-program-to-get-all-subsets-of-given-size-of-a-set/
# Allow to find all subsets of a given a size of a set
def findsubsets(s, n): 
    return list(itertools.combinations(s, n))

# compute frequency of an itemset in dataset
def compute_freq(itemset, dataset,data_size):
	freq = 0
	for i in range(data_size):
		if set(itemset).issubset(set(dataset.get_transaction(i))):
			freq = freq + 1
	return freq/data_size

# check if an itemset is frequent for a min_freq
def is_frequent(itemset, dataset, data_size, min_freq):
	freq = 0
	for i in range(data_size):
		if set(itemset).issubset(set(dataset.get_transaction(i))):
			freq = freq + 1
		if freq >= min_freq:
			return True
	return False

# return support of an itemset
def get_support(itemset,dataset,data_size):
	supp = 0
	for i in range(data_size):
		if set(itemset).issubset(set(dataset.get_transaction(i))):
			supp = supp + 1
	return supp

# convert itemset to string
def listToString(itemset):
	return ','.join(str(i) for i in itemset)

# combine itemsets that are identical except for last symbol
def combine_items(itemset1, itemset2):
	if itemset1[:-1] == itemset2[:-1]:
		try: 
			tmp1 = int(itemset1[-1])
			tmp2 = int(itemset2[-1])
			if tmp1 >= tmp2:
				ret = itemset2 + [itemset1[-1]]
				return ret
			else:
				ret = itemset1 + [itemset2[-1]]
				return ret
			
		except TypeError:
			print('must be integers')

	else:
		#print('strings must be identical except for last symbol')
		return 0

# gen candidates 
def gen_candidates(itemset):
	ret = []
	for i in range(len(itemset)):
		c = i + 1
		while(c < len(itemset)):
			if len(itemset[i]) > 1:
				tmp = combine_items(itemset[i],itemset[c])
				if tmp != 0:
					ret.append(tmp)
			else:
				tmp = itemset[i] + itemset[c]
				ret.append(tmp)
			c += 1
	return ret


def apriori(filepath, minFrequency):
	"""Runs the apriori algorithm on the specified file with the given minimum frequency"""
	start = time.time()
	data = Dataset(filepath)
	nb_trans = data.trans_num()
	items = data.items_num()
	f = {j:[] for j in range(items+1)}
	c = {j:[] for j in range(items+1)}
	i = 1
	while(True):
		if i == 1:
			c[i] = [[k] for k in range(1,items+1)]
		else:
			c[i] = gen_candidates([i[0] for i in f[i-1]])
			
		for elem in c[i]:
			tmp = compute_freq(elem,data,nb_trans)
			if tmp >= minFrequency:
				print(elem,(tmp))
				f[i].append((elem,tmp))
		if not(len(f[i]) > 0):
			break
		
		i += 1

	end = time.time()
	t = end - start
	return f"Finished in {t:.3f} seconde(s)"

print(apriori('./Datasets/chess.dat',0.9))


def alternative_miner(filepath, minFrequency):
	"""Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency"""
	# TODO: either second implementation of the apriori algorithm or implementation of the depth first search algorithm
	print("Not implemented")

data = Dataset("./Datasets/toy.dat")
trans = data.get_transaction(1)
items = data.items_num()
size = data.trans_num()
trie = Trie(['key1', 'key2', 'key12'])
#print(listToString([1,2,3,4,5]))
#print(apriori("./Datasets/toy.dat",0.5))
