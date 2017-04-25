
#######################
# --- PYTEX UTILS --- #
#######################

# IMPORTS

import sublime, sublime_plugin, sys, re, os

from func.utils import sepIdent


# Caminho para módulos
paths = (

  # Linux
  '/home/andre/.config/sublime-text-3/Packages/User',

  # Windows
  'C:\\Users\\Triata\\AppData\\Roaming\\Sublime Text 3\\Packages\\User'
)

for path in paths:
  if os.path.isdir(path) and path not in sys.path:
    sys.path.append(path)


# --------------------------------

from func.editor import *
from func.utils import *
from func.css_apaga import *
from func.css_expande import *
from func.html import *
from func.entities import *
from func.formata_linhas import *
from func.comentator import *
from func.escolhe_projeto import *

# --------------------------------

################################################
# !!! RELOAD !!!

import imp

imp.reload(sys.modules['func.css_expande'])
from func.css_expande import *

imp.reload(sys.modules['func.formata_linhas'])
from func.formata_linhas import *

imp.reload(sys.modules['func.css_config'])
from func.css_config import *

imp.reload(sys.modules['func.editor'])
from func.editor import *

imp.reload(sys.modules['func.escolhe_projeto'])
from func.escolhe_projeto import *

################################################


# ============== CLASSES DOS COMANDOS ============== #

#----------------------------------------------------#
# CONVERTE 'HTML ENTITIES'
#----------------------------------------------------#
class TrocaEntitiesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    aplica( edit, vis=self.view, func=trocaEntities)


#----------------------------------------------------#
# LIMPA TEXTO
#----------------------------------------------------#
class LimpaTextoCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    aplica( edit, vis=self.view, func=limpaTexto )


#----------------------------------------------------#
# FORMATA LINHAS
#----------------------------------------------------#
class FormataLinhasCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    aplica( edit, vis=self.view, func=formataLinhas, argList={ 'limpa_vazio': False })


#----------------------------------------------------#
# AUTO EXPANDE
#----------------------------------------------------#
class AutoExpandeCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    vis = self.view
    modo = resolveModo(pegaInfoModo(vis))

    # Expande CSS
    if modo['modo'] in ('css_arq','css_tag','css_attr'):
      aplica(
        edit, vis=vis, modo=modo,
        func=cssExpande
      )

    # Expande HTML
    elif modo['modo'] == 'html':
      aplica(
        edit, vis=vis, modo=modo,
        func=htmlExpande
      )

    # Expande PHP
    elif modo['modo'] == 'php':
      aplica(
        edit, vis=vis, modo=modo,
        func=phpExpande
      )

    else:
      x('Não expande "' + modo['ext'] + '"')


#----------------------------------------------------#
# AUTO APAGA
#----------------------------------------------------#
class AutoApagaCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    vis = self.view
    modo = resolveModo(pegaInfoModo(vis))

    # Apaga CSS
    if modo['modo'] in ('css_arq','css_tag','css_attr'):
      cssAutoApaga(edit, self.view)
    else:
      x('Não apaga "' + modo['ext'] + '"')


#----------------------------------------------------#
# COMENTÁRIOS
#----------------------------------------------------#
class ComentaCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    vis = self.view
    modo = resolveModo(pegaInfoModo(vis))
    aplica( edit, vis=self.view, func=comenta, modo=modo)

    #x(pegaInfoModo(vis))


#----------------------------------------------------#
# MOSTRA NOME
#----------------------------------------------------#

class MostraNomeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # !!! X_(self.view.file_name())
    sublime.set_clipboard(self.view.file_name())


#----------------------------------------------------#
# SNIPPET > ALERT
#----------------------------------------------------#

def wrapAlert(tx, modo, aspas=False):

  formato = None
  ident, tx = sepIdent(tx)

  if aspas:
    formato = '{0}X_("{1}")'
  else:
    formato = '{0}X_({1})'

  return formato.format(ident,tx)

class AlertCommand(sublime_plugin.TextCommand):
  def run(self, edit, aspas):
    aplica( edit, vis=self.view, func=wrapAlert, argList={ 'aspas': aspas })


#----------------------------------------------------#
# ALTERNA PROJETOS
#----------------------------------------------------#

class AlternaProjetosCommand(sublime_plugin.WindowCommand):
  def run(self):

    arq_projeto_atual = os.path.basename(self.window.project_file_name())
    projetos = list( filter( lambda proj: proj['arq'] != arq_projeto_atual, projetos_config ))

    def cb(ind = 0):
      comando = "subl --project '/home/andre/Documents/ST3 Projetos/{0}'".format(projetos[ind]['arq'])
      os.system(comando)
      #self.window.run_command('close_window')

    nomes = [ proj.get('tit') for proj in projetos ]

    self.window.show_quick_panel(
      items     = nomes,
      on_select = cb
    )