
#####################
#	CONFIG DO HTML	#
#####################

class ConfigHtml:
	
	dirImg = 'img/'

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
				('src', dirImg),
				('alt', '')
			)
		},
		{ # <div>
			're':r'^\s*d(?=\s+|\.|#|~|$)', 'tag':'div',
		},
		{ # <span>
			're':r'^\s*s(?=\s+|\.|#|~|$)', 'tag':'span',
			'linear': True
		},
		{ # <p>
			're':r'^\s*p(?=\s+|\.|#|~|$)', 'tag':'p',
			'linear': True
		},
		{ # <strong>
			're':r'^\s*st(?=\s+|\.|#|~|$)', 'tag':'strong',
			'linear': True
		},
		{ # <br> <hr>
			're':r'^\s*(?P<tag>br|hr)(?=\s+|\.|#|~|$)', 'tag':'\g<tag>',
			'taglist': ('br','hr'),
			'autofecha': True
		},

		# === LISTAS ===

		{ # <ul>
			're':r'^\s*ul(?=\s+|\.|#|~|$)', 'tag':'ul',
		},
		{ # <li>
			're':r'^\s*li(?=\s+|\.|#|~|$)', 'tag':'li',
			'linear': True
		},

		# === HEADERS ===

		{ # <h1> <h2> <h3> <h4> <h5> <h6>
			're':r'^\s*h([123456])(?=\s+|\.|#|~|$)', 'tag':r'h\1',
			'taglist': ('h1','h2','h3','h4','h5','h6'),
			'linear': True
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
			'linear': True
		},
		{ # <th>
			're':r'^\s*th(?=\s+|\.|#|~|$)', 'tag':'th',
			'linear': True
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