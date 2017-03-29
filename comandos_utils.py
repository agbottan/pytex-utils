
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

from func.editor import *
from func.utils import *
from func.css_apaga import *
from func.css_expande import *
from func.html import *
from func.entities import *
from func.formata_linhas import *
from func.comentator import *

# --------------------------------

################################################
# !!! RELOAD !!!
import sys
import imp
imp.reload(sys.modules['func.css_expande'])
from func.css_expande import *
imp.reload(sys.modules['func.formata_linhas'])
from func.formata_linhas import *
imp.reload(sys.modules['func.css_config'])
from func.css_config import *
################################################


# ============== CLASSES DOS COMANDOS ============== #

#----------------------------------------------------#
#	CONVERTE 'HTML ENTITIES'
#----------------------------------------------------#
class TrocaEntitiesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		aplica( edit, vis=self.view, func=entities.trocaEntities)


#----------------------------------------------------#
#	LIMPA TEXTO
#----------------------------------------------------#
class LimpaTextoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		aplica( edit, func=limpaTexto, vis=self.view)


#----------------------------------------------------#
#	FORMATA LINHAS
#----------------------------------------------------#
class FormataLinhasCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		aplica( edit, vis=self.view, func=formataLinhas, argList={ 'limpa_vazio': False })


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
		aplica( edit, vis=self.view, func=comenta, modo=modo)

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
		aplica( edit, vis=self.view, func=self.wrapTraduz)
