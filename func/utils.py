
############### FUNÇÕES ÚTEIS ###############

# Funções que NÃO DEPENDEM do editor

import re

# Regex da identação
reIdent = re.compile(r'^\s*')


# Retorna a posição do término da primeira identação de um texto (linha)
def posIdent(tx):
	return re.match(reIdent,tx).end(0)


# Retorna dupla (identação, texto)
def sepIdent(tx):
	p = posIdent(tx)
	return tx[:p], tx[p:]


# Retorna a parte de identação do texto
def txIdent(tx):
	p = posIdent(tx)
	return tx[:p] if p == 0 else ''


def indices(tx, sep, completa = False):
	if (type(sep) is str):
		sep = re.compile(sep)

	inds = [match.start() for match in sep.finditer(tx)]
	
	if completa and len(inds) == 0:
		# inds = [0,len(tx)]
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
def resolveModo(argInfo):

	arqNome, tx, pos = argInfo

	import os.path

	# Init do modo
	modo = {
		'modo':   None,
		'dirImg': None,
		'ext':    None,
		'match':  None
	}

	# Extensão do nome do arquivo
	modo['ext'] = os.path.splitext(arqNome)[1]


	# Extensão TXT
	if re.match(
		r'\.txt',
		modo['ext'], re.I
	):
		modo['modo'] = 'texto'
		return modo


	# Extensão JS
	'''
	if re.match(
		r'\.js',
		modo['ext'], re.I
	):
		modo['modo'] = 'javascript'
		return modo
	'''


	# Extensão PY
	if re.match(
		r'\.py',
		modo['ext'], re.I
	):
		modo['modo'] = 'python'
		return modo


	# Extensões CSS, SCSS e SASS
	if re.match(
		r'\.(css|scss|sass)',
		modo['ext'], re.I
	):
		modo['modo']	 = 'css_arq'
		modo['dirImg'] = '../img/'
		return modo


	# Extensões HTML, HTM, PHTML, ASP e PHP
	if re.match(
		r'\.(htm|html|phtml|php|asp|js|jsx)',
		modo['ext'], re.I
	):

		modo['dirImg'] = 'img/'
		
		# !!! TODO: Dentro do html
		# pos = editor.posCursor(vis)
		# tx  = pegaTextoTodo(vis)

		# Checa se está em um trecho de CSS ou PHP, dentro de um HTML
		reTipos = (
			( 'css_tag',  re.compile(r'<style.*?>(.*?)</style>', re.S)),
			( 'css_attr', re.compile(r'style="(.*?)"', re.S)),
			( 'php',	  re.compile(r'<\?php(.*?)\?>', re.S))
		)

		for tipo in reTipos:
			for m in tipo[1].finditer(tx):

				if m.start(1) <= pos <= m.end(1):
					modo['modo'] = tipo[0]
					modo['match'] = m
					break
				
				if modo['modo'] != None:
					break

		# Se não está em nenhum trecho especial, é HTML
		if modo['modo'] == None:
			modo['modo'] = 'html'

		return modo

	else: return modo

# ------------------------ /resolveModo
