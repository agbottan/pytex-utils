############### PYTEX UTILS ###############

import sublime, sublime_plugin, sys, re, os, imp

# Caminho para módulos
paths = (

  # Laptop - Linux
  # ----

  # Apto Bauru - Linux
  '/home/andre/.config/sublime-text-3/Packages/User',

  # Triata - Windows
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

from func.meuteste import solta as solta2
# import func.meuteste.soltaTeste # Dá pau

# --------------------------------

################################################
# !!! RELOAD !!!

import sys
import imp

imp.reload(sys.modules['func.css_expande'])
from func.css_expande import *

imp.reload(sys.modules['func.formata_linhas'])
from func.formata_linhas import *

imp.reload(sys.modules['func.meuteste'])
from func.meuteste import solta as solta2
from func.meuteste import soltaTeste

################################################


# ============== CLASSES DOS COMANDOS ============== #

#----------------------------------------------------#
# TESTE REGEX
#----------------------------------------------------#
class TesteRegexCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    #X_(varteste)

    solta2()
    soltaTeste()

    #def testa(modo=None, tx=''):

      # multilinha  = re.compile(r'^\s*;;;\s*\n?$')
      # multilinha  = re.compile(r'^\s*;;;\s*$', re.M)

      #X_(multilinha.search(tx))

      # if(None):
      #   X_('False')
      # else:
      #   X_('True')

    #aplica( edit, vis=self.view, func=testa)


#----------------------------------------------------#
# TESTES > PLUGIN
#----------------------------------------------------#

class TestePluginCommand(sublime_plugin.TextCommand):

  def teste(d):
    X_(d)
    
  def run(self, edit):

    X_(self.description)
    self.teste()

    #open_file(file_name)

    #sublime.active_window().open_file(
      # '/home/andre/Documents/ST3 Projetos/ponto-cruz.sublime-project'
      #sublime.active_window().project_file_name('')
    #)

    #X_(sublime.active_window().project_data())


#----------------------------------------------------#
# TESTES > COMMAND OVERLAY
#----------------------------------------------------#

class TesteOverlayCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    def cb(ind):
      X_(ind,' -> ',lista[ind]);

    lista = ('banana', 'maçã', 'uva')

    #self.view.window().run_command("show_overlay", {"overlay": "command_palette", "text": "Meu Plugin"})

    sublime.active_window().run_command("show_overlay", {"overlay": "command_palette", "text": "Active Window"})

    #self.view.show_popup('<p><input type="text" /></p>')


#----------------------------------------------------#
# TESTES > QUICK PANEL
#----------------------------------------------------#

class TesteQuickPanelCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    def cb(ind):
      X_(ind,' -> ',lista[ind]);

    lista = (
      'banana',
      'maçã',
      'uva'
    )

    self.view.window().show_quick_panel(items=lista, on_select=cb)


#----------------------------------------------------#
# TESTES > MENU INLINE
#----------------------------------------------------#

class TesteMenuInlineCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    def cb(ind):
      X_(ind,' -> ',lista[ind]);

    lista = (
      'banana',
      'maçã',
      'uva'
    )

    self.view.show_popup_menu(items=lista, on_select=cb)


#----------------------------------------------------#
# TESTES > PEGA CONFIG DO PROJETO
#----------------------------------------------------#

class TesteConfigProjetoCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    X_(sublime.active_window().project_file_name())


#----------------------------------------------------#
# TESTES > ESCOPO
#----------------------------------------------------#

class TesteEscopoCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    vis = self.view
    X_(vis.scope_name(posCursor(vis)))
    X_(sys.version)


#----------------------------------------------------#
# TESTES > ESCOPO
#----------------------------------------------------#

class TesteNumerosCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    def testa(modo, tx):

      #tt = 'fff dddddd 123'

      #X_(pegaCor(tt))

      #v, t = (0, 0)

      #X_(v,t)

      #X_(pegaNumeros(tx, limite=1))
      # M = re.search(r'[.,]', tx)
      # return tx[:M.start(0)]

      #return str(M.start(0) + M.end(0))

      #X_(1 in (1,2))

      tt = 'ddd kkk'

      tt = '_' + pegaCor(tt) + '_'

      X_(type(tt))

    aplica( edit, vis=self.view, func=testa)