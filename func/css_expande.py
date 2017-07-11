
#####################
#   CSS > EXPANDE   #
#####################

import re, sublime
from func.utils import splitRe, posIdent
from func.editor import *
from func.css_config import ConfigCss


# ------------------------------------------------------- #

def pegaFonte():
  # !!! TODO !!! -> Pegar a fonte por projeto ?? SASS
  return ''


reCor = re.compile(r'(?:[0-9a-fA-F]{3}){1,2}')

def pegaCor(regra, junta=True):
  cores = reCor.findall(regra)
  cores[:] = [ '#' + cor for cor in cores ]
  if junta:
    cores = ' '.join(cores)
  return cores


# -------- MEDIDAS --------

unidades = ('px','%','rem','em','vw','vh','cm','mm')
unidades_atalhos = ('=', 'm')

sub = {
  'm': 'em',
  '=': '%',
}

# Regex que acha os números
reMedida = re.compile(r'(a|-?[\d,\.]+)(' + '|'.join(unidades + unidades_atalhos) + ')?')

def pegaMedidas(regra, limite=None, completaUnidades=True, unidadePadrao='px', junta=True):

  medidas = reMedida.findall(regra)

  if limite:
    medidas = medidas[:limite]

  if completaUnidades:
    for i, medida in enumerate(medidas):

      numero, unidade = medida

      # Tira '0' à esquerda
      numero = re.sub(r'^0(\d+)','\g<1>', numero)

      # Põe a unidade padrão
      if unidade == '':
        unidade = unidadePadrao

      # 'm' vira 'em'
      if unidade == 'm':
        unidade = 'em'

      # '=' vira '%'
      if unidade == '=':
        unidade = '%'

      # Descarta casa decimal quando a unidade é em pixels
      match = False
      if unidade == 'px':
        match = re.search(r'[.,]+', numero)

      if match:
        numero = numero[:match.start(0)]

      # medida 'auto'
      if numero == 'a':
        numero, unidade = 'auto', ''

      # Transforma '0 unid' em '0'
      if numero == '0':
        unidade = ''

      # Altera item da coleção
      medidas[i] = numero + unidade

  # Junta tudo em 'string' se a opção estiver habilitada
  if junta:
    medidas = ' '.join(medidas)

  return medidas


def limpaNumeros(regra):

  numeros = reMedida.findall(regra)

  numeros[:] = [n[0] for n in numeros] # Reduz para o primeiro subgrupo apenas

  for n in numeros:
    regra = re.sub(n,'',regra)

  return regra


def separaNumeros(regra, limite=None, completaUnidades=True, unidadePadrao='px', junta=True):

  return limpaNumeros(regra), pegaMedidas(regra, limite, completaUnidades, unidadePadrao, junta)


############### EXPANSOR DE CSS ###############

def cssExpande(tx, modo=None, escopo=None):

  # Converte tuplas de config_prop-val em string
  def propsMonta(propsReserva, ident='', propsSepara='', separa=': '):
    return propsSepara.join([
      ident + p[0] + separa + p[1] + ';' for p in propsReserva
    ])

  ret = ''

  # Aplica 'cssLista' dentro das chaves '{}'
  if re.search(r'{.+}',tx):

    def cb(tx):

      nonlocal modo

      lista = cssLista(
        tx = tx,
        dirImg = modo['dirImg']
      )
      return propsMonta(
        propsReserva = lista,
        ident = '',
        propsSepara = ' '
      )

    tx = re.sub(r'(?<={).*?(?=})', cb, tx)  # aplica 'cssLista' e 'propsMonta' dentro das chaves '{}'
    tx = re.sub(r'{(?=\S)','{ ', tx)        # põe espaço depois de '{'
    tx = re.sub(r'(?<=\S)}',' }', tx)       # põe espaço antes de '}'
    ret = tx

  # Aplica 'cssLista' se não houver as duas chaves '{}'
  else:
    i = posIdent(tx)
    lista = cssLista(
      tx = tx[i::],
      dirImg = modo['dirImg']
    )
    ret = propsMonta(
      propsReserva = lista,
      ident = tx[0:i],
      propsSepara = '\n'
    )

  return ret

#--------------------------------- fim de 'cssExpande'

############### CSS SUB ##############################

def cssLista(tx, dirImg=''):

  configCss = ConfigCss()

  if type(tx) != str:
    tx = tx.group(0)
  
  Regras = splitRe(tx, configCss.reCss)

  fim_prop = None
  novasRegras = []
  
  if Regras == None:
    return ''.join(novasRegras)

  # ========================== Laço por cada regra
  for regra in Regras:
    
    novaRegra = []; # inicializa nova regra

    # ========================== Propriedade feita, ignora...

    if configCss.reIgnora.match(regra):

      regra = regra.replace(';','')           # Retira o ';' no final da propriedade
      regra = re.sub(r'\s+$', '', regra)      # Apaga os espaços em branco no final da propriedade
      regra = re.split(r'\s*:\s*', regra, 1)  # Corta pelo ':' e faz o par
      regra = tuple(regra)                    # Transforma a lista em tupla

      novaRegra.append(regra)
      continue

    # ========================== Propriedades não formadas

    for config_prop in configCss.props:

      # ===============================================
      #   Sem expansão, ignora...
      # ===============================================

      matchRegra = re.match(config_prop['regex'],regra)

      if matchRegra == None:
        continue # sai do loop


      # ========================== Com expansão...

      caso = config_prop['nome']


      # ===============================================
      #   DISPLAY
      # ===============================================

      if caso == 'Display':

        valor = {

          'b': 'block',
          'f': 'flex',
          'i': 'inline',
          'l': 'inline-block',
          'n': 'none',

        }.get(matchRegra.group(1))

        novaRegra.append(('display', valor))


      # ===============================================
      #   POSITION
      # ===============================================

      if caso == 'Position':

        valor = {

          'a': 'absolute',
          'f': 'fixed',
          'k': 'sticky',
          'r': 'relative',
          's': 'static',

        }.get(matchRegra.group(1))

        completaPosicao = {

          '7' : [('top', '0'), ('left', '0')],
          '8' : [('top', '0'), ('left', '0')],
          '88': [('top', '0'), ('right', '0'), ('left', '0')],
          '9' : [('top', '0'), ('right', '0')],
          '6' : [('right', '0')],
          '66': [('top', '0'), ('right', '0'), ('bottom', '0')],
          '3' : [('bottom', '0'), ('left', '0')],
          '2' : [('bottom', '0')],
          '22': [('right', '0'), ('bottom', '0'), ('left', '0')],
          '1' : [('bottom', '0'), ('left', '0')],
          '4' : [('left', '0')],
          '44': [('top', '0'), ('bottom', '0'), ('left', '0')],
          '5' : [('top', '0'), ('right', '0'), ('bottom', '0'), ('left', '0')],

        }.get(matchRegra.group(2))

        # Só posição, sem dimensionamento
        if valor:
            novaRegra.append(('position', valor))

        # 'position absolute', com dimensionamento
        else:
            novaRegra.append(('position', 'absolute'))
            novaRegra += completaPosicao


      # ===============================================
      #   DESLOCAMENTO
      # ===============================================

      if caso == 'Deslocamento':

        propriedade = {

          'to': 'top',
          'r':  'right',
          'b':  'bottom',
          'l':  'left',

        }.get(matchRegra.group(0))

        valor = pegaMedidas(regra, limite=1)

        novaRegra.append((propriedade, valor))


      # ===============================================
      #   Z-INDEX
      # ===============================================

      if caso == 'Z-index':

        valor = pegaMedidas(regra, limite=1, unidadePadrao='')

        novaRegra.append(('z-index', valor))


      # ===============================================
      #   FLOAT
      # ===============================================

      if caso == 'Float':

        valor = {

          'l': 'left',
          'r': 'right',
          'n': 'none',

        }.get(matchRegra.group(1))

        novaRegra.append(('float', valor))


      # ===============================================
      #   CLEAR
      # ===============================================

      if caso == 'Clear':

        valor = {

          'l': 'left',
          'r': 'right',
          'b': 'both',
          'n': 'none',

        }.get(matchRegra.group(1))

        novaRegra.append(('clear', valor))


      # ===============================================
      #   BOX-SIZING
      # ===============================================

      if caso == 'Box':

        valor = {

          'b': 'border-box',
          'c': 'content-box',

        }.get(matchRegra.group(1))

        novaRegra.append(('box-sizing', valor))


      # ===============================================
      #   CURSOR
      # ===============================================

      if caso == 'Cursor':

        valor = {

          'd': 'default',
          'p': 'pointer',

        }.get(matchRegra.group(1))

        novaRegra.append(('cursor', valor))


      # ===============================================
      #   OVERFLOW
      # ===============================================

      if caso == 'Overflow':

        valor = {

          'a': 'auto',
          'h': 'hidden',
          's': 'scroll',
          'v': 'visible',

        }.get(matchRegra.group(1))

        novaRegra.append(('overflow', valor))


      # ===============================================
      #   COLOR
      # ===============================================

      if caso == 'Color':

        valor = pegaCor(regra)
        
        novaRegra.append(('color', valor))


      # ===============================================
      #   WIDTH - HEIGHT
      # ===============================================

      if caso == 'Width-Height':
        
        numeros = pegaMedidas(regra, limite=2, junta=False)

        matchProp = matchRegra.group(1)

        propriedades = {

          'w':  ['width'],
          'h':  ['height'],
          'wh': ['width','height'],
          'hw': ['height','width'],
          'q':  ['width','height']

        }.get(matchProp)

        if matchProp == 'q':
          novaRegra = list(zip(propriedades,(numeros[0],numeros[0])))

        else:
          novaRegra = list(zip(propriedades,numeros))


      # ===============================================
      #   MARGIN - PADDING
      # ===============================================

      if caso == 'Margin-Padding':

        propriedade = {

          'm':  'margin',
          'pd': 'padding'

        }.get(matchRegra.group(1))

        propriedade_sub  = {

          't': '-top',
          'r': '-right',
          'b': '-bottom',
          'l': '-left'

        }.get(matchRegra.group(2),'')

        if propriedade_sub == '':
          limite = 4
        else:
          limite = 1

        valor = pegaMedidas(regra, limite=limite)

        novaRegra.append(( propriedade + propriedade_sub, valor ))


      # ===============================================
      #   TEXT
      # ===============================================

      if caso == 'Text':
        
        # sub-propriedades e valores
        subprop_val = {

          'a': ( '-align',
            {
              'c': 'center',
              'j': 'justify',
              'l': 'left',
              'r': 'right',
            }),

          'd': ( '-decoration',
            {
              'n': 'none',
              'o': 'overline',
              'u': 'underline',
            }),

          'i': '-indent',

          't': ( '-transform',
            {
              'l': 'lowercase',
              'c': 'capitalize',
              'u': 'uppercase',
            }),

        }.get(matchRegra.group(1))

        # Não é text-indent
        if isinstance(subprop_val, tuple):
          propriedade_sub = subprop_val[0]
          valor = subprop_val[1].get(matchRegra.group(2), '')

        # É text-indent
        else:
          propriedade_sub = subprop_val
          valor = pegaMedidas(regra, limite=1)
        
        novaRegra.append(( 'text' + propriedade_sub, valor ))


      # ===============================================
      #   FONT
      # ===============================================

      if caso == 'Font':
        
        # sub-propriedades e valores
        subprop_val = {

          'f': '-family',
          's': '-size',

          'w': ( '-weight',
            {
              'b': 'bold',
              'n': 'normal',
            }),

        }.get(matchRegra.group(1))
        
        # Não é 'text-indent'
        if isinstance(subprop_val, tuple):
          propriedade_sub = subprop_val[0]
          valor = subprop_val[1].get(matchRegra.group(2), '')

        # É 'text-indent'
        else:
          propriedade_sub = subprop_val
          valor = pegaMedidas(regra, limite=1)
        
        novaRegra.append(( 'font' + propriedade_sub, valor ))


      # ===============================================
      #   BORDER
      # ===============================================

      # sub-propriedades e valores
      if caso == 'Border':
        
        subprop = {

          'd':'dotted',
          'r':'radius',
          's':'solid',

        }.get(matchRegra.group(1))

        # É 'border-radius'
        if subprop == 'radius':
          propriedade_sub = '-radius'
          valor = pegaMedidas(regra, limite=4)

        # Não é 'border-radius'
        else:
          propriedade_sub = ''
          valor = subprop

        novaRegra.append(( 'border' + propriedade_sub, valor ))


      # ===============================================
      #   BACKGROUND
      # ===============================================

      if caso == 'Background':
        
        vImg = vCor = vPox = vPoy = vAtt = vRep = ''
        
        # -------------------------- Background --------------------------------
        
        subprop = {

          'a': '-attachment',
          'i': '-image', 
          'p': '-position',
          'r': '-repeat',
          'c': '-color',
          's': '-size',

        }.get(matchRegra.group(1),'')

        if subprop in ('','-image'):
        
          # -------------------------- Imagem --------------------------------
          
          vImg = re.search(r'\w+\.(png|jpg|gif)', regra)
          if vImg:
            vImg = vImg.group(0)
            regra = re.sub(vImg,'',regra)
            vImg = 'url("'+ dirImg + vImg +'")'
          else:
            vImg = ''
        
        if subprop in ('','-color'):

          # -------------------------- Color --------------------------------

          vCor = pegaCor(regra)

        if subprop in ('','-position'):

          # -------------------------- Position X --------------------------------
        
          if   regra.find('l') != -1: vPox = 'left'
          elif regra.find('r') != -1: vPox = 'right'

          # -------------------------- Position Y --------------------------------

          if   regra.find('t') != -1: vPoy = 'top'
          elif regra.find('b') != -1: vPoy = 'bottom'
        
        if subprop in ('','-repeat'):

          # -------------------------- Repeat --------------------------------
        
          if   regra.find('n')  != -1: vRep = 'no-repeat'
          elif regra.find('re') != -1: vRep = 'repeat'
          elif regra.find('x')  != -1: vRep = 'repeat-x'
          elif regra.find('y')  != -1: vRep = 'repeat-y'
        
        if subprop == '':
        
          # -------------------------- Genéricas --------------------------------
          
          if vImg == '': vImg = 'url("'+ dirImg +'")'
          if vCor == '': vCor = ''
          if vPox == '': vPox = 'left'
          if vPoy == '': vPoy = 'top'
          if vAtt == '': vAtt = ''
          if vRep == '': vRep = 'no-repeat'
        
        # Retorna
        fim_vals = ( vImg, vCor, vPox, vPoy, vAtt, vRep )
        fim_vals = ' '.join(fim_vals)
        fim_vals = fim_vals.strip(' ')

        fim_vals = str(fim_vals)

        novaRegra.append(( 'background' + subprop, fim_vals ))
      
      #- 'switch'
    #- 'for' dos 'patterns'

    novasRegras += novaRegra

  #- 'for' das 'Regras'

  return novasRegras

#--------------------------------- fim de 'cssLista'