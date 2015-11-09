
############### REPLICAÇÃO ###############

import sublime, sublime_plugin, sys, re, os

# Caminho para módulos
paths = (
	# Apto Bauru - Windows
	# 'C:\\Users\\andre_bottan\\AppData\\Roaming\\Sublime Text 3\\Packages\\User',

	# Apto Bauru - Linux
	'/home/andre/.config/sublime-text-3/Packages/User',

	# Lecom
	# 'C:\\Users\\123\\AppData\\Roaming\\Sublime Text 3\\Packages\\User',

	# Triata
	'C:\\Users\\Triata\\AppData\\Roaming\\Sublime Text 3\\Packages\\User',

	# Duartina
	'F:\\ST3\\Data\\Packages\\User'
)

# =========================================================== #

for path in paths:
	if os.path.isdir(path) and path not in sys.path:
		sys.path.append(path)

import func.editor, func.utils

# RELOAD !!!

import imp
imp.reload(func.editor)

#----------------------------------------------------#
#	MONTA AULA CURSO
#----------------------------------------------------#

def limpaTags(tx=''):
	return re.sub(r'<.*?>','',tx)

def quebra(tx):
	return re.split(r'\n{2,}',tx,re.MULTILINE)

def montaAula(txt=''):

	def monta(tx):
		tx = re.sub(r'</?p>','',tx)
		tx = re.sub(r'"(.*?)"',r'<strong>\1</strong>',tx)
		tx = re.sub(r'\n','<br />\n',tx)
		tx = re.sub(r'<br />$','',tx,re.MULTILINE)
		tx = '<p>'+tx+'</p>'
		return tx

	itens = map(monta,quebra(txt))

	return '\n\n'.join(itens)


#----------------------------------------------------#

class MontaAulaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		func.editor.aplica(edit, func=montaAula, vis=self.view)

class LimpaTagsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		func.editor.aplica(edit, func=limpaTags, vis=self.view)