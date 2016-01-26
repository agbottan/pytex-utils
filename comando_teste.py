
import sublime_plugin, moduloteste.n1.ff
#import moduloteste.n1.ff
#from moduloteste.n1 import ff

barra = '*'*150

class TestaModuloCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print(barra)
		ff()
		moduloteste.n1.ff()
		n1.ff()
