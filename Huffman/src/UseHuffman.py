'''
Created on 5 de mar de 2018

@author: raiff.anderson.mata
'''
from HuffmanCoding import HuffmanCoding  

#input file path
path = "samples.txt"

arq = open(path, 'r')
texto = arq.readlines()
for linha in texto :
    print(linha)
arq.close()

h = HuffmanCoding(path)

output_path = h.compress()
h.decompress(output_path)