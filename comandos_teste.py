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

from func.meuteste import solta as solta2

# --------------------------------

################################################
# !!! RELOAD !!!

import sys
import imp

imp.reload(sys.modules['func.css_expande'])
from func.css_expande import *

imp.reload(sys.modules['func.formata_linhas'])
from func.formata_linhas import *

imp.reload(sys.modules['func.meuteste'])
from func.meuteste import solta as solta2

################################################


# ============== CLASSES DOS COMANDOS ============== #

#----------------------------------------------------#
#	TESTE REGEX
#----------------------------------------------------#
class TesteRegexCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		#X_(varteste)

		solta2()

		#def testa(modo=None, tx=''):

			# multilinha	= re.compile(r'^\s*;;;\s*\n?$')
			# multilinha	= re.compile(r'^\s*;;;\s*$', re.M)

			#X_(multilinha.search(tx))

			# if(None):
			# 	X_('False')
			# else:
			# 	X_('True')

		#aplica( edit, vis=self.view, func=testa)


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
