
# ----------------------------------------------- #
#	APTOS
# ----------------------------------------------- #

import sublime, sublime_plugin, re, os

# =============================================================== #

def ul(lista):
	html = ''
	for li in lista:
		html += '<li>' + li + '</li>'
	html = '<ul>' +  html + '</ul>'
	return html

def titula(s, exceptions = []):
   word_list = re.split(' ', s)       #re.split behaves as expected
   final = [word_list[0].capitalize()]
   for word in word_list[1:]:
      final.append(word in exceptions and word or word.capitalize())
   return " ".join(final)

articles = ['a', 'an', 'of', 'the', 'is']

def tr(txt,lista):
	for par in lista:
		txt = txt.replace(par[0],par[1])
	return txt

listaAcentos = (

	('├â','Ã'),
	('├ü','Á'),

	('├ë','É'),
	('├ê','È'),

	('├ì','Í'),

	('├ô','Ó'),
	('├ö','Ô'),

	('├Ü','Ú'),

	('├ç','Ç'),
	
	('├æ','Ñ')
)

# Init apto
def newApto():
	return {
	'id':			None,
	'img':			'-',
	'file':			'-',
	'endereco':		'-',
	'edificio':		'-',
	'finalidade':	[],
	'categoria':	'-',
	'nome':			'-',
	'bairro':		'-',
	'desc':			'-',
	'lat':			'-',
	'lng':			'-',
	'valor_menor':	'-',
	'valor_maior':	'-',
	'social':		[],
	'interno':		[],
	'dormitorios':	0,
	'suites':		0,
	'garagens':		0
}

# Finalidade, Bairro, Dormitorios, Suites, Garagens, Valor, Categoria

# =============================================================== #

rootdir ='C:/Users/123/Documents/andre_bottan/Apartamento Bauru/busca_infos'

# IDs do BANCO =====================================================================================

banco_aptos = []

f = open(os.path.join(rootdir,'ids_aptos.txt'),'r',encoding="utf8")
txt_banco = f.read()
f.close()

banco_aptos = txt_banco.split('\n')
banco_aptos[:] = [ apto.split(';') for apto in banco_aptos ]

# LISTAGEM DE LOCAÇÃO =====================================================================================

lista_locacao = []

f = open(os.path.join(rootdir,'listagemLocacao.txt'),'r',encoding="utf8")
txt_locacao = f.read()
f.close()

nomes_locacao = []
for tit in re.finditer('<span class="st_tit">\s*(.*?)\s*</span>',txt_locacao):
	nomes_locacao.append(tit.group(1))

desc_locacao = []
for tit in re.finditer('<span class="sp_chama">\s*(.*?)\s*</span>',txt_locacao):
	desc_locacao.append(tit.group(1))

valor_locacao = []
for tit in re.finditer('<span class="sp_preco">\s*(.*?)\s*</span>',txt_locacao):
	valor_locacao.append(tit.group(1))

for i in range(len(nomes_locacao)):
	apto = {
		'nome':nomes_locacao[i],
		'desc':desc_locacao[i],	
		'valor':valor_locacao[i],
	}
	lista_locacao.append(apto)

# LISTAGEM DE VENDAS =====================================================================================

lista_venda = []

f = open(os.path.join(rootdir,'listagemVenda.txt'),'r',encoding="utf8")
txt_venda = f.read()
f.close()

nomes_venda = []
for tit in re.finditer('<span class="st_tit">\s*(.*?)\s*</span>',txt_venda):
	nomes_venda.append(tit.group(1))

desc_venda = []
for tit in re.finditer('<span class="sp_chama">\s*(.*?)\s*</span>',txt_venda):
	desc_venda.append(tit.group(1))

valor_venda = []
for tit in re.finditer('<span class="sp_preco">\s*(.*?)\s*</span>',txt_venda):
	valor_venda.append(tit.group(1))


for i in range(len(nomes_venda)):
	apto = {
		'nome':nomes_venda[i],
		'desc':desc_venda[i],	
		'valor':valor_venda[i],
	}
	lista_venda.append(apto)

# ==========================================================================================

def filtraInfoAptos(aptos=[],listagem=[],tipoDir=''):

	raiz = os.path.join(rootdir,tipoDir)

	for subdir, dirs, files in os.walk(raiz):
		for file in files:
			f = open( os.path.join(subdir,file),'r', encoding="utf8")
			txt = f.read()
			f.close()

			# Init apto
			apto = newApto()

			# Arquivo
			apto['file'] = file
			
			# Nome
			apto['nome'] = tr( file[0:file.index('.')], listaAcentos )

			# Tipo
			apto['finalidade'].append(tipoDir)

			# Categoria
			apto['categoria'] = 'sem'

			# Coordenadas
			coord = re.search('latLng: ?\[(-?(?:\d|\.)+), ?(-?(?:\d|\.)+)]',txt)
			apto['lat']	= float(coord.group(1))
			apto['lng']	= float(coord.group(2))

			# Coordenadas
			coord = re.search('latLng: ?\[(-?(?:\d|\.)+), ?(-?(?:\d|\.)+)]',txt)
			apto['lat']	= float(coord.group(1))
			apto['lng']	= float(coord.group(2))

			for item in listagem:
				if apto['nome'] == item['nome']:

					# Bairro
					apto['bairro'] = re.search('^(.*?)\s*?-',item['desc']).group(1)

					# Descrição
					apto['desc'] = re.search('<div class="descricao">\s*(.*?)\s*</div>',txt,re.DOTALL).group(1)

					# Valores
					valores = list(re.finditer('\d+',item['valor'].replace('.','')))
					apto['valor_menor']	= valores[0].group(0)
					apto['valor_maior']	= valores[0].group(0)
					if len(valores) == 2:
						apto['valor_maior']	= valores[1].group(0)

			# Area Social
			sociais = re.finditer(
				'<li>\s*(.*?)\s*</li>',
				re.search('ficha-detalhes-areasocial(.*?)</div>',txt,re.DOTALL).group(0)
			)
			for item in sociais:
				apto['social'].append(item.group(1))

			# Area Interna
			internos = re.finditer(
				'<li>\s*(.*?)\s*</li>',
				re.search('ficha-detalhes-aptomodelo(.*?)</div>',txt,re.DOTALL).group(0)
			)
			for item in internos:
				apto['interno'].append(item.group(1))
			aptos.append(apto)

			# Dormitorios
			for item in apto['interno']:
				m = re.search('(\d+) dormit.rio',item)
				if m:
					apto['dormitorios'] = int(m.group(1))
					break

			# Suites
			for item in apto['interno']:
				m = re.search('(\d+) su.te',item)
				if m:
					apto['suites'] = int(m.group(1))
					break

			if apto['dormitorios'] == 0:
				apto['dormitorios'] = apto['suites']

			# Garagem
			for item in apto['interno']:
				m = re.search('(\d+) vagas',item)
				if m:
					apto['garagens'] = int(m.group(1))
					break
	return aptos

barra = '\n---------------------------------------------------------\n\n'

def soltaListas():

	ret = ''

	for apto in lista_locacao:
		ret += str(apto) + '\n'

	ret += barra

	for apto in lista_venda:
		ret += str(apto) + '\n'

	return ret

# =================================================================================

# codimovel, imgImagem, texDescricao, desValorEstimado, txtDetalhes, desLegenda, urlLinkDetalhe
# Finalidade, Bairro, Dormitorios, Suites, Garagens, Valor, Categoria

# =================================================================== #

def soltaAptos(aptos):

	p = '\t\t'
	ret = ''
	ret += '\nINFO APTOS' + barra

	for apto in aptos:
		ret += 'Arquivo:'		+ p + apto['file']				+ '\n\n'
		ret += 'ID:'			+ p + str(apto['id'])			+ '\n'
		ret += 'Imagem:'		+ p + str(apto['img'])			+ '\n'
		ret += 'Finalidade:'	+ p + str(apto['finalidade'])	+ '\n'
		ret += 'Categoria:'		+ p + apto['categoria']			+ '\n'
		ret += 'Nome:'			+ p + apto['nome']				+ '\n'
		ret += 'Bairro:'		+ p + apto['bairro']			+ '\n'
		ret += 'Desc:'			+ p + apto['desc']				+ '\n'
		ret += 'Latitude:'		+ p + str(apto['lat'])			+ '\n'
		ret += 'Longitude:'		+ p + str(apto['lng'])			+ '\n'
		ret += 'Valor menor:'	+ p + str(apto['valor_menor'])	+ '\n'
		ret += 'Valor maior:'	+ p + str(apto['valor_maior'])	+ '\n'
		ret += 'Dormitorios:'	+ p + str(apto['dormitorios'])	+ '\n'
		ret += 'Suites:'		+ p + str(apto['suites'])		+ '\n'
		ret += 'Garagens:'		+ p + str(apto['garagens'])		+ '\n\n'
		ret += 'Area Social:'	+ p + str(apto['social'])		+ '\n'
		ret += 'Area Interna:'	+ p + str(apto['interno'])		+ '\n'

		ret += barra

	return ret

# =================================================================== #

def montaQueryAptos(aptos):

	sql = ''

	for ap in aptos:
		sql +=	"UPDATE aptobauru_institucional.imovel SET\n"
		sql += "desResumo = \"" + str(ap['desc']) + '",\n'

		# sql += "desNome = \""			+ str(ap['nome'])			+ '",\n'
		# sql += "desFinalidade = \""		+ str(ap['finalidade'])		+ '",\n'
		# sql += "desCategoria = \""		+ str(ap['categoria'])		+ '",\n'
		# sql += "desEdificio = \""		+ str(ap['edificio'])		+ '",\n'
		# sql += "desBairro = \""			+ str(ap['bairro'])			+ '",\n'
		# sql += "texDescricao = \""		+ str(ap['desc'])			+ '",\n'
		# sql += "desLatitude = \""		+ str(ap['lat'])			+ '",\n'
		# sql += "desLongitude = \""		+ str(ap['lng'])			+ '",\n'
		# sql += "texEndereco = \""		+ str(ap['endereco'])		+ '",\n'
		# sql += "intValorMenor = \""		+ str(ap['valor_menor'])	+ '",\n'
		# sql += "intValorMaior = \""		+ str(ap['valor_maior'])	+ '",\n'
		# sql += "txtDescSocial = \""		+ ul(ap['social'])			+ '",\n'
		# sql += "txtDescInterno = \""	+ ul(ap['interno'])			+ '",\n'
		# sql += "intDormitorios = \""	+ str(ap['dormitorios'])	+ '",\n'
		# sql += "intSuites = \""			+ str(ap['suites'])			+ '",\n'
		# sql += "intGaragens = \""		+ str(ap['garagens'])		+ '"\n'

		sql +=  "WHERE codimovel = \"" + str(ap['id']) + "\";"
		sql +=  '\n\n'

	return sql
	
# =================================================================== #

vendas  = filtraInfoAptos([],lista_venda,'venda')
locas	= filtraInfoAptos([],lista_locacao,'locacao')

nomesVenda = [ apto['nome'] for apto in vendas ]
nomesLoca  = [ apto['nome'] for apto in locas ]

nomesVendaLoca	=	[ n for n in nomesVenda if n in nomesLoca ]
nomesSoVenda	=	[ n for n in nomesVenda if n not in nomesLoca ]
nomesSoLoca		=	[ n for n in nomesLoca if n not in nomesVenda ]

Todos = []

# for nome in nomesVendaLoca:
# 	for ap in vendas:
# 		if nome == ap['nome']:
# 			Todos.append(ap)
# 			break
# 
# for nome in nomesSoVenda:
# 	for ap in vendas:
# 		if nome == ap['nome']:
# 			ap['finalidade'] = "venda"
# 			Todos.append(ap)
# 			break

for nome in nomesSoLoca:
	for ap in locas:
		if nome == ap['nome']:
			ap['finalidade'] = "locação"
			Todos.append(ap)
			break

# for nome in nomesVendaLoca:
# 	for ap in Todos:
# 		if nome == ap['nome']:
# 			ap['finalidade'] = "venda,locação"
# 			Todos.append(ap)
# 			break

# nomesJuntos = nomesVendaLoca + nomesSoVenda + nomesSoLoca
# nomesBanco[:] = [ reg[1] for reg in banco_aptos ]
# nomesFora[:] = [ nome for nome in nomesJuntos if nome not in nomesBanco ]

for ap in Todos:

	for reg in banco_aptos:
		if ap['nome'] == reg[1]:
			ap['id'] = reg[0]
			continue

####################################################################################################

# ['ANAVILHANAS', 'ARAGUAIA', 'DANIELLE', 'MARANELLO', 'VIA PONTINA']

class InfoAptosCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		ret = ''
		ret += montaQueryAptos(Todos)
		#ret += str(nomesSoLoca)

		f = open(os.path.join(rootdir,'output.sql'),'w',encoding="utf8")
		f.write(ret)
		f.close()