
###################
#  CONFIG DO CSS  #
###################

import re

class ConfigCss:
  
  # Unidades
  unidades = ('px','%','rem','em','vw','vh','cm','mm')

  # Unidade padrão !!! IMPLEMENTAR
  unidadePadrao = 'px'
  
  # Diretório das imagens
  dirImg = 'img/'

  # Propriedades já montadas - não sofrem alteração
  ignora = r'\b(display|position|z-index|left|top|right|bottom|float|clear|margin|padding|(min-|max-)?width|(min-|max-)?height|line-height|border|text|font|color||cursor|background|overflow)[^;]*;'

  # Propriedades a montar
  props = (

    # VISIBILIDADE
    { 'nome': 'Display',  'regex': r'\bd([bfnil])\b'      }, # Display
    { 'nome': 'Overflow', 'regex': r'\bo([xy]?)([hsv])\b' }, # Overflow
    
    # Z-INDEX
    { 'nome': 'Z-index', 'regex': r'\bz', 'unidade': '' }, # Z-index

    # POSICIONAMENTO
    { 'nome': 'Position', 'regex': r'\bp(?:([afkrs])|(1|2|22|3|6|66|9|8|88|7|4|44|5))?\b' }, # Position
    { 'nome': 'Float',    'regex': r'\bf([lrn])\b'   }, # Float
    { 'nome': 'Clear',    'regex': r'\bc([lrbn])\b'  }, # Clear
    
    # BOX-MODEL
    { 'nome': 'Box', 'regex': r'\bbz([bc])?\b'  }, # Box-sizing

    # DESLOCAMENTO
    { 'nome': 'Deslocamento', 'regex': r'\b(to|r|bo|l)' }, # Top | Right | Bottom | Left
    
    # WIDTH - HEIGHT
    { 'nome': 'Width-Height', 'regex': r'\b(wh?|hw?|q)'},

    # MARGIN - PADDING
    { 'nome': 'Margin-Padding',  'regex': r'\b(m|pd)([trbl])?'},

    # BORDER
    { 'nome': 'Border', 'regex': r'\bb([drs])\b' },

    # TEXTO
    { 'nome': 'Text', 'regex': r'\bt([adit])([cjlnoru])?' },

    # CURSOR
    { 'nome': 'Cursor', 'regex': r'\bcu[dp]\b' },

    # COR
    { 'nome': 'Color',  'regex': r'\bco\b' },

    # FONTE
    { 'nome': 'Font', 'regex': r'\bf([fsw])([abn])?' },

    # LINE-HEIGHT
    { 'nome': 'Line-Height', 'regex': r'\blh' },

    # BACKGROUND
    { 'nome': 'Background', 'regex': r'\bbg([aiprcs])?\b' },

  ) # ------ /-props

  # Inicialização
  def __init__ (self):

    self.reIgnora = re.compile(self.ignora)

    self.reCss = re.compile(
      r'(' +
      '|'.join([self.ignora] + [ prop['regex'] for prop in self.props ]) +
      r')'
    )

# ------------------------------
# Fim de 'ConfigCss'