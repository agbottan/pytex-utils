
# ===================
#	FORMATA LINHAS
# ===================

# /////////////// IMPORTS

import re

# /////////////// CONFIG

sinal		= ';\d*;'
sepCampo	= '\t+'
multilinha	= ';;;'
formato		= None
ln			= '\n'

sepCampo = re.compile(sepCampo)

def montaCampos(linha,modelo):
	campos = re.split(sepCampo,linha)
	for campo in campos:
		#if re.search(sinal,linha) != None:
		#linha = re.sub(sinal,campo,modelo,1)
		linha = re.sub(sinal,campo,modelo)
	return linha

def formataLinhas(tx):

	linhas = tx.splitlines(False)

	for (i,linha) in enumerate(linhas):
		if re.search(sinal,linha) != None:
			formato = linha
			del linhas[i]
			break

	# Retira linhas em branco
	linhas[:] = [ L for L in linhas if( re.search('^\s*$',L) == None )]

	# Formata as linhas
	linhas[:] = [ montaCampos(L,formato) for L in linhas]

	return ln.join(linhas)
