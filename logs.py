"""
Eine Python-Bibliothek, welche importierbare Standard-Logger bereitstellt

Autor: Maximilian Janisch
"""
__all__ = ('mainlog',)

import logging


# region MainLog
# Variablen
debug_file = 'mainDebug.log'
warning_file = 'main.log'

# Formatter
formatter = logging.Formatter('{asctime} | {levelname:<8} | {name}: {message}', style='{',
                              datefmt='%d. %m. %Y / %H:%M:%S')

mainlog = logging.getLogger('MainLog')
mainlog.setLevel(logging.DEBUG)

# Handler 1
filehandler_debug = logging.FileHandler(debug_file)
filehandler_debug.setLevel(logging.DEBUG)
# Handler 2
filehandler_important = logging.FileHandler(warning_file)
filehandler_important.setLevel(logging.WARNING)

# Initialisiere Formatter
filehandler_debug.setFormatter(formatter)
filehandler_important.setFormatter(formatter)

while mainlog.handlers:  # verhindert doppelte Logs bei mehrfachem Import des Moduls
    mainlog.removeHandler(mainlog.handlers[0])

mainlog.addHandler(filehandler_debug)
mainlog.addHandler(filehandler_important)
# endregion MainLog
