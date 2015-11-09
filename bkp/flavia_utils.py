
#####################
#	FLÁVIA UTILS	#
#####################

# Distribuição de um 'subset' sem dependências de 'André Utils' para Flávia

#################
#    IMPORTS    #
#################

import re, sublime, sublime_plugin

#################
#	ENTITIES	#
#################


# === Confiruração === #

# Modo de Operação
#
# Codifica		-> 0
# Decodifica	-> 1
# Resolve		-> 2
# Menu pergunta -> 3

MODO_INICIAL = 3

# === Tabela das 'Entities' === #

TABELA_ENTITIES = (

# =============== LETRAS

('Á','&Aacute;'),
('á','&aacute;'),
('Â','&Acirc;'),
('â','&acirc;'),
('À','&Agrave;'),
('à','&agrave;'),
('Ã','&Atilde;'),
('ã','&atilde;'),

('É','&Eacute;'),
('é','&eacute;'),
('Ê','&Ecirc;'),
('ê','&ecirc;'),

('Í','&Iacute;'),
('í','&iacute;'),
('Î','&Icirc;'),
('î','&icirc;'),

('Ó','&Oacute;'),
('ó','&oacute;'),
('Ô','&Ocirc;'),
('ô','&ocirc;'),
('Õ','&Otilde;'),
('õ','&otilde;'),

('Ú','&Uacute;'),
('ú','&uacute;'),
('Û','&Ucirc;'),
('û','&ucirc;'),

('Ç','&Ccedil;'),
('ç','&ccedil;'),

# =============== SÍMBOLOS

('Ø','&#8960;'),
('≤','&le;'),
('≥','&ge;'),
('°','&deg;')

) # ---- FIM de 'entities'

def trocaEntities(tx = '', modo = None):
	global TABELA_ENTITIES

	# Resolve -> 2
	if modo == 2:
		for ch in TABELA_ENTITIES:
			if re.search(ch[1],tx):
				modo = 1
				break
			else:
				modo = 0

	# Codifica -> 0
	if modo == 0:
		ini = 0
		fim = 1

	# Decodifica -> 1
	else:
		ini = 1
		fim = 0

	for ch in TABELA_ENTITIES:
		tx = tx.replace(ch[ini],ch[fim])
	return tx

#################################################################################

###############
#   TABELAS   #
###############

#def formataTabela(tx, linha_sep='\n', coluna_sep=' {2,}', modo=None):
def formataTabela(tx, linha_sep='\n', coluna_sep='\t', modo=None):

	#listras = (' class=""','') TODO !!!

	# Montando matriz

	linha_sep = re.compile(linha_sep)
	coluna_sep = re.compile(coluna_sep)

	matriz = linha_sep.split(tx)

	matriz[:] = [coluna_sep.split(tr) for tr in matriz]

	# Montando tabela

	tabela = ''
	log = 'log'
	listra_texto = (' class="trCinza"','')
	listra_conta = 0

	for linha in matriz:

		tr = ''

		for coluna in linha:
			coluna = coluna.strip()
			#tr += '\t\t<td>' + coluna + '</td>\n'
			tr += '<td>' + coluna + '</td>'
			tr = re.sub( r'<td>;(\d+) +', r'<td rowspan="\1">', tr)
			tr = re.sub( r'<td>;;(\d+) +', r'<td colspan="\1">', tr)

		#tabela += '\t<tr>\n' + tr + '\t</tr>\n'
		tabela += '<tr' + listra_texto[listra_conta] + '>' + tr + '</tr>\n'
		if(listra_conta==0):
			listra_conta = 1
		else:
			listra_conta = 0
	
	#tabela = '<table>\n' + tabela + '</table>\n'
	tabela = '<table class="tableProd centra">\n' + tabela + '</table>\n'

	# retorno
	return tabela

#################################################################################

# 'aplica' decide qual parte do texto será alterada
def aplica(vis,edit,func,modo=None):

	# Guarda posição inicial do cursor para voltar depois
	pos_antes = vis.rowcol(vis.sel()[0].b)

	# Sem seleção
	if vis.sel()[0].empty():

		# Mexe em tudo
		reg = sublime.Region(0,vis.size())

	# Com seleção
	else:
		# Mexe só na seleção
		reg = sublime.Region(vis.sel()[0].a,vis.sel()[0].b)

	# Altera o texto e devolve
	vis.replace(edit,reg,func(vis.substr(reg),modo=modo))

	# Volta o cursor na posição inicial ou mais próxima
	nova_linha = vis.line(vis.text_point(pos_antes[0],pos_antes[0]))
	comp_linha = nova_linha.b - nova_linha.a

	if comp_linha < pos_antes[1]:
		pos_linha = comp_linha
	else:
		pos_linha = pos_antes[1]

	vis.sel().clear()
	vis.sel().add(sublime.Region(vis.text_point(pos_antes[0],pos_linha)))


#################################################################################

# =================== #
#	-- COMANDOS --	  #
# =================== #


# CONVERTE 'HTML ENTITIES'

class ConvertEntitiesCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		global MODO_INICIAL
		modo = MODO_INICIAL

		# Mostra o menu opcional e muda o modo de operação
		def mudaModo(m):
			nonlocal modo
			modo = m

		if MODO_INICIAL == 3:
			self.view.show_popup_menu((
				'Codifica',
				'Decodifica',
				'Resolve',
				),mudaModo)

		aplica(self.view,edit,trocaEntities,modo)


# FORMATA TABELAS

class FormataTabelaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		aplica(self.view,edit,formataTabela)