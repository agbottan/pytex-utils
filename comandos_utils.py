
#######################
# --- PYTEX UTILS --- #
#######################

# IMPORTS

import sublime, sublime_plugin, sys, re, os, subprocess, threading, multiprocessing

from pytex.editor.log_utils  import *
from pytex.escolhe_projeto   import projetos_config
from pytex.utils             import resolveModo
from pytex.editor.text_utils import aplica, pegaInfoModo
from pytex.css.css_expande   import cssExpande
from pytex.html.html         import htmlExpande


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
  def run(self, edit, alternativo):
    vis = self.view
    modo = resolveModo(pegaInfoModo(vis))
    aplica( edit, vis=self.view, func=comenta, modo=modo, argList={ 'alternativo': alternativo })


#----------------------------------------------------#
# MOSTRA NOME
#----------------------------------------------------#
class MostraNomeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    X_(self.view.file_name(), '-> Foi pro clipboard')
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

    # Projetos listados
    projetos = projetos_config

    # Nome do projeto
    arq_projeto_atual = self.window.project_file_name()

    if arq_projeto_atual != None:

      # Projeto aberto
      arq_projeto_atual = os.path.basename(arq_projeto_atual)

      # Retira projeto atual da lista
      projetos = list( filter( lambda proj: proj['arq'] != arq_projeto_atual, projetos_config ))

    # Nome no painel
    nomes = [ proj.get('tit') for proj in projetos ]

    # Processo
    def abreProjeto(pathProjeto, janelaAnterior):
      def dentroThread(_pathProjeto, _janelaAnterior):

        # Abre projeto por linha de comando
        proc = subprocess.Popen([ "subl", "--new-window", "--project", _pathProjeto ])
        
        # Espera a execução finalizar
        # proc.wait()

        # Fecha a janela anterior
        # _janelaAnterior.run_command('close_window')

        return

      thread = threading.Thread(
        target=dentroThread,
        args=(pathProjeto, janelaAnterior))

      thread.start()
      return thread

    def callbackMenu(ind = 0):
      if (ind == -1):
        return

      janelaAnterior = sublime.active_window()
      pathProjeto = "/home/andre/Projetos/ST-3/ST-3 Projetos/{0}".format(projetos[ind]['arq'])

      abreProjeto(pathProjeto, janelaAnterior)

    # Mostra painel
    self.window.show_quick_panel(
      items     = nomes,
      on_select = callbackMenu
    )