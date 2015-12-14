
#########################
#	FUNÇÕES PARA HTML	#
#########################

import re, sublime
from func.utils import splitRe, indices, limpaTexto, posIdent
from func.config_html import *
from func.editor import *

# ------------------------------------------------------- #

# Pega ID e Classes
def pegaIdClasses(tx):
	ret = { 'id':None, 'classes':None }

	mId	   = re.finditer(r'#([a-zA-Z][_a-zA-Z0-9-]*)',tx)
	mClass = re.finditer(r'\.(-?[_a-zA-Z]+[_a-zA-Z0-9-]*)',tx)

	if mId:
		for Id in mId:
			ret['id'] = Id.group(1)
			break

	if mClass:
		ret['classes'] = []
		for classe in mClass:
			ret['classes'].append(classe.group(1))

	return ret

# Tira grupo casado por expressão do texto
def tiraGrupo(tx, match, ind = 0):
	return tx[:match.span(ind)[0]] + tx[match.span(ind)[1]:]

# ------------------------------------------------------- #

# Config init
config_html = ConfigHtml()

############### IDENTA ##############################
# Monta objeto-árvore

def identaHtml(tx='', inicIdent='', ident='\t', ln='\n', linear=None):

	re_abre	 = re.compile(r'<(?P<tag>([a-z]+[1-6]*)[^<>]*?)(?<=[^/])>(?P<txt>[^<]*)')
	re_fecha = re.compile(r'<\/(?P<tag>[a-z]+[1-6]*)>')
	re_auto	 = re.compile(r'<(?P<tag>[a-z]+)[^<>]*? \/>')

	seqIdent = [inicIdent]
	partes = []

	# Abre
	for item in re_abre.finditer(tx):
		partes.append({ 'tipo':'abre', 'm':item, 'nivel':None, 'cola':None })

	# Fecha
	for item in re_fecha.finditer(tx):
		partes.append({ 'tipo':'fecha', 'm':item, 'nivel':None, 'cola':None })

	# Autofecha
	for item in re_auto.finditer(tx):
		partes.append({ 'tipo':'auto', 'm':item, 'nivel':None, 'cola':None })

	# Ordena pela posição do começo do 'match'
	partes.sort(key=lambda parte: parte['m'].start())

	# Índices dos níveis
	cont_nivel = 0
	max_nivel = 0

	for p in partes:

		# Colagem
		for tag in config_html.tags:
			p['cola'] = str(tag.get('taglist'))
			p['cola'] = 'deu'

		# Nível
		if  p['tipo'] == 'fecha': cont_nivel -= 1
		p['nivel'] = cont_nivel
		if p['tipo'] == 'abre':
			cont_nivel += 1
			max_nivel += 1

	# Gera texto
	tx_identado = ''
	for p in partes:
		#tx_identado += inicIdent + ident * p['nivel'] + limpaTexto(p['m'].group('tag')) + p['cola']

		if p['tipo'] == 'abre':
			tx_identado += inicIdent + ident * p['nivel']

		tx_identado += limpaTexto(p['m'].group(0))
		
		#tx_identado += ln

	# Retorna texto identado
	return tx_identado

# ---------------------------- FIM de 'identa'

############### SPLIT TAGS ###############
# Monta objeto-árvore

def splitTags(tx,Tags):

	arvore = {
		# navegação - regex
		r';<': 'sobe',
		r';>': 'insere',
		r';;': 'concatena'
	}

	re_cortes = [corte for corte, tipo in arvore.items()]
	re_cortes.sort(key = lambda x: len(x), reverse = True)
	re_corta = '('+'|'.join(re_cortes)+')'

	cortes = []
	for corte in re.finditer(re_corta,tx):
		cortes.append((corte.start(),arvore.get(corte.group(0))))

	cortes = [(0,'comeca')] + cortes + [(len(tx),'termina')]

	for i, corte in enumerate(cortes):

		pos  = corte[0]
		tipo = corte[1]
		
		if tipo != 'termina':
		
			el = {
				'tag'		: None,
				'autofecha'	: None,
				'linear'	: None,
				'tipo'		: tipo,
				'pos'		: pos,
				'atribs'	: None,
				'subs'		: [],
				'repete'	: None,
				'txt'		: None
			}

			# Pega texto do elemento e limpa marcas de corte
			el['txt'] = re.sub(re_corta,'',tx[corte[0]:cortes[i+1][0]])

			for tag in Tags:

				matchTag = re.match(tag['re'],el['txt'])

				if matchTag:

					# Autofecha
					el['autofecha'] = tag.get('autofecha',False)

					# Linear
					el['linear'] = tag.get('linear',False)

					# Tag
					el['tag'] = re.sub(tag['re'],tag['tag'],matchTag.group(0))
					el['txt'] = tiraGrupo(el['txt'],matchTag); # limpa tag do texto

					# Repetição
					matchRepete = re.match(r'^\S*(~(\d+))',el['txt'])
					if matchRepete:
						el['repete'] = int(matchRepete.group(2)) # Segundo grupo é o dígito
						el['txt'] = tiraGrupo(el['txt'],matchRepete,1); # limpa dígito de repetição

					# === ATRIBUTOS ===
					el['atribs'] = []

					# IDs e Classses

					matchIdClass = re.match('^[\.#][a-zA-Z0-9-_.#]+',el['txt'])

					if matchIdClass:
						el['txt'] = tiraGrupo(el['txt'],matchIdClass); # limpa ids e classes

						id_class = pegaIdClasses(matchIdClass.group(0))

						if id_class['id']:
							el['atribs'].append(('id',id_class['id']))
						
						if id_class['classes']:
							el['atribs'].append(('class',' '.join(id_class['classes'])))

					el['atribs'] += tag.get('atribs',())
					break
		else:
			break # Termina
		
		if tipo == 'comeca':

			monta = []
			pais  = []
			atual = monta

		elif tipo == 'insere':
			
			pais.append(atual)
			atual = atual[-1]['subs']

		elif tipo == 'sobe':
			
			if len(pais) > 0:
				atual = pais[-1]
				del pais[-1]

		# Com repetição
		if el['repete']:
			for i in range(el['repete']):
				if (el['tipo'] == 'comeca' and i>0):
					el['tipo'] = 'concatena'
				atual.append(el)

		else: # Sem repetição
			atual.append(el)

	return monta
# ---------------------------- FIM de 'splitTags'

############### MONTA TAGS ##############################
# Monta tags identadas

def montaTags(arvore):

	seqFecha = []
	ret		 = ''

	def itera(colec):

		nonlocal seqFecha, ret

		for node in colec:

			if not (isinstance(node,dict) or isinstance(node,list)): continue

			if node['tag'] != None:
				txTag = '<' + node['tag']
			else:
				txTag = ''

			# Atributos
			if node['atribs']:
				for a in node['atribs']:
					txTag += ' {atr}="{val}"'.format(atr=a[0], val=a[1])

			# Fechamento da tag
			fechaTag = ''

			# Tags auto-fechantes
			if node['autofecha'] == True:
				txTag += ' />'
			
			# Fechamento normal
			else:
				if node['tag'] != None:
					txTag += '>'
					fechaTag = '</'+ node['tag'] +'>'

			# Se tiver texto dentro
			if node['txt']:
				txTag += limpaTexto(node['txt'])

			seqFecha.append(fechaTag)
			ret += txTag

			# Com filhos
			if len(node['subs']) > 0:
				itera(node['subs']) # RECURSÃO

			# Sem filhos
			ret += seqFecha.pop()

	# Executa montagem
	itera(arvore)

	# Retorna
	return ret.rstrip()

#------------------------------------------------------- fim 'monta'

############### HTML EXPANDE ##############################

def htmlExpande(tx,modo=None):

	pos_ident = posIdent(tx)

	# Tags montadas
	return identaHtml(
		tx = montaTags(
			splitTags(
				tx[pos_ident::],
				config_html.tags
			)
		),
		inicIdent = tx[0:pos_ident]
	)

#------------------------------------- fim 'htmlExpande'