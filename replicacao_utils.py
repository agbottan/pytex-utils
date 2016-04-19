
############### REPLICAÇÃO ###############

import sublime, sublime_plugin, sys, re, os, imp

# Caminho para módulos
paths = (

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
#from func import editor

from func.utils import *

from func.css_apaga import *
from func.css_expande import *
from func.html import *
from func.entities import *
from func.formata_linhas import *

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
		modo = resolveModo(pegaModoInfo(vis))

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

		modo = resolveModo(pegaNomeArquivoAtivo(self.view))

		# Apaga CSS
		if modo['modo'] in ('css_arq','css_tag','css_attr'):
			cssAutoApaga(self.view,edit)
		else:
			x('Não apaga "' + modo['ext'] + '"')
