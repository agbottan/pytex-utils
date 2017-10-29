
#####################
  #	LIMPEZA GERAL	#
#####################


# === Tabela das 'Entities' === #

entities = (

# =============== LETRAS ACENTUADAS

('Á','&Aacute;'),
('á','&aacute;'),
('Â','&Acirc;'),
('â','&acirc;'),
('À','&Agrave;'),
('à','&agrave;'),
('Ã','&Atilde;'),
('ã','&atilde;'),

('É','&Eacute;'),
('é','&eacute;'),
('Ê','&Ecirc;'),
('ê','&ecirc;'),

('Í','&Iacute;'),
('í','&iacute;'),
('Î','&Icirc;'),
('î','&icirc;'),

('Ó','&Oacute;'),
('ó','&oacute;'),
('Ô','&Ocirc;'),
('ô','&ocirc;'),
('Õ','&Otilde;'),
('õ','&otilde;'),

('Ú','&Uacute;'),
('ú','&uacute;'),
('Û','&Ucirc;'),
('û','&ucirc;'),

('Ç','&Ccedil;'),
('ç','&ccedil;'),

# =============== SÍMBOLOS

('Ø','&#8960;'),
('≤','&le;'),
('≥','&ge;'),
('°','&deg;')

) # ---- FIM de 'entities'


def trocaEntities(tx):
	global entities
	for ch in entities:
		tx = tx.replace(ch[0], ch[1])
	return tx
