
###################
#   COMENTÁRIOS   #
###################

import re, sublime
from func.utils import splitRe, sepIdent
from func.editor import *


# ------------------------ #
#  CONFIG DOS COMENTÁRIOS  #
# ------------------------ #

class ConfigComenta:

	langs = (

		# MODO | REGEX

	)

# Fim de 'ConfigComenta'


def comenta(tx='', modo=None):

	linhas = tx.splitlines(True)
	tx = ''.join(linhas).strip()

	#return '<!--\n' + tx + '\n-->'

	return str(sepIdent(tx)) + '\n' + str(posIdent(tx))
