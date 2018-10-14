
# ===================
#	FORMATA LINHAS
# ===================

# /////////////// IMPORTS

import re
from pytex.utils import sepIdent

# /////////////// CONFIG

sinal       = re.compile( r'\d*;;')
sepCampo    = re.compile( r' {2,}|\t+')
multilinha  = re.compile( r'^;;$', re.M)
linhaVazia  = re.compile( r'^\s*$')
formato     = None
ln          = '\n'


def montaCampos(linha, modelo):
	
	# Não usa linhas em branco como campos
	if linhaVazia.match(linha):
		return ''

	ident, campos = sepIdent(linha)

	campos = re.split(sepCampo,campos)

	linha_montada = modelo

	for campo in campos:
		linha_montada = sinal.sub(campo, linha_montada, 1)

	# Devolve identação e retira os sinais de campos restantes
	linha_montada = ident + re.sub(sinal, '', linha_montada)

	return linha_montada


def formataLinhas(tx, modo = None, limpa_vazio = False, escopo = None):

	juntaLinha = None	

	# Modelo com várias linhas
	if multilinha.search(tx):

		partes = multilinha.split(tx, 1)

		for i, parte in enumerate(partes):

			if sinal.search(parte):
				formato = partes.pop(i)
				tx = partes.pop()
	
		linhas = tx.splitlines()

		juntaLinha = ''

	# Modelo de linha única
	else:			

		linhas = tx.splitlines()

		for i, linha in enumerate(linhas):
			if re.search(sinal,linha):
				formato = linhas.pop(i)
				juntaLinha = ln
				break
	
	# -----------------------------------

	# Retira linhas em branco
	if limpa_vazio:
		linhas[:] = [ L for L in linhas if not linhaVazia.search(L) ]

	# Formata as linhas
	linhas[:] = [ montaCampos(L,formato) for L in linhas]

	return juntaLinha.join(linhas)