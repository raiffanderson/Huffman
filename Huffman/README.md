Passos para execução:

	- Compressão Huffman:
		Executar o arquivo huffman-compress.py passando os arquivos de entrada e saida. Por exemplo: python huffman-compress.py ArquivoEntrada ArquivoSaida".
		
	- Descompressão Huffman:
		Executar o arquivo huffman-decompress.py passando os arquivos de entrada e saida. Por exemplo: python huffman-decompress.py ArquivoEntrada ArquivoSaida"
		
		
	Estrutura:
	
	src/: Parta com os arquivos fontes do código.
		huffmancoding.py: Arquivo usado como biblioteca tanto pelo compressor, quanto pelo descompressor.
		huffman-compress.py. Arquivo responsável pelo compressão do arquivo passado na linha de comando.
		huffman-compress.py. Arquivo responsável pelo descompressão do arquivo passado na linha de comando.
		
	files/: Pasta com arquivos originais e arquivos gerados.
		email.txt: arquivo com conteúdo de email;
		email_compressed.bin: compressão do arquivo email.txt ;
		email_decompressed.txt: decompressão do arquivo email_compressed.bin;
		mutual_information.html: arquivo com conteúdo de mutual_information;
		mutual_information_compressed.bin:  compressão do arquivo mutual_information.bin;
		mutual_information_decompressed.html:  descompressão do arquivo mutual_information.bin
	