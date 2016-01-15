
######################
#   CSS > APAGADOR   #
######################

import re, sublime
from func.editor import *


############### APAGADOR DE CSS ###############

def pegaCssProp(vis):

	# ---> Cursor move 1 atrás se tiver um ';' antes
	# p = posCursor(vis)
	# if vis.substr(sublime.Region(p,p-1)) == ';': vaiCursor(vis,p-1)

	ini = fim = posCursor(vis)
	eof = vis.size()

	# Indo para o começo da linha
	ch = ''
	while ini > 0:
		ch = vis.substr(sublime.Region(ini,ini-1))
	
		if ch == '{': break

		elif ch == ';': break

		elif ch == '}':
			ini = None; break

		ini -= 1

	# Indo para o fim da linha
	ch = ''
	while fim < eof:
		ch = vis.substr(sublime.Region(fim,fim+1))

		if ch == '}': break

		elif ch == ';':
			fim += 1; break

		elif ch == '{':
			fim = None; break

		fim += 1

	return sublime.Region(ini,fim)

#--------------------------------- fim de 'pegaCssProp'

def cssAutoApaga(vis, edit):

	prop = pegaCssProp(vis)
	if None not in (prop.a,prop.b):
		vis.erase(edit,prop)

#--------------------------------- fim de 'cssAutoApaga'