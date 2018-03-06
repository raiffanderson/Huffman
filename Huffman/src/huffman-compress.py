import sys
import huffmancoding
python3 = sys.version_info.major >= 3


def main(args):
	# Coleta argumentos de linha de comando. 
	if len(args) != 2:
		sys.exit("Usage: python huffman-compress.py ArquivoEntrada ArquivoSaida")
	inputfile  = args[0]
	outputfile = args[1]
	
	# Le arquivo de entrada para processar a frequencia dos simbolos
	freqs = get_frequencies(inputfile)
	freqs.increment(256)  # simbolo EOF recebe frequencia 1.
	code = freqs.build_code_tree()
	canoncode = huffmancoding.CanonicalCode(tree=code, symbollimit=257)

	code = canoncode.to_code_tree()
	
	# le arquivo novamente, comprime e escreve no arquivo saida.
	inp = open(inputfile, "rb")
	bitout = huffmancoding.BitOutputStream(open(outputfile, "wb"))
	try:
		write_code_len_table(bitout, canoncode)
		compress(code, inp, bitout)
	finally:
		bitout.close()
		inp.close()


# Retorna tabela de frequencia baseada no arquivo dado.
def get_frequencies(filepath):
	freqs = huffmancoding.FrequencyTable([0] * 257)
	with open(filepath, "rb") as input:
		while True:
			b = input.read(1)
			if len(b) == 0:
				break
			b = b[0] if python3 else ord(b)
			freqs.increment(b)
	return freqs


def write_code_len_table(bitout, canoncode):
	for i in range(canoncode.get_symbol_limit()):
		val = canoncode.get_code_length(i)
		# Suporta apenas codigos de tamanho maximo 256.
		if val >= 256:
			raise ValueError("Codigo do simbolo muito grande")
		
		# Escreve valores em big endian, 8 bits
		for j in reversed(range(8)):
			bitout.write((val >> j) & 1)


def compress(code, inp, bitout):
	enc = huffmancoding.HuffmanEncoder(bitout)
	enc.codetree = code
	while True:
		b = inp.read(1)
		if len(b) == 0:
			break
		enc.write(b[0] if python3 else ord(b))
	enc.write(256)  # EOF


# Main
if __name__ == "__main__":
	main(sys.argv[1 : ])
