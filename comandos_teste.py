
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

import pytex.editor.log_utils

from pytex.editor.text_utils import *
from pytex.utils import *
from pytex.css import *
from pytex.html import *
from pytex.entities import *
from pytex.formata_linhas import *
from pytex.comentator import *
from pytex.escolhe_projeto import *
# from pytex.config.global_config import *

l = log_utils.log


# ============== CLASSES DOS COMANDOS ============== #

#----------------------------------------------------#
#   TESTES > CONFIG
#----------------------------------------------------#

class TesteConfigCommand(sublime_plugin.TextCommand):

  def teste(e):
    return e;

  # description = "Descrição Marota"

  def run(self, edit):
    l.X_(self.description)
    l.X_(pytex.global_config.ConfigGlobal)
    l.X_(sublime.active_window().project_data().get('projeto_config').get('tamanho'))


#----------------------------------------------------#
#   TESTES > COMMAND OVERLAY
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
#   TESTES > QUICK PANEL
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
#   TESTES > MENU INLINE
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
#   TESTES > PEGA CONFIG DO PROJETO
#----------------------------------------------------#

class TesteConfigProjetoCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    l.X_(sublime.active_window().project_file_name())
    l.X_(sublime.active_window().project_data().get('projeto_config').get('fruta'))
    l.X_(sublime.active_window().project_data().get('projeto_config').get('tamanho'))


#----------------------------------------------------#
#   TESTES > ESCOPO
#----------------------------------------------------#

class TesteEscopoCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    vis = self.view
    l.x(vis.scope_name(posCursor(vis)))