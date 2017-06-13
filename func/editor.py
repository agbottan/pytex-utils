
############### FUNÇÕES DO EDITOR ###############

# Funções que DEPENDEM do editor
# Devem ser alteradas para portabilidade entre editores

import sublime, re

# --------------- Debug

# Barra Separadora
barra = '\n' + '#' * 80 + '\n'

def x(*args):
	ret = ''
	for tx in args:
		ret += str(tx)
	print(ret)


def X(*args):
	ret = ''
	for tx in args:
		ret += str(tx)
	return ret


def X_(*args):
	ret = ''
	for tx in args:
		ret += str(tx)
	sublime.message_dialog(ret)


def x_(*args):
	ret = ''
	for tx in args:
		ret += str(tx)
	ret += '\n'	
	print(ret)


def x__(*args):
	ret = ''
	for tx in args:
		ret += str(tx) + '\n'
	ret = barra + ret
	print(ret)


# !!! Fazer um que loga num arquivo de log aberto e abre se não tiver um

# ------------------------------


# Retorna o nome do arquivo ativo
def pegaNomeArquivoAtivo(vis):
	return vis.file_name()


# Retorna a posição do cursor, relativo ao começo do texto
def posCursor(vis):
	return vis.sel()[0].b


# Retorna a posição do cursor no texto, como 'linha' e 'coluna'
def coordCursor(vis):
	return vis.rowcol(posCursor(vis))


# Retorna limites da linha que contém o cursor
def linhaCursor(vis):
	return vis.line(posCursor(vis))


# Retorna a posição do cursor no texto da linha em que ele está
def posLinha(vis):
	return posCursor(vis) - linhaCursor(vis).a


# Manda o cursor para uma posição no texto da linha em que ele está
# Se o incremento for maior que o comprimento da linha, manda para o final da linha
def vaiPosLinha(vis, n=0):
	linha = linhaCursor(vis)
	pos = linha.a + n
	if pos > linha.b:
		pos = linha.b
	vaiCursor(vis,pos)


# Retorna uma referência à região selecionada
def regSel(vis):
	return sublime.Region(vis.sel()[0].a,vis.sel()[0].b)


# Retorna o texto da região selecionada
def pegaTextoSel(vis):
	return vis.substr(regSel(vis))


# Retorna todo o texto do arquivo
def pegaTextoTodo(vis):
	return vis.substr(sublime.Region(0,vis.size()))


# Retorna o texto da linha em que está o cursor
def pegaTextoLinha(vis):
	return vis.substr(vis.line(vis.sel()[0].a))


# Muda o texto da linha do cursor
def mudaLinha(vis, edit, tx):
	vis.replace(edit,linhaCursor(vis),tx)


# Muda o texto da seleção atual
def mudaSel(vis, edit, tx):
	vis.replace(edit,regSel(vis),tx)


# Manda o cursor para uma posição do texto
def vaiCursor(vis, pos):
	vis.sel().clear()
	vis.sel().add(sublime.Region(pos,pos))


# Retorna o cursor para a posição certa, de acordo com parâmetro
def voltaCursor(vis, pos_init, retorno_cursor=0):

	# 0 - Fim da linha
	if retorno_cursor == 0:
		vaiCursor(vis,vis.line(posCursor(vis)).b)

	# 1 - Posição inicial ou mais próxima
	elif retorno_cursor == 1:

		nova_linha = vis.line(vis.text_point(pos_init[0],pos_init[0]))
		comp_linha = nova_linha.b - nova_linha.a

		if comp_linha < pos_init[1]:
			pos_linha = comp_linha
		else:
			pos_linha = pos_init[1]

		vaiCursor(vis,vis.text_point(pos_init[0],pos_linha))

	# 2 - Busca info na linha e se adpta !!!
	else: return


# Retorna informações do arquivo ativo para resolver o modo de operação
def pegaInfoModo(vis):

	arqNome = pegaNomeArquivoAtivo(vis) # Nome do arquivo
	if not arqNome:
		arqNome = ''

	arqTx = pegaTextoTodo(vis) 	  # Texto do arquivo
	arqPosCursor = posCursor(vis) # Posição do cursor no texto

	return (arqNome, arqTx, arqPosCursor)


# Padrão para aplicação de alteração no texto
def aplica(
	edit, vis, func,

	argList = {},
	retorno_cursor = 0,
	modo = None
):

	# Se não foi passada a 'view', considera a última view ativa
	if vis == None:
		vis = sublime.active_window().active_view()

	# Guarda posição inicial do cursor para voltar depois
	pos_antes = coordCursor(vis)

	# Resolve se há seleção
	sel_vazia = pegaTextoSel(vis) == ''
	# TODO !!! e se é 'multiline'

	argList['tx']			= pegaTexto(vis)
	argList['modo'] 	= modo
	argList['escopo']	= vis.scope_name(posCursor(vis))

	linhaComeco = linhaCursor(vis) # TODO !!! VERIFICAR UTILIDADES

	# Aplica a função de transformação
	ret = func(**argList)

	# seleção vazia
	if sel_vazia:
		mudaLinha(vis,edit,ret)

	# seleção com texto
	else:
		mudaSel(vis,edit,ret)

	# Volta cursor na posição inicial
	voltaCursor( vis=vis, pos_init=pos_antes, retorno_cursor=retorno_cursor)

# ------------------------ /- aplica


# Pega texto seleção e, se esta estiver vazia, da linha
def pegaTexto(vis=None):

	tx 	= ''

	if vis == None:
		vis = sublime.active_window().active_view()

	# Guarda posição inicial do cursor para voltar depois
	pos_antes = coordCursor(vis)

	if vis.sel()[0].empty():
		tx = pegaTextoLinha(vis)
	else:
		tx = pegaTextoSel(vis)
	return tx


# Pega texto seleção e, se esta estiver vazia, da linha
# def getTexto(vis=None):
# 
# 	tx 	= ''
# 
# 	if vis == None:
# 		vis = sublime.active_window().active_view()
# 
# 	# Guarda posição inicial do cursor para voltar depois
# 	pos_antes = coordCursor(vis)
# 
# 	if vis.sel()[0].empty():
# 		tx = pegaTextoLinha(vis)
# 	else:
# 		tx = pegaTextoSel(vis)
# 	return tx

# ------------------------ /- Get texto


# Bota texto
# def botaTexto(edit, vis=None, tx=''):
# 
# 	# Seleção vazia
# 	if sel_vazia:
# 		mudaLinha(vis,edit,tx)
# 
# 	# Seleção com texto
# 	else:
# 		mudaSel(vis, edit, tx)
# 
# 	# Volta cursor na posição inicial
# 	voltaCursor( vis=vis, pos_init=pos_antes, retorno_cursor=retorno_cursor)

# ------------------------ /- Bota texto