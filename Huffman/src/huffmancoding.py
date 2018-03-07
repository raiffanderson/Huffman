# 
# Reference Huffman coding
# Copyright (c) Project Nayuki
# 
# https://www.nayuki.io/page/reference-huffman-coding
# https://github.com/nayuki/Reference-Huffman-coding
# 

import heapq, sys
python3 = sys.version_info.major >= 3


# ---- Huffman coding core classes ----

# Encodes symbols and writes to a Huffman-coded bit stream.
class HuffmanEncoder(object):
	
	# Constructs a Huffman encoder based on the given bit output stream.
	def __init__(self, bitout):
		# The underlying bit output stream
		self.output = bitout
		# The code tree to use in the next write() operation. Must be given a suitable value
		# value before calling write(). The tree can be changed after each symbol encoded, as long
		# as the encoder and decoder have the same tree at the same point in the code stream.
		self.codetree = None
	
	
	# Encodes the given symbol and writes to the Huffman-coded output stream.
	def write(self, symbol):
		if not isinstance(self.codetree, CodeTree):
			raise ValueError("Invalid current code tree")
		bits = self.codetree.get_code(symbol)
		for b in bits:
			self.output.write(b)



# Reads from a Huffman-coded bit stream and decodes symbols.
class HuffmanDecoder(object):
	
	# Constructs a Huffman decoder based on the given bit input stream.
	def __init__(self, bitin):
		# The underlying bit input stream
		self.input = bitin
		# The code tree to use in the next read() operation. Must be given a suitable value
		# value before calling read(). The tree can be changed after each symbol decoded, as long
		# as the encoder and decoder have the same tree at the same point in the code stream.
		self.codetree = None
	
	
	# Reads from the input stream to decode the next Huffman-coded symbol.
	def read(self):
		if not isinstance(self.codetree, CodeTree):
			raise ValueError("Invalid current code tree")
		currentnode = self.codetree.root
		while True:
			temp = self.input.read_no_eof()
			if   temp == 0: nextnode = currentnode.leftchild
			elif temp == 1: nextnode = currentnode.rightchild
			else: raise AssertionError("Invalid value from read_no_eof()")
			
			if isinstance(nextnode, Leaf):
				return nextnode.symbol
			elif isinstance(nextnode, InternalNode):
				currentnode = nextnode
			else:
				raise AssertionError("Illegal node type")



# A table of symbol frequencies. Mutable. Symbols values are numbered
# from 0 to symbolLimit-1. A frequency table is mainly used like this:
# 0. Collect the frequencies of symbols in the stream that we want to compress.
# 1. Build a code tree that is statically optimal for the current frequencies.
class FrequencyTable(object):
	
	# Constructs a frequency table from the given sequence of frequencies.
	# The sequence length must be at least 2, and each value must be non-negative.
	def __init__(self, freqs):
		self.frequencies = list(freqs)  # Make a copy
		if len(self.frequencies) < 2:
			raise ValueError("At least 2 symbols needed")
		for x in self.frequencies:
			if x < 0:
				raise ValueError("Negative frequency")
	
	
	# Returns the number of symbols in this frequency table. The result is always at least 2.
	def get_symbol_limit(self):
		return len(self.frequencies)
	
	
	# Returns the frequency of the given symbol in this frequency table. The result is always non-negative.
	def get(self, symbol):
		self._check_symbol(symbol)
		return self.frequencies[symbol]
	
	
	# Sets the frequency of the given symbol in this frequency table to the given value.
	def set(self, symbol, freq):
		self._check_symbol(symbol)
		if freq < 0:
			raise ValueError("Negative frequency")
		self.frequencies[symbol] = freq
	
	
	# Increments the frequency of the given symbol in this frequency table.
	def increment(self, symbol):
		self._check_symbol(symbol)
		self.frequencies[symbol] += 1
	
	
	# Returns silently if 0 <= symbol < len(frequencies), otherwise raises an exception.
	def _check_symbol(self, symbol):
		if 0 <= symbol < len(self.frequencies):
			return
		else:
			raise ValueError("Symbol out of range")
	
	
	# Returns a string representation of this frequency table,
	# useful for debugging only, and the format is subject to change.
	def __str__(self):
		result = ""
		for (i, freq) in enumerate(self.frequencies):
			result += "{}\t{}\n".format(i, freq)
		return result
	
	
	# Returns a code tree that is optimal for the symbol frequencies in this table.
	# The tree always contains at least 2 leaves (even if they come from symbols with
	# 0 frequency), to avoid degenerate trees. Note that optimal trees are not unique.
	def build_code_tree(self):
		# Note that if two nodes have the same frequency, then the tie is broken
		# by which tree contains the lowest symbol. Thus the algorithm has a
		# deterministic output and does not rely on the queue to break ties.
		# Each item in the priority queue is a tuple of type (int frequency,
		# int lowestSymbol, Node node). As per Python rules, tuples are ordered asceding
		# by the lowest differing index, e.g. (0, 0) < (0, 1) < (0, 2) < (1, 0) < (1, 1).
		pqueue = []
		
		# Add leaves for symbols with non-zero frequency
		for (i, freq) in enumerate(self.frequencies):
			if freq > 0:
				heapq.heappush(pqueue, (freq, i, Leaf(i)))
		
		# Pad with zero-frequency symbols until queue has at least 2 items
		for (i, freq) in enumerate(self.frequencies):
			if len(pqueue) >= 2:
				break
			if freq == 0:
				heapq.heappush(pqueue, (freq, i, Leaf(i)))
		assert len(pqueue) >= 2
		
		# Repeatedly tie together two nodes with the lowest frequency
		while len(pqueue) > 1:
			x = heapq.heappop(pqueue)  # Tuple of (frequency, lowest symbol, node object)
			y = heapq.heappop(pqueue)  # Tuple of (frequency, lowest symbol, node object)
			z = (x[0] + y[0], min(x[1], y[1]), InternalNode(x[2], y[2]))  # Construct new tuple
			heapq.heappush(pqueue, z)
		
		# Return the remaining node
		return CodeTree(pqueue[0][2], len(self.frequencies))




class CodeTree(object):
	

	def __init__(self, root, symbollimit):
		# Recursive helper function
		def build_code_list(node, prefix):
			if isinstance(node, InternalNode):
				build_code_list(node.leftchild , prefix + (0,))
				build_code_list(node.rightchild, prefix + (1,))
			elif isinstance(node, Leaf):
				if node.symbol >= symbollimit:
					raise ValueError("Symbol exceeds symbol limit")
				if self.codes[node.symbol] is not None:
					raise ValueError("Symbol has more than one code")
				self.codes[node.symbol] = prefix
			else:
				raise AssertionError("Illegal node type")
		
		if symbollimit < 2:
			raise ValueError("At least 2 symbols needed")
		self.root = root

		self.codes = [None] * symbollimit
		build_code_list(root, ())  # Fill 'codes' with appropriate data
	
	

	def get_code(self, symbol):
		if symbol < 0:
			raise ValueError("Illegal symbol")
		elif self.codes[symbol] is None:
			raise ValueError("No code for given symbol")
		else:
			return self.codes[symbol]
	
	
	def __str__(self):
		# Recursive helper function
		def to_str(prefix, node):
			if isinstance(node, InternalNode):
				return to_str(prefix + "0", node.leftchild) + to_str(prefix + "0", node.rightchild)
			elif isinstance(node, Leaf):
				return "Code {}: Symbol {}\n".format(prefix, node.symbol)
			else:
				raise AssertionError("Illegal node type")
		
		return to_str("", self.root)



class Node(object):
	pass


class InternalNode(Node):
	def __init__(self, left, right):
		if not isinstance(left, Node) or not isinstance(right, Node):
			raise TypeError()
		self.leftchild = left
		self.rightchild = right


# A leaf node in a code tree. It has a symbol value.
class Leaf(Node):
	def __init__(self, sym):
		if sym < 0:
			raise ValueError("Symbol value must be non-negative")
		self.symbol = sym

class CanonicalCode(object):
	
	def __init__(self, codelengths=None, tree=None, symbollimit=None):
		if codelengths is not None and tree is None and symbollimit is None:
			# Check basic validity
			if len(codelengths) < 2:
				raise ValueError("At least 2 symbols needed")
			for cl in codelengths:
				if cl < 0:
					raise ValueError("Illegal code length")
			
			# Copy once and check for tree validity
			codelens = sorted(codelengths, reverse=True)
			currentlevel = codelens[0]
			numnodesatlevel = 0
			for cl in codelens:
				if cl == 0:
					break
				while cl < currentlevel:
					if numnodesatlevel % 2 != 0:
						raise ValueError("Under-full Huffman code tree")
					numnodesatlevel //= 2
					currentlevel -= 1
				numnodesatlevel += 1
			while cl < currentlevel:
				if numnodesatlevel % 2 != 0:
					raise ValueError("Under-full Huffman code tree")
				numnodesatlevel //= 2
				currentlevel -= 1
			if numnodesatlevel < 1:
				raise ValueError("Under-full Huffman code tree")
			if numnodesatlevel > 1:
				raise ValueError("Over-full Huffman code tree")
			
			# Copy again
			self.codelengths = list(codelengths)
		
		elif tree is not None and symbollimit is not None and codelengths is None:
			# Recursive helper method
			def build_code_lengths(node, depth):
				if isinstance(node, InternalNode):
					build_code_lengths(node.leftchild , depth + 1)
					build_code_lengths(node.rightchild, depth + 1)
				elif isinstance(node, Leaf):
					# Note: CodeTree already has a checked constraint that disallows a symbol in multiple leaves
					if self.codelengths[node.symbol] != 0:
						raise AssertionError("Symbol has more than one code")
					if node.symbol >= len(self.codelengths):
						raise ValueError("Symbol exceeds symbol limit")
					self.codelengths[node.symbol] = depth
				else:
					raise AssertionError("Illegal node type")
			
			if symbollimit < 2:
				raise ValueError("At least 2 symbols needed")
			self.codelengths = [0] * symbollimit
			build_code_lengths(tree.root, 0)
		
		else:
			raise ValueError("Invalid arguments")
	
	
	def get_symbol_limit(self):
		return len(self.codelengths)
	
	
	def get_code_length(self, symbol):
		if 0 <= symbol < len(self.codelengths):
			return self.codelengths[symbol]
		else:
			raise ValueError("Symbol out of range")
	
	
	def to_code_tree(self):
		nodes = []
		for i in range(max(self.codelengths), -1, -1):  # Descend through code lengths
			assert len(nodes) % 2 == 0
			newnodes = []
			
			if i > 0:
				for (j, codelen) in enumerate(self.codelengths):
					if codelen == i:
						newnodes.append(Leaf(j))
			
			# Merge pairs of nodes from the previous deeper layer
			for j in range(0, len(nodes), 2):
				newnodes.append(InternalNode(nodes[j], nodes[j + 1]))
			nodes = newnodes
		
		assert len(nodes) == 1
		return CodeTree(nodes[0], len(self.codelengths))




class BitInputStream(object):
	
	def __init__(self, inp):
		self.input = inp
		self.currentbyte = 0
		self.numbitsremaining = 0
	
	
	def read(self):
		if self.currentbyte == -1:
			return -1
		if self.numbitsremaining == 0:
			temp = self.input.read(1)
			if len(temp) == 0:
				self.currentbyte = -1
				return -1
			self.currentbyte = temp[0] if python3 else ord(temp)
			self.numbitsremaining = 8
		assert self.numbitsremaining > 0
		self.numbitsremaining -= 1
		return (self.currentbyte >> self.numbitsremaining) & 1
	
	
	def read_no_eof(self):
		result = self.read()
		if result != -1:
			return result
		else:
			raise EOFError()
	
	
	# Closes this stream and the underlying input stream.
	def close(self):
		self.input.close()
		self.currentbyte = -1
		self.numbitsremaining = 0



class BitOutputStream(object):
	
	# Constructs a bit output stream based on the given byte output stream.
	def __init__(self, out):
		self.output = out  # The underlying byte stream to write to
		self.currentbyte = 0  # The accumulated bits for the current byte, always in the range [0x00, 0xFF]
		self.numbitsfilled = 0  # Number of accumulated bits in the current byte, always between 0 and 7 (inclusive)
	
	
	# Writes a bit to the stream. The given bit must be 0 or 1.
	def write(self, b):
		if b not in (0, 1):
			raise ValueError("Argument must be 0 or 1")
		self.currentbyte = (self.currentbyte << 1) | b
		self.numbitsfilled += 1
		if self.numbitsfilled == 8:
			towrite = bytes((self.currentbyte,)) if python3 else chr(self.currentbyte)
			self.output.write(towrite)
			self.currentbyte = 0
			self.numbitsfilled = 0
	
	
	def close(self):
		while self.numbitsfilled != 0:
			self.write(0)
		self.output.close()
