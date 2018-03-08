Passos para execu��o:

	- Compress�o Huffman:
		Executar o arquivo huffman-compress.py passando os arquivos de entrada e saida. Por exemplo: python huffman-compress.py ArquivoEntrada ArquivoSaida".
		
	- Descompress�o Huffman:
		Executar o arquivo huffman-decompress.py passando os arquivos de entrada e saida. Por exemplo: python huffman-decompress.py ArquivoEntrada ArquivoSaida"
		
		
	Estrutura:
	
	src/: Parta com os arquivos fontes do c�digo.
		huffmancoding.py: Arquivo usado como biblioteca tanto pelo compressor, quanto pelo descompressor.
		huffman-compress.py. Arquivo respons�vel pelo compress�o do arquivo passado na linha de comando.
		huffman-compress.py. Arquivo respons�vel pelo descompress�o do arquivo passado na linha de comando.
		
	files/: Pasta com arquivos originais e arquivos gerados.
		email.txt: arquivo com conte�do de email;
		email_compressed.bin: compress�o do arquivo email.txt ;
		email_decompressed.txt: decompress�o do arquivo email_compressed.bin;
		mutual_information.html: arquivo com conte�do de mutual_information;
		mutual_information_compressed.bin:  compress�o do arquivo mutual_information.bin;
		mutual_information_decompressed.html:  descompress�o do arquivo mutual_information.bin
	