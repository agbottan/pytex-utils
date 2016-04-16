﻿
############### REPLICAÇÃO ###############

import sublime, sublime_plugin, sys, re, os

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

import func.css_apaga, func.css_expande, func.html, func.entities, func.editor, func.utils, func.formata_linhas

# !!! RELOAD !!!
import imp
imp.reload(func.editor)
imp.reload(func.html)
imp.reload(func.css_apaga)
imp.reload(func.css_expande)


# ============================ CLASSES DOS COMANDOS ============================ #

#----------------------------------------------------#
#	CONVERTE 'HTML ENTITIES'
#----------------------------------------------------#
class TrocaEntitiesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		func.editor.aplica(edit,func.entities.trocaEntities,self.view)


#----------------------------------------------------#
#	LIMPA TEXTO
#----------------------------------------------------#
class LimpaTextoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		func.editor.aplica(edit, func=func.utils.limpaTexto, vis=self.view)


#----------------------------------------------------#
#	FORMATA LINHAS
#----------------------------------------------------#
class FormataLinhasCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		func.editor.aplica(edit, vis=self.view, func=func.formata_linhas.formataLinhas)


#----------------------------------------------------#
#	AUTO EXPANDE
#----------------------------------------------------#
class AutoExpandeCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		vis = self.view
		modo = func.editor.pegaModo(vis)

		# Expande CSS
		if modo['modo'] in ('css_arq','css_tag','css_attr'):
			func.editor.aplica(
				edit, vis=vis, modo=modo,
				func=func.css_expande.cssExpande
			)

		# Expande HTML
		elif modo['modo'] == 'html':
			func.editor.aplica(
				edit, vis=vis, modo=modo,
				func=func.html.htmlExpande
			)

		# Expande PHP
		elif modo['modo'] == 'php':
			func.editor.aplica(
				edit, vis=vis, modo=modo,
				func=func.html.phpExpande
			)

		else:
			func.editor.x('Não expande "' + modo['ext'] + '"')


#----------------------------------------------------#
#	AUTO APAGA
#----------------------------------------------------#
class AutoApagaCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		modo = func.editor.pegaModo(self.view)

		# Apaga CSS
		if modo['modo'] in ('css_arq','css_tag','css_attr'):
			func.css_apaga.cssAutoApaga(self.view,edit)
		else:
			func.editor.x('Não apaga "' + modo['ext'] + '"')