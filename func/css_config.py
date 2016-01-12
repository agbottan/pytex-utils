
###################
#  CONFIG DO CSS  #
###################

class ConfigCss:
	
	dirImg = 'img/'

	props = (

		{ # <a>
			're':r'^\s*a(?=\s+|\.|#|~|$)', 'tag':'a',
			'linha':0,
			'atribs':(
				('href', '#'),
			)
		},
		{ # <img>
			're':r'^\s*i(?=\s+|\.|#|~|$)', 'tag':'img',
			'autofecha': True,
			'linha':0,
			'atribs':(
				('src', dirImg),
				('alt', '')
			)
		},
		{ # <div>
			're':r'^\s*d(?=\s+|\.|#|~|$)', 'tag':'div',
			'linha':2
		},
		{ # <span>
			're':r'^\s*s(?=\s+|\.|#|~|$)', 'tag':'span',
			'linha':0
		},
		{ # <p>
			're':r'^\s*p(?=\s+|\.|#|~|$)', 'tag':'p',
			'linha':1
		},
		{ # <strong>
			're':r'^\s*st(?=\s+|\.|#|~|$)', 'tag':'strong',
			'linha':0
		},
		{ # <br> <hr>
			're':r'^\s*(?P<tag>br|hr)(?=\s+|\.|#|~|$)', 'tag':'\g<tag>',
			'taglist': ('br','hr'),
			'autofecha': True,
			'linha':1
		},

		# === LISTAS === #

		{ # <ul>
			're':r'^\s*ul(?=\s+|\.|#|~|$)', 'tag':'ul',
			'linha':2
		},
		{ # <li>
			're':r'^\s*li(?=\s+|\.|#|~|$)', 'tag':'li',
			'linha':1
		},

		# === HEADERS === #

		{ # <h1> <h2> <h3> <h4> <h5> <h6>
			're':r'^\s*h([1-6])(?=\s+|\.|#|~|$)', 'tag':r'h\1',
			'taglist': ('h1','h2','h3','h4','h5','h6'),
			'linha':1
		},

		# === TABELAS === #

		{ # <table>
			're':r'^\s*tb(?=\s+|\.|#|~|$)', 'tag':'table',
			'linha':2
		},
		{ # <tr>
			're':r'^\s*tr(?=\s+|\.|#|~|$)', 'tag':'tr',
			'linha':2
		},
		{ # <td> <th>
			're':r'^\s*(?P<tag>td|th)(?=\s+|\.|#|~|$)', 'tag':'\g<tag>',
			'taglist': ('td','th'),
			'linha':1
		},

		# === FORMS === #

		{ # <form>
			're':r'^\s*fm(?=\s+|\.|#|~|$)', 'tag':'form',
			'linha':2,
			'atribs':(
				('action', "javascript:alert('action');"),
				('method', 'post')
			)
		},
		{ # <input - text>
			're':r'^\s*in(?=\s+|\.|#|~|$)', 'tag':'input',
			'autofecha': True,
			'linha':1,
			'atribs':(
				('id', ''),
				('name', ''),
				('type', 'text')
			)
		},
		{ # <option>
			're':r'^\s*op(?=\s+|\.|#|~|$)', 'tag':'option',
			'linha':1,
			'atribs':(
				('value', ''),
			)
		},

		# === HTML-5 === #
		
		{ # <header>
			're':r'^\s*h[ed](?=\s+|\.|#|~|$)', 'tag':'header',
			'linha':2
		},
		{ # <section>
			're':r'^\s*s[ce](?=\s+|\.|#|~|$)', 'tag':'section',
			'linha':2
		},
		{ # <footer>
			're':r'^\s*f[ot](?=\s+|\.|#|~|$)', 'tag':'footer',
			'linha':2
		},
		{ # <aside>
			're':r'^\s*as(?=\s+|\.|#|~|$)', 'tag':'aside',
			'linha':2
		},
		{ # <article>
			're':r'^\s*at(?=\s+|\.|#|~|$)', 'tag':'article',
			'linha':2
		},
		{ # <main>
			're':r'^\s*ma(?=\s+|\.|#|~|$)', 'tag':'main',
			'linha':2
		}

	)  # .tags

# Fim de 'ConfigHtml'
