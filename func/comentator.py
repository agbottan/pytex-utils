
###################
#   COMENTÁRIOS   #
###################

import re, sublime
from func.utils import splitRe, posIdent
from func.editor import *


# ------------------------ #
#  CONFIG DOS COMENTÁRIOS  #
# ------------------------ #

class ConfigComenta:
	
	#dirImg = 'img/'

	tags = (
	) # -tags

# Fim de 'ConfigComenta'


def comenta(tx='', modo=None):

	linhas = tx.splitlines(True)

	return str(linhas)
