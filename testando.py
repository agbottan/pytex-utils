
# -------------------
# 	TESTANDO
# -------------------

import sublime, sublime_plugin, imp

import testemod.testemod_1
import testemod.testemod_2

#from testemod import *
#import testemod


#imp.reload(testemod)
#imp.reload(testemod)


barra = '\n\n###############################################\n\n'

class TesteModuloCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print(
			barra,
			testemod.testemod_1.func_1(),
			testemod_2.func_2()
		)
