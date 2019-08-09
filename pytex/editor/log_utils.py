
############### EDITOR FUNCTIONS ################

# Editor dependent functions
# Should be changed for portability between editors

import sublime, re

# --------------- Debug Log

class log:

    sep = ' '
    log_file = None 
    barra = '\n' + '-' * 40 + '\n'

    # Join Args
    def join(*args, sep = sep):
        return sep.join([str(a) for a in args])

    # Print
    def x(*args):
        print (log.join(*args))

    # Return
    def X(*args):
        return (log.join(*args))

    # Dialog
    def X_(*args):
        # sublime.message_dialog(log.join(*args))
        return ('SUBLIME ALERT => ' + log.join(*args))

    # Space line
    def x_(*args):
        print (log.join(*args), '\n')

    # Multiline
    def x__(*args):
        print (log.join(*args, sep = '\n'), log.barra)

    # !!! Fazer um que loga num arquivo de log aberto e abre se não tiver um