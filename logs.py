"""
Eine Python-Bibliothek, welche importierbare Standard-Logger wie
"mainlog" bereitstellt. Zudem können benutzerdefinierte Logger mittels get_logger erstellt werden.

Autor: Maximilian Janisch
"""
__all__ = ('get_logger', 'mainlog')

import logging


def get_logger(name: str, formatter: logging.Formatter, debug_file: str, warning_file: str):
    """
    Hat als Output einen Logger mit Namen name, welcher entsprechend formatter wichtige Mitteilung in warning_file und
    "unwichtige" Mitteilungen in debug_file speichert.
    :param formatter: Formatter, nach welchem Log-Meldungen gespeichert werden
    :param name: Name des Loggers
    :param debug_file: Debug Meldungen werden hier gespeichert
    :param warning_file: Wichtige Meldungen werden hier gespeichert
    :return: Logger entsprechend den obigen Angaben
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Handler 1 (Debug)
    filehandler_debug = logging.FileHandler(debug_file)
    filehandler_debug.setLevel(logging.DEBUG)
    # Handler 2 (Wichtig)
    filehandler_important = logging.FileHandler(warning_file)
    filehandler_important.setLevel(logging.WARNING)

    # Initialisiere Formatter
    filehandler_debug.setFormatter(formatter)
    filehandler_important.setFormatter(formatter)

    while logger.handlers:  # verhindert doppelte Logs bei mehrfacher Erstellung eines Loggers
        logger.removeHandler(logger.handlers[0])

    logger.addHandler(filehandler_debug)
    logger.addHandler(filehandler_important)

    return logger


# Defaults
default_formatter = logging.Formatter('[{asctime}] | {levelname} | PID: {process} / File: {filename}, line {lineno}'
                                      ' | {name}: {message}', style='{', datefmt='%d. %m. %Y / %H:%M:%S')
mainlog = get_logger("MainLog", default_formatter, "mainDebug.log", "main.log")
