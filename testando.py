
# -------------------
# 	TESTANDO
# -------------------

import sublime, sublime_plugin, imp

#import testemod.testemod_1
#import testemod.testemod_2

#from testemod import *
# import testemod
from testemod.testemod_1 import func_1
from testemod.testemod_2 import func_2


#imp.reload(testemod)
#imp.reload(testemod)

# Barra Separadora
barra = '\n' + '#' * 80 + '\n'

class TesteModuloCommand(sublime_plugin.TextCommand):
	def run(self, edit, fruta):
		print(
			# barra,
			# fruta,
			# func_1(),
			# func_2(),
			# sublime.context

			sublime.Window.extract_variables(self)
		)


# PROXY