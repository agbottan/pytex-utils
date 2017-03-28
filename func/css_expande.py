
#####################
#   CSS > EXPANDE   #
#####################

import re, sublime
from func.utils import splitRe, posIdent
from func.editor import *
from func.css_config import ConfigCss


# ------------------------------------------------------- #

def pegaFonte():
	# !!! TODO !!! -> Pegar a fonte por projeto
	return ''

reCor = re.compile(r'(?:[0-9a-fA-F]{3}){1,2}')
def pegaCor(P):
	cores = reCor.findall(P)
	cores[:] = ['#'+cor for cor in cores]
	return cores

# Regex que acha os números
# unids = 'px|%|rem|em|vw|vh|cm|mm'
unidades = ('px','%','rem','em','vw','vh','cm','mm')
unidadesAtalho = ('=','m')
reNum = re.compile(r'(-?[\d,\.a]+(' + '|'.join(unidades + unidadesAtalho) + ')?)')

def pegaNumeros(P, limite=None, completaUnidades=True, unidadePadrao='px'):

	nums = reNum.findall(P)
	nums[:] = [n[0] for n in nums] # Reduz para o primeiro subgrupo apenas
	nums[:] = [re.sub('a','auto',n) for n in nums] # 'a' vira 'auto'

	if limite: nums = nums[:limite]

	if completaUnidades:
		for i, n in enumerate(nums):

			# Tira '0' à esquerda
			n = re.sub(r'^0(\d+)','\g<1>',n)

			# Põe a unidade padrão
			n = re.sub(r'^(-?[\d,.]+)$','\g<1>'+unidadePadrao,n)

			# 'm' vira 'em'
			n = re.sub(r'^(-?[\d,.]+)m$','\g<1>em',n)

			# '=' vira '%'
			n = re.sub(r'^(-?[\d,.]+)=$','\g<1>%',n)

			# Transforma '0 unid' em '0'
			n = re.sub(r'^0('+ '|'.join(unidades) +')$','0',n)

			# 'A.Bpx' vira 'Apx'
			n = re.sub(r'^(-?\d+)[.,]\d+px$','\g<1>px',n)

			nums[i] = n

	return nums
	
def limpaNumeros(P):
	nums = reNum.findall(P)
	nums[:] = [n[0] for n in nums] # Reduz para o primeiro subgrupo apenas
	for n in nums:
		P = re.sub(n,'',P)
	return P


############### EXPANSOR DE CSS ###############

def cssExpande(tx, modo=None):

	# Converte tuplas de prop-val em string
	def propsMonta(propsReserva, ident='', propsSepara='', valSepara=': '):
		return propsSepara.join([
			ident + p[0] + valSepara + p[1] + ';' for p in propsReserva
		])

	ret = ''

	# Aplica 'cssLista' dentro das chaves '{}'
	if re.search(r'{.+}',tx):

		def cb(tx):

			nonlocal modo

			lista = cssLista(
				tx = tx,
				dirImg = modo['dirImg']
			)
			return propsMonta(
				propsReserva = lista,
				ident = '',
				propsSepara = ' '
			)

		tx = re.sub(r'(?<={).*?(?=})', cb, tx)	# aplica 'cssLista' e 'propsMonta' dentro das chaves '{}'
		tx = re.sub(r'{(?=\S)','{ ', tx)				# põe espaço depois de '{'
		tx = re.sub(r'(?<=\S)}',' }', tx)				# põe espaço antes de '}'
		ret = tx

	# Aplica 'cssLista' se não houver as duas chaves '{}'
	else:
		i = posIdent(tx)
		lista = cssLista(
			tx = tx[i::],
			dirImg = modo['dirImg']
		)
		ret = propsMonta(
			propsReserva = lista,
			ident = tx[0:i],
			propsSepara = '\n'
		)

	return ret

#--------------------------------- fim de 'cssExpande'

############### CSS SUB ##############################

def cssLista(tx, dirImg=''):

	patCss = ConfigCss()

	if type(tx) != str:
		tx = tx.group(0)
	
	Props = splitRe(tx, patCss.reCss)

	fim_prop = None
	retProps = []
	
	if Props == None:
		return ''.join(retProps)

	for iniProp in Props:
		
		# ========================== Propriedade feita, ignora...

		if patCss.reIgnora.match(iniProp):

			iniProp = iniProp.replace(';','')						# Retira o ';' no final da propriedade
			iniProp = re.sub(r'\s+$', '', iniProp)			# Apaga os espaços em branco no final da propriedade
			iniProp = re.split(r'\s*:\s*', iniProp, 1)	# Corta pelo ':' e faz o par
			iniProp = tuple(iniProp)										# Transforma a lista em tupla
			retProps.append(iniProp)										# Adiciona na lista
			continue
		
		for prop in patCss.props:

			ind = prop['nome']
			pat = prop['regex']

			# ========================== Sem expansão, ignora...
			m = re.match(pat,iniProp)
			if m == None:
				continue

			ini_prop = m.group(0)
			ini_vals = iniProp[len(ini_prop):]
			
			# ========================== DISPLAY
			if ind == 'Display':
				
				rel_vals = { 'b':'block', 'f':'flex', 'n':'none', 'i':'inline', 'l':'inline-block' }

				val = rel_vals.get(ini_prop[-1],'')

				retProps.append(('display',val))
				
			# ========================== POSITION
			if ind == 'Position':
				
				rel_vals = { 'a':'absolute', 'r':'relative', 'f':'fixed', 's':'static', 'k':'sticky' }

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
					'hw':['height','width'],
					'q':['width','height']
				}
				
				props = rel_props.get(ini_prop,'')

				if iniProp[0] == 'q':
					retProps += list(zip(props,(numeros[0],numeros[0])))
				else:
					retProps += list(zip(props,numeros))

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
					'm':'family',
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
					val = pegaFonte()

				else:
					if( len(ini_prop) == 3 ):
						val = subPropsVals[1].get(ini_prop[2],'')
				
				retProps.append(('font-' + subProp, val))
			
			# ========================== BORDER
			if ind == 'Border':
				
				rel_subProps_vals = {
					'd':'dotted',
					'r':'radius',
					's':'solid'
				}
				
				subPropsVals = rel_subProps_vals.get(ini_prop[1],None)
				
				subProp = ''
				if(type(subPropsVals) is str):
					subProp = subPropsVals
				else:
					subProp = subPropsVals[0]
					
				val = numeros = ''
				
				if(subProp == 'radius'):
					numeros = pegaNumeros(iniProp)
					iniProp = limpaNumeros(iniProp)
					val = numeros[0]
				else:
					if( len(ini_prop) == 3 ):
						val = subPropsVals[1].get(ini_prop[2],'') # !!!
				
				retProps.append(('border-' + subProp, val))

			# ========================== BACKGROUND
			if ind == 'Background':
				
				vImg = vCor = vPox = vPoy = vAtt = vRep = ''
				
				# -------------------------- background
				
				if	 ini_prop[-1] == 'a':	fim_prop = 'background-attachment'
				elif ini_prop[-1] == 'i':	fim_prop = 'background-image'
				elif ini_prop[-1] == 'p':	fim_prop = 'background-position'
				elif ini_prop[-1] == 'r':	fim_prop = 'background-repeat'
				elif ini_prop[-1] == 'c':	fim_prop = 'background-color'
				elif ini_prop[-1] == 's':	fim_prop = 'background-size'
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

#--------------------------------- fim de 'cssLista'
