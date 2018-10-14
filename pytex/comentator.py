
###################
#   COMENTÁRIOS   #
###################

import re, sublime
from pytex.utils import splitRe, sepIdent, posIdent
from pytex.editor import *


# ------------------------ #
#  CONFIG DOS COMENTÁRIOS  #
# ------------------------ #

class ConfigComenta:

	langs = (

		# ------------ HTML
		('html', {
			'linhas': False,
			'comeco': '<!-- ',
			'fim': ' -->'
		}),

		# ------------ JS | PHP
		('js', {
			'linhas': True,
			'comeco': '# '
		}),

		# ------------ PYTHON
		('py', {
			'linhas': True,
			'comeco': '# '
		})
	)

# Fim de 'ConfigComenta'


def comenta(tx='', modo=None, escopo='', alternativo=False):

	X_("modo => ", modo);
	X_("escopo => ", escopo);
	X_("alternativo => ", alternativo);

	conf = ConfigComenta()

	linhas = tx.splitlines(True)
	tx = ''.join(linhas)

	tx_ident, tx_resto = sepIdent(tx)

	ret = tx_ident + '<!--' + tx_resto + '-->'

	return ret