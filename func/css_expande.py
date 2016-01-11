
#####################
#   CSS > EXPANDE   #
#####################

import re, sublime
from func.utils import splitRe, posIdent
from func.editor import *

# ------------------------------------------------------- #

def pegaFonte():
	# !!! TODO !!! -> Pegar a fonte por projeto
	return 'Arial'

reCor = re.compile(r'(?:[0-9a-fA-F]{3}){1,2}')
def pegaCor(P):
	cores = reCor.findall(P)
	cores[:] = ['#'+cor for cor in cores]
	return cores

reNum = re.compile(r'a|(-?[\d,\.]+(px|=|%|rem|em|m|vw|vh|cm|mm)?)')

def pegaNumeros(P, unidades=True):
	numeros = reNum.findall(P)
	numeros[:] = [n[0] for n in numeros] # Reduz para o primeiro subgrupo apenas
	if unidades:
		numeros[:] = [re.sub(r'^(-?[\d,\.]+)$','\g<1>px',n) for n in numeros] # Põe unidade 'px'
		numeros[:] = [re.sub(r'^(-?[\d,\.]+)m$','\g<1>em',n) for n in numeros] # 'm' vira 'em'
		numeros[:] = [re.sub(r'^(-?[\d,\.]+)=$','\g<1>%',n) for n in numeros] # '=' vira '%'
		numeros[:] = [re.sub(r'^0.+$','0',n) for n in numeros] # Transforma '0 unid' em '0'
	return numeros
	
def limpaNumeros(P):
	numeros = reNum.findall(P)
	numeros[:] = [n[0] for n in numeros] # Reduz para o primeiro subgrupo apenas
	for n in numeros: P = re.sub(n,'',P)
	return P


############### EXPANSOR DE CSS ###############

# Converte tuplas de 'prop-val' em string
#retProps[:] = [ p[0] + ': ' + p[1] + ';' for p in retProps]
#return re.sub(' +',' ',' '.join(retProps))
#return ident + ('\n'+ident).join(retProps)

def cssExpande(tx, modo=None):

	# Converte tuplas de prop-val em string
	def propsMonta(propsLista, ident=' ', ln=''):
		montaLista[:] = [ ident + p[0] + ': ' + p[1] + ';' for p in propsLista]
		ret = ln.join(montaLista)
		ret = re.sub(' +',' ',ret) # Junta espaços em um só
		return ret

	def cb(tx):
		nonlocal modo
		lista = cssSub(
			tx = tx,
			dirImg = modo['dirImg']
		)
		ret = propsMonta(propsLista=lista)

	if re.search('{.+}',tx):
		tx = re.sub(r'(?<={).*?(?=})',cb,tx)	# aplica 'cssSub' dentro das chaves '{}'
		tx = re.sub(r'{(?=\S)','{ ',tx)			# põe espaço depois de '{'
		tx = re.sub(r'(?<=\S)}',' }',tx)		# põe espaço antes de '}'
	else:
		# aplica 'cssSub' se não houver chaves '{}'
		i = posIdent(tx)
		tx = cssSub(
			tx 		= tx[i::],
			ident 	= tx[0:i],
			dirImg 	= modo['dirImg']
		)
	return tx

#--------------------------------- fim de 'cssExpande'

############### CSS SUB ##############################

def cssSub(tx, ident='', dirImg=''):

	if type(tx) != str: tx = tx.group(0)

	patCss = (
		# Propriedades montadas - não sofre alteração
		( 'ignora', r'\b(display|position|z-index|left|top|right|bottom|float|clear|margin|padding|(min-|max-)?width|(min-|max-)?height|line-height|border|text|font|color|background|overflow)[^;]*;' ), # ignora...			
		# Chamadas para montar propriedades
		( 'Display',		r'\bd[bnil]\b'			),	# Display
		( 'Position',		r'\bp[arfs]\b'			),	# Position
		( 'Z-index',		r'\bz\s*\d+\b'			),	# Z-index
		( 'Float',			r'\bf[lrn]\b'			),	# Float
		( 'Clear',			r'\bc[lrbn]\b'			),	# Clear
		( 'Box',			r'\bbs[b]?\b'			),	# Box-sizing
		( 'Cursor',			r'\bcu[dp]\b'			),	# Cursor
		( 'Overflow',		r'\bo[xy]?[hsv]\b'		),	# Overflow
		( 'Color',			r'\bco\b'				),	# Color
		( 'Width-Height',	r'\b(wh?|hw?)'			),	# Width - Height
		( 'Margin-Padding',	r'\b(m|pd)[trbl]?'		),	# Margin - Padding
		( 'Text',			r'\bt[adit][cjlnoru]?'	),	# Text
		( 'Font',			r'\bf[fsw][abn]?'		),	# Font
		( 'Border',			r'\bbd\b'				),	# Border
		( 'Background',		r'\bbg[aiprc]?\b'		) 	# Background		
	)

	reCss = ''
	for item in patCss:
		reCss += item[1] + '|'
	
	reCss = r'(' + reCss[:-1] + r')'
	
	reCss = re.compile(reCss)
	
	Props = splitRe(tx,reCss)
	
	fim_prop = None
	retProps = []
	
	if Props == None:
		return ''.join(retProps)

	for iniProp in Props:
		
		# ========================== Propriedade feita, ignora...
		pronta = re.match(patCss[0][1],iniProp)
		if pronta:
			retProps.append(iniProp)
			continue
		
		for (ind,pat) in patCss[1:]:

			# ========================== Sem expansão, ignora...
			m = re.match(pat,iniProp)
			if m == None:
				continue

			ini_prop = m.group(0)
			ini_vals = iniProp[len(ini_prop):]
			
			# ========================== DISPLAY
			if ind == 'Display':
				
				rel_vals = { 'b':'block', 'n':'none', 'i':'inline', 'l':'inline-block' }

				val = rel_vals.get(ini_prop[-1],'')

				retProps.append(('display',val))
				
			# ========================== POSITION
			if ind == 'Position':
				
				rel_vals = { 'a':'absolute', 'r':'relative', 'f':'fixed', 's':'static' }

				val = rel_vals.get(ini_prop[-1],'')

				retProps.append(('position',val))

			# ========================== Z-INDEX
			if ind == 'Z-index':

				val = pegaNumeros(ini_prop,False)[0]

				retProps.append(('z-index',val))

			# ========================== FLOAT
			if ind == 'Float':
				
				rel_vals = { 'l':'left', 'r':'right', 'n':'none' }

				val = rel_vals.get(ini_prop[-1],'')
				
				retProps.append(('float',val))
				
			# ========================== CLEAR
			if ind == 'Clear':
				
				rel_vals = { 'l':'left', 'r':'right', 'b':'both', 'n':'none' }

				val = rel_vals.get(ini_prop[-1],'')
				
				retProps.append(('clear',val))

			# ========================== BOX-SIZING
			if ind == 'Box':
				
				rel_vals = { 'b':'border-box' }

				val = rel_vals.get(ini_prop[-1],'border-box')
				
				retProps.append(('box-sizing',val))
				
			# ========================== CURSOR
			if ind == 'Cursor':
				
				rel_vals = { 'd':'default', 'p':'pointer' }

				val = rel_vals.get(ini_prop[-1],'')
				
				retProps.append(('cursor',val))
				
			# ========================== OVERFLOW
			if ind == 'Overflow':
				
				rel_vals = { 'a':'auto', 'h':'hidden', 's':'scroll', 'v':'visible' }

				val = rel_vals.get(ini_prop[-1],'')
				
				coord = ''
				if len(ini_prop) == 3:
					coord = '-' + ini_prop[1]
				
				retProps.append(('overflow' + coord,val))

			# ========================== COLOR
			if ind == 'Color':

				val = pegaCor(ini_vals)
				
				retProps.append((
					'color',
					'='.join(val)
				))
				
			# ========================== WIDTH - HEIGHT
			if ind == 'Width-Height':
			
				numeros = pegaNumeros(iniProp)
				iniProp = limpaNumeros(iniProp)
				
				rel_props = {
					'w':['width'],
					'h':['height'],
					'wh':['width','height'],
					'hw':['height','width']
				}
				
				props = rel_props.get(ini_prop,'')
				retProps.append(list(zip(props,numeros)))

			# ========================== MARGIN - PADDING
			if ind == 'Margin-Padding':
				
				numeros = pegaNumeros(iniProp)
				iniProp = limpaNumeros(iniProp)
				
				rel_props		= { 'm':'margin', 'p':'padding' }
				rel_subProps	= { 't':'top', 'r':'right', 'b':'bottom', 'l':'left' }
				
				val = ''
				subProp = ''
				prop	= rel_props.get(ini_prop[0],'')
				subProp	= rel_subProps.get(ini_prop[-1],'')
				if( subProp != '' ): subProp = '-' + subProp
				
				retProps.append((
					prop + subProp,
					' '.join(numeros)
				))
			
			# ========================== TEXT
			if ind == 'Text':
				
				rel_subProps_vals = {
					'a':('align',{ 'c':'center', 'j':'justify', 'l':'left', 'r':'right' }),
					'd':('decoration',{ 'n':'none', 'o':'overline', 'u':'underline' }),
					'i':'indent',
					't':('transform',{ 'l':'lowercase', 'c':'capitalize', 'u':'uppercase' })
				}
				
				subPropsVals = rel_subProps_vals.get(ini_prop[1],None)
				
				subProp = ''
				if(type(subPropsVals) is str):
					subProp = subPropsVals
				else:
					subProp = subPropsVals[0]
					
				val = numeros = ''
				
				if(subProp == 'indent'):
					numeros = pegaNumeros(iniProp)
					iniProp = limpaNumeros(iniProp)
					val = numeros[0]
				else:
					if( len(ini_prop) == 3 ):
						val = subPropsVals[1].get(ini_prop[2],'')
				
				retProps.append(('text-' + subProp, val))

			# ========================== FONT
			if ind == 'Font':
				
				rel_subProps_vals = {
					'f':'family',
					's':'size',
					'w':('weight',{ 'b':'bold', 'n':'normal' })
				}
				
				subPropsVals = rel_subProps_vals.get(ini_prop[1],'')
				
				subProp = ''
				if(type(subPropsVals) is str):
					subProp = subPropsVals
				else:
					subProp = subPropsVals[0]
					
				val = numeros = ''
				
				if(subProp == 'size'):
					numeros = pegaNumeros(iniProp)
					iniProp = limpaNumeros(iniProp)
					val = numeros[0]
					
				elif(subProp == 'family'):
					if( len(ini_prop) == 3 ):
						val = pegaFonte()
					
				else:
					if( len(ini_prop) == 3 ):
						val = subPropsVals[1].get(ini_prop[2],'')
				
				retProps.append(('font-' + subProp, val))
			
			# ========================== BACKGROUND
			if ind == 'Background':
				
				vImg = vCor = vPox = vPoy = vAtt = vRep = ''
				
				# -------------------------- background
				
				if ini_prop[-1] == 'a':		fim_prop = 'background-attachment'
				elif ini_prop[-1] == 'i':	fim_prop = 'background-image'
				elif ini_prop[-1] == 'p':	fim_prop = 'background-position'
				elif ini_prop[-1] == 'r':	fim_prop = 'background-repeat'
				elif ini_prop[-1] == 'c':	fim_prop = 'background-color'
				else: fim_prop = 'background'
				
				if fim_prop in ['background','background-image']:
				
					# -------------------------- imagem
					
					vImg = re.search(r'\w+\.(png|jpg|gif)',ini_vals)
					if vImg:
						vImg = vImg.group(0)
						iniProp = re.sub(vImg,'',iniProp)
						vImg = 'url("'+ dirImg + vImg +'")'
					else:
						vImg = ''
				
				if fim_prop in ['background','background-color']:
				
					# -------------------------- color
					
					vCor = re.search(r'(\d|a|b|c|d|e|f){3,6}',ini_vals,re.I) #???
					if vCor:
						vCor = vCor.group(0)
						ini_vals = re.sub(vCor,'',ini_vals)
						vCor = '#' + vCor
					else:
						vCor = ''
				
				if fim_prop in ['background','background-position']:
				
					# -------------------------- position x
				
					if ini_vals.find('l')	!= -1: vPox = 'left'
					elif ini_vals.find('r') != -1: vPox = 'right'
				
					# -------------------------- position y
				
					if ini_vals.find('t')	!= -1: vPoy = 'top'
					elif ini_vals.find('b') != -1: vPoy = 'bottom'
				
				if fim_prop in ['background','background-repeat']:
				
					# -------------------------- repeat
				
					if ini_vals.find('n')	!= -1: vRep = 'no-repeat'
					elif ini_vals.find('re')!= -1: vRep = 'repeat'
					elif ini_vals.find('x') != -1: vRep = 'repeat-x'
					elif ini_vals.find('y') != -1: vRep = 'repeat-y'
				
				if fim_prop == 'background':
				
					# -------------------------- genéricas
					
					if vImg == '': vImg = 'url("'+ dirImg +'")'
					if vCor == '': vCor = ''
					if vPox == '': vPox = 'left'
					if vPoy == '': vPoy = 'top'
					if vAtt == '': vAtt = ''
					if vRep == '': vRep = 'no-repeat'
				
				# Retorna
				fim_vals = ( vImg, vCor, vPox, vPoy, vAtt, vRep )
				fim_vals = ' '.join(fim_vals)
				fim_vals = fim_vals.strip(' ')

				retProps.append((fim_prop, fim_vals))
			
			#- 'switch'
		#- 'for' dos 'patterns'
	#- 'for' das 'Props'
	return retProps

#--------------------------------- fim de 'cssSub'
