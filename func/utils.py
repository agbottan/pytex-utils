
############### FUNÇÕES ÚTEIS ###############

# Funções que NÃO DEPENDEM do editor

import re, func.editor

# Retorna a posição do término da primeira identação de um texto (linha)
def posIdent(tx):
	reIdent = re.compile(r'^\s*')
	return re.match(reIdent,tx).end(0)


# Retorna a parte de identação do texto
def txIdent(tx):
	pos = posIdent(tx)
	if pos == 0:
		return ''
	else:
		return tx[0::pos]


def indices(tx, sep, completa = False):
	if (type(sep) is str):
		sep = re.compile(sep)

	inds = [match.start() for match in sep.finditer(tx)]
	
	if completa and len(inds) == 0:
		#inds = [0,len(tx)]
		inds = [len(tx)] # !!! TODO: MELHORAR - POR CHECAGEM ANTES !!!
	
	return inds


def splitPosic(tx,pos):

	ret = []

	if len(pos) == 0:
		return

	if pos[0] != 0:
		pos.insert(0,0)

	if pos[-1] != len(tx):
		pos.append(len(tx))

	for i in range(len(pos)):
		if i+1 >= len(pos):
			break
		ret.insert(i,tx[pos[i]:pos[i+1]])

	return ret


def splitRe(tx,regex):
	return splitPosic(tx,indices(tx,regex))


def indicePosic(ponteiro,marcas):
	indice = 0
	for i, p in enumerate(marcas):
		if p < ponteiro: indice = i
	return indice


def limpaTexto(tx):
	tx = re.sub('\n',' ',tx)
	tx = re.sub('\s+',' ',tx)
	tx = tx.strip()
	return tx


# Decide e retorna o modo de operação e informações sobre ele
def pegaModo(arqNome):

	import os.path
	ret = {
		'modo':None,
		'dirImg':None,
		'ext':None,
		'match':None
	}

	ext = os.path.splitext(arqNome)[1]
	ret['ext'] = ext 

	# Extensão 'css'
	if re.match( r'\.s?css', ret['ext'], re.I ):
		ret['modo']		= 'css_arq'
		ret['dirImg']	= '../img/'
		return ret

	# Extensão 'html' e 'php'
	if re.match( r'\.php|\.p?html?|\.asp', ret['ext'], re.I ):
		ret['dirImg'] = 'img/'
		
		# Dentro do html
		pos = posCursor(vis)
		tx	= pegaTextoTodo(vis)

		reTipos = (
			( 'css_tag',	re.compile(r'<style.*?>(.*?)</style>',re.S)),
			( 'css_attr',	re.compile(r'style="(.*?)"',re.S)),
			( 'php',		re.compile(r'<\?php(.*?)\?>',re.S))
		)

		for tipo in reTipos:
			for m in tipo[1].finditer(tx):

				if m.start(1) <= pos <= m.end(1):
					ret['modo'] = tipo[0]
					ret['match'] = m
					break
				
				if ret['modo'] != None:
					break

		if ret['modo'] == None:
			ret['modo'] = 'html'

		return ret
	else: return ret

# ------------------------ -pegaModo
