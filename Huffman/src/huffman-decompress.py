import sys
import huffmancoding
python3 = sys.version_info.major >= 3


def main(args):
	# Coleta argumentos de linha de comando.
	if len(args) != 2:
		sys.exit("Usage: python huffman-decompress.py ArquivoEntrada ArquivoSaida")
	inputfile  = args[0]
	outputfile = args[1]
	
	# Realiza descompressao do arquivo
	bitin = huffmancoding.BitInputStream(open(inputfile, "rb"))
	out = open(outputfile, "wb")
	try:
		canoncode = read_code_len_table(bitin)
		code = canoncode.to_code_tree()
		decompress(code, bitin, out)
	finally:
		out.close()
		bitin.close()


def read_code_len_table(bitin):
	codelengths = []
	for i in range(257):
		# Le valores em big endian, 8 bits
		val = 0
		for j in range(8):
			val = (val << 1) | bitin.read_no_eof()
		codelengths.append(val)
	return huffmancoding.CanonicalCode(codelengths=codelengths)


def decompress(code, bitin, out):
	dec = huffmancoding.HuffmanDecoder(bitin)
	dec.codetree = code
	while True:
		symbol = dec.read()
		if symbol == 256:  # simbolo EOF
			break
		out.write(bytes((symbol,)) if python3 else chr(symbol))


# Main launcher
if __name__ == "__main__":
	main(sys.argv[1 : ])
