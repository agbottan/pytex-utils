
#####################
#	CONFIG DO HTML	#
#####################

class ConfigHtml:
	
	dirImg = '',

	tags = (
		{ # <a>
			're':r'^\s*a(?=\s+|\.|#|~|$)', 'tag':'a',
			'atribs':(
				('href', '#'),
			)
		},
		{ # <img>
			're':r'^\s*i(?=\s+|\.|#|~|$)', 'tag':'img',
			'autofecha': True,
			'atribs':(
				#('src', self['dirImg']),
				('src', 'img/'),
				('alt', '')
			)
		},
		{ # <div>
			're':r'^\s*d(?=\s+|\.|#|~|$)', 'tag':'div',
		},
		{ # <span>
			're':r'^\s*s(?=\s+|\.|#|~|$)', 'tag':'span',
		},
		{ # <p>
			're':r'^\s*p(?=\s+|\.|#|~|$)', 'tag':'p',
		},
		{ # <strong>
			're':r'^\s*st(?=\s+|\.|#|~|$)', 'tag':'strong',
		},
		{ # <br> <hr>
			're':r'^\s*(?P<tag>br|hr)(?=\s+|\.|#|~|$)', 'tag':'\g<tag>',
			'autofecha': True
		},

		# === LISTAS ===

		{ # <ul>
			're':r'^\s*ul(?=\s+|\.|#|~|$)', 'tag':'ul',
		},
		{ # <li>
			're':r'^\s*li(?=\s+|\.|#|~|$)', 'tag':'li',
		},

		# === HEADERS ===

		{ # <h1> <h2> <h3> <h4> <h5> <h6>
			're':r'^\s*h([123456])(?=\s+|\.|#|~|$)', 'tag':r'h\1',
		},

		# === TABELAS ===

		{ # <table>
			're':r'^\s*tb(?=\s+|\.|#|~|$)', 'tag':'table',
		},
		{ # <tr>
			're':r'^\s*tr(?=\s+|\.|#|~|$)', 'tag':'tr',
		},
		{ # <td>
			're':r'^\s*td(?=\s+|\.|#|~|$)', 'tag':'td',
		},
		{ # <th>
			're':r'^\s*th(?=\s+|\.|#|~|$)', 'tag':'th',
		},

		# === FORMS ===

		{ # <form>
			're':r'^\s*fm(?=\s+|\.|#|~|$)', 'tag':'form',
			'atribs':(
				('action', "javascript:alert('action');"),
				('method', 'post')
			)
		},
		{ # <input - text>
			're':r'^\s*in(?=\s+|\.|#|~|$)', 'tag':'input',
			'autofecha': True,
			'atribs':(
				('id', ''),
				('name', ''),
				('type', 'text')
			)
		},
		{ # <option>
			're':r'^\s*op(?=\s+|\.|#|~|$)', 'tag':'option',
			'atribs':(
				('value', ''),
			)
		},
	)  # .tags

# Fim de 'ConfigHtml'