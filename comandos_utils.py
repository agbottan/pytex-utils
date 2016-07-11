
############### PYTEX UTILS ###############

import sublime, sublime_plugin, sys, re, os, imp

# Caminho para módulos
paths = (

	# Laptop - Linux
	# ---- 

	# Apto Bauru - Linux
	'/home/andre/.config/sublime-text-3/Packages/User',

	# Triata - Windows
	'C:\\Users\\Triata\\AppData\\Roaming\\Sublime Text 3\\Packages\\User'
)

for path in paths:
	if os.path.isdir(path) and path not in sys.path:
		sys.path.append(path)


# --------------------------------

# !!! from func import editor
from func.editor import *

from func.utils import *

from func.css_apaga import *
from func.css_expande import *
from func.html import *
from func.entities import *
from func.formata_linhas import *
from func.comentator import *

# --------------------------------

# !!! RELOAD !!!
# import imp
# imp.reload(func.editor)
# imp.reload(func.html)
# imp.reload(func.css_apaga)
# imp.reload(func.css_expande)


# ============== CLASSES DOS COMANDOS ============== #

#----------------------------------------------------#
#	CONVERTE 'HTML ENTITIES'
#----------------------------------------------------#
class TrocaEntitiesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		aplica(edit,entities.trocaEntities,self.view)


#----------------------------------------------------#
#	LIMPA TEXTO
#----------------------------------------------------#
class LimpaTextoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		aplica(edit, func=limpaTexto, vis=self.view)


#----------------------------------------------------#
#	FORMATA LINHAS
#----------------------------------------------------#
class FormataLinhasCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		aplica(edit, vis=self.view, func=formataLinhas)


#----------------------------------------------------#
#	AUTO EXPANDE
#----------------------------------------------------#
class AutoExpandeCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		vis = self.view
		modo = resolveModo(pegaInfoModo(vis))

		# Expande CSS
		if modo['modo'] in ('css_arq','css_tag','css_attr'):
			aplica(
				edit, vis=vis, modo=modo,
				func=cssExpande
			)

		# Expande HTML
		elif modo['modo'] == 'html':
			aplica(
				edit, vis=vis, modo=modo,
				func=htmlExpande
			)

		# Expande PHP
		elif modo['modo'] == 'php':
			aplica(
				edit, vis=vis, modo=modo,
				func=phpExpande
			)

		else:
			x('Não expande "' + modo['ext'] + '"')


#----------------------------------------------------#
#	AUTO APAGA
#----------------------------------------------------#
class AutoApagaCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		vis = self.view
		modo = resolveModo(pegaInfoModo(vis))

		# Apaga CSS
		if modo['modo'] in ('css_arq','css_tag','css_attr'):
			cssAutoApaga(edit, self.view)
		else:
			x('Não apaga "' + modo['ext'] + '"')


#----------------------------------------------------#
#	COMENTÁRIOS
#----------------------------------------------------#
class ComentaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		vis = self.view
		modo = resolveModo(pegaInfoModo(vis))
		aplica(edit, vis=self.view, func=comenta, modo=modo)

		#x(pegaInfoModo(vis))


#----------------------------------------------------#
#	MOSTRA NOME
#----------------------------------------------------#
class MostraNome(sublime_plugin.TextCommand):
	def run(self, edit):
		# sublime.message_dialog(self.view.file_name())
		x(self.view.file_name())


#----------------------------------------------------#
#	SNIPPET
#----------------------------------------------------#

class SnipTraduzCommand(sublime_plugin.TextCommand):

	def wrapTraduz(modo, tx):
		return "<?php echo $this->translate('" + tx + "'); ?>"

	def run(self, edit):
		aplica(edit, vis=self.view, func=self.wrapTraduz)


#----------------------------------------------------#
#	BUSCA ARQUIVOS RELACIONADOS
#----------------------------------------------------#

class BuscaArquivoCommand(sublime_plugin.TextCommand):

	locais = {
		'local':			  'C:\\Apache24\\htdocs\\trio\\',
		'dev':				  'Z:\\projetos\\2_execucao\\fastpro\institucional\\site\\',
		'instalador_trio':	  'C:\\Apache24\htdocs\\projeto-padrao\\',
		'instalador_modulos': 'C:\\Apache24\htdocs\\trio-modulos-v2\\'
	}

	def run(self, edit):

		ambiente_atual = None;
		nome = self.view.file_name()

		x(nome)

		for ambiente, pasta in self.locais.items():

			if pasta in nome:
				ambiente_atual = ambiente

		x(ambiente_atual)

#x('_' in 'ccc')
#x(self.vteste)
#x(self.view.file_name())

#sublime.active_window().open_file(
#	self.view.file_name()
#)

#sublime.active_window().project_file_name()
#self.view.file_name()
