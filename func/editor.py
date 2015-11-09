
############### FUNÇÕES DO EDITOR ###############

import sublime, re

# ================================================================= DEPENDENTE do editor

# !!! DEBUG !!!

def x(*args):
	ret = ''
	for tx in args:
		# ret += str(tx) + '\n'
		ret += str(tx)
	print(ret)

def x_(*args):
	ret = ''
	for tx in args:
		ret += str(tx) + '\n'
	sublime.message_dialog(ret)


# Retorna o modo de operação e informações
def pegaModo(vis):

	import os.path
	ret = {
		'modo':None,
		'dirImg':None,
		'ext':None,
		'match':None
	}

	ext = os.path.splitext(vis.file_name())[1]
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

# ------------------------ FIM de modo

# Retorna a posição do cursor no texto
def posCursor(vis):
	return vis.sel()[0].b

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

# Pega texto seleção e, se esta estiver vazia, da linha
def pegaTexto(vis):
	tx 	= ''
	if vis.sel()[0].empty():
		tx = pegaTextoLinha(vis)
	else:
		tx = pegaTextoSel(vis)
	return tx

# Manda o cursor para uma posição do texto
def vaiCursor(vis, pos):
	vis.sel().clear()
	vis.sel().add(sublime.Region(pos,pos))

# Retorna o cursor para a posição certa, de acordo com parâmetro
def voltaCursor(vis, pos_init, modo_retorno=0):

	# 1 - Posição inicial ou mais próxima
	if modo_retorno == 1:

		nova_linha = vis.line(vis.text_point(pos_init[0],pos_init[0]))
		comp_linha = nova_linha.b - nova_linha.a

		if comp_linha < pos_init[1]:
			pos_linha = comp_linha
		else:
			pos_linha = pos_init[1]

		vaiCursor(vis,vis.text_point(pos_init[0],pos_linha))

	# 0 - Fim da linha
	elif modo_retorno == 0:
		vaiCursor(vis,vis.line(posCursor(vis)).b)

	else: return


# Padrão para aplicação de alteração no texto
def aplica(edit, func, vis=None, argList=(), retorno_cursor=0, modo=None):

	# if match:
	#	x(match.start(1),match.end(1))

	#  !!! FAZER ???
	# se não foi passada a 'view', considera a última view ativa

	# Guarda posição inicial do cursor para voltar depois
	pos_antes = vis.rowcol(vis.sel()[0].b)

	tx = pegaTexto(vis)
	argList += (tx,)
	if modo != None:
		argList += (modo,)

	linhaComeco = linhaCursor(vis)
	ret = func(*argList)

	if (pegaTextoSel(vis) == ''):
		mudaLinha(vis,edit,ret)
	else:
		mudaSel(vis,edit,ret)

	# Volta cursor na posição inicial
	voltaCursor(vis, pos_antes, modo_retorno=retorno_cursor)