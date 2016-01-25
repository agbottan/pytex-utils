
############### REPLICAÇÃO ###############

import sublime, sublime_plugin, sys, re, os, imp

# Caminho para módulos
for path in (
	'/home/andre/.config/sublime-text-3/Packages/User', # Apto Bauru - Linux
	'C:\\Users\\Triata\\AppData\\Roaming\\Sublime Text 3\\Packages\\User' # Triata - Windows
):
	if os.path.isdir(path) and path not in sys.path:
		sys.path.append(path)

from func import *

# 'Reload' nos módulos, ao salvar este arquivo
# imp.reload(func)


# ============================ CLASSES DOS COMANDOS ============================ #

#----------------------------------------------------#
#	CONVERTE 'HTML ENTITIES'
#----------------------------------------------------#
class TrocaEntitiesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		editor.aplica(edit,entities.trocaEntities,self.view)


#----------------------------------------------------#
#	LIMPA TEXTO
#----------------------------------------------------#
class LimpaTextoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		editor.aplica(edit, func=utils.limpaTexto, vis=self.view)


#----------------------------------------------------#
#	FORMATA LINHAS
#----------------------------------------------------#
class FormataLinhasCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		editor.aplica(edit, vis=self.view, func=formata_linhas.formataLinhas)


#----------------------------------------------------#
#	AUTO EXPANDE
#----------------------------------------------------#
class AutoExpandeCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		vis = self.view
		modo = utils.pegaModo(editor.pegaNomeArquivoAtivo(vis))

		# Expande CSS
		if modo['modo'] in ('css_arq','css_tag','css_attr'):
			editor.aplica(
				edit, vis=vis, modo=modo,
				func=css_expande.cssExpande
			)

		# Expande HTML
		elif modo['modo'] == 'html':
			editor.aplica(
				edit, vis=vis, modo=modo,
				func=html.htmlExpande
			)

		# Expande PHP
		elif modo['modo'] == 'php':
			editor.aplica(
				edit, vis=vis, modo=modo,
				func=html.phpExpande
			)

		else:
			editor.x('Não expande "' + modo['ext'] + '"')


#----------------------------------------------------#
#	AUTO APAGA
#----------------------------------------------------#
class AutoApagaCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		modo = utils.pegaModo(editor.pegaNomeArquivoAtivo(self.view))

		# Apaga CSS
		if modo['modo'] in ('css_arq','css_tag','css_attr'):
			css_apaga.cssAutoApaga(self.view,edit)
		else:
			editor.x('Não apaga "' + modo['ext'] + '"')
