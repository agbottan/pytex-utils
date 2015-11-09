
#################
#	ENTITIES	#
#################

import re

def formataTabelas(tx):

	# tabela		= tx.split('\n')
	# tabela[:]	= [linha.split('\t') for linha in tabela]
	# return str(tabela)

	#tx = re.sub('^(.*?)$','<tr>$1</tr>',tx,re.MULTILINE)
	tx = re.sub('.','-',tx)

	return tx

# teste