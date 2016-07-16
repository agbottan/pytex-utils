
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

####################
    #  TESTES  #
####################

#----------------------------------------------------#
#	TESTES > PLUGIN
#----------------------------------------------------#

class TestePluginCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		#x('== Teste de Plugin ==')
		#open_file(file_name)
		sublime.active_window().open_file(
			sublime.active_window().project_file_name()
		)


#----------------------------------------------------#
#	TESTES > COMMAND OVERLAY
#----------------------------------------------------#

class TesteOverlayCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		def cb(ind):
			x(ind,' -> ',lista[ind]);

		lista = ('banana', 'maçã', 'uva')

		self.view.window().run_command("show_overlay", {"overlay": "command_palette", "text": "Meu Plugin"})


#----------------------------------------------------#
#	TESTES > QUICK PANEL
#----------------------------------------------------#

class TesteQuickPanelCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		def cb(ind):
			x(ind,' -> ',lista[ind]);

		lista = ('banana', 'maçã', 'uva')

		self.view.window().show_quick_panel(items=lista, on_select=cb)


#----------------------------------------------------#
#	TESTES > MENU INLINE
#----------------------------------------------------#

class TesteMenuInlineCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		def cb(ind):
			x(ind,' -> ',lista[ind]);

		lista = ('banana', 'maçã', 'uva')

		self.view.show_popup_menu(items=lista, on_select=cb)


#----------------------------------------------------#
#	TESTES > PEGA CONFIG DO PROJETO
#----------------------------------------------------#

class TesteConfigProjetoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		x_(
			sublime.active_window().project_file_name()
			# sublime.active_window().views(),
			# sublime.active_window().active_view(),
			# self.view.settings().get('cor_secundaria',None),
			# sublime.active_window().project_data().get('config',None).get('cor_principal',None)
		)
