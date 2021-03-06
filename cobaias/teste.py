#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# ****************************************************** #


###################
#  CONFIG DO CSS  #
###################

import re


class ConfigCss:
  
  # Diretório das imagens
  dirImg = 'img/'

  # Propriedades já montadas - não sofrem alteração
  ignora = r'\b(display|position|z-index|left|top|right|bottom|float|clear|margin|padding|(min-|max-)?width|(min-|max-)?height|line-height|border|text|font|color|background|overflow)[^;]*;'

  # Propriedades a montar
  props = (

    # VISIBILIDADE
    { 'nome' : 'Display',  'regex' : r'\bd[bfnil]\b'    }, # Display
    { 'nome' : 'Overflow', 'regex' : r'\bo[xy]?[hsv]\b' }, # Overflow
    
    # POSICIONAMENTO
    { 'nome' : 'Position', 'regex' : r'\bp[akrfs]\b' }, # Position
    { 'nome' : 'Z-index',  'regex' : r'\bz\s*\d+\b'  }, # Z-index
    { 'nome' : 'Float',    'regex' : r'\bf[lrn]\b'   }, # Float
    { 'nome' : 'Clear',    'regex' : r'\bc[lrbn]\b'  }, # Clear
    { 'nome' : 'Box',      'regex' : r'\bbs[b]?\b'   }, # Box-sizing
    
    # DESLOCAMENTO
    { 'nome' : 'Left',   'regex' : r'\bl\b' }, # Left
    { 'nome' : 'Top',    'regex' : r'\bt\b' }, # Top
    { 'nome' : 'Right',  'regex' : r'\br\b' }, # Right
    { 'nome' : 'Bottom', 'regex' : r'\bb\b' }, # Bottom
    
    # WIDTH - HEIGHT
    { 'nome' : 'Width-Height', 'regex' : r'\b(wh?|hw?|q)'},

    # MARGIN - PADDING
    { 'nome' : 'Margin-Padding',  'regex' : r'\b(m|pd)[trbl]?'},

    # BORDER
    { 'nome' : 'Border', 'regex' : r'\bbd[drs]\b' },

    # TEXTO
    { 'nome' : 'Cursor',      'regex' : r'\bcu[dp]\b'          }, # Cursor
    { 'nome' : 'Color',       'regex' : r'\bco\b'              }, # Color
    { 'nome' : 'Text',        'regex' : r'\bt[adit][cjlnoru]?' }, # Text
    { 'nome' : 'Font',        'regex' : r'\bf[msw][abn]?'      }, # Font
    { 'nome' : 'Line-Height', 'regex' : r'\blh'                }, # Line-Height

    # BACKGROUND
    { 'nome' : 'Background', 'regex' : r'\bbg[aiprcs]?\b' },
  ) # -props

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

conf = ConfigCss()

print(conf.reCss)