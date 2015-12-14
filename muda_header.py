
# <header class="title"><!-- !!! Colocar Seta !!! -->
#     <?php echo $this->render('botoes_acoes.phtml'); ?>
#     <h1 class="js-menu-area">
#       <?php echo $this->Texto->desnome ?>
#       <span class="seta cskin"></span>
#     </h1>
# </header>

import sublime, sublime_plugin, re, func.editor
def x(*args): func.editor.x(*args);


class mudaHeaderCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		vis = self.view
		tx = func.editor.pegaTextoTodo(vis)

		# Substituição
		tx = tx.replace('<!-- !! Colocar Seta !! -->','')
		tx = re.sub(
			r'<header class="title">(.*?)<h1>(.*?)</h1>(.*?)</header>',
			r'<header class="title">\1<h1 class="js-menu-area">\2<span class="seta cskin"></span></h1>\3</header>',
			tx, flags=re.DOTALL)

		tudo = sublime.Region(0,vis.size())
		vis.replace(edit,tudo,tx)
