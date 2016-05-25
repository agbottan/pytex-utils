
###################
#   COMENTÁRIOS   #
###################

import re, sublime
from func.utils import splitRe, sepIdent, posIdent
from func.editor import *


# ------------------------ #
#  CONFIG DOS COMENTÁRIOS  #
# ------------------------ #

class ConfigComenta:

	langs = (

		# MODO | REGEX
		('html', ('<!-- ', ' -->')),
		('py', 	 ('# '))
	)

# Fim de 'ConfigComenta'


def comenta(tx='', modo=None):

	config = ConfigComenta()

	linhas = tx.splitlines(True)
	#tx = ''.join(linhas).strip()
	tx = ''.join(linhas)

	#return str(sepIdent(tx)) + '\n' + str(posIdent(tx))

	tx_ident, tx_resto = sepIdent(tx)

	#return str(linhas)
	return tx_ident + '<!--' + tx_resto + '-->'

	#return '<!--\n' + tx + '\n-->'
