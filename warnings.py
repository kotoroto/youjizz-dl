#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
from colorama import Fore, init, Style ## Deze installeren uit repo's

if os.name == 'posix':
    WAIT = 'sys.stdout.write(Style.BRIGHT + Fore.RESET + "[" + Fore.YELLOW + " WAIT " + Fore.RESET + "]" + Style.RESET_ALL + "\\b\\b\\b\\b\\b\\b\\b\\b")'
    OK =   'sys.stdout.write(Style.BRIGHT + Fore.RESET + "[" + Fore.GREEN  + "  OK  " + Fore.RESET + "]" + Style.RESET_ALL + "\\n")'
    FAIL = 'sys.stdout.write(Style.BRIGHT + Fore.RESET + "[" + Fore.RED    + " FAIL " + Fore.RESET + "]" + Style.RESET_ALL + "\\b\\b\\b\\b\\b\\b\\b\\b")'
    FAILPLUSREGEL = 'sys.stdout.write(Style.BRIGHT + Fore.RESET + "[" + Fore.RED    + " FAIL " + Fore.RESET + "]" + Style.RESET_ALL + "\\n")'
    ONLINE = 'sys.stdout.write(Style.BRIGHT + Fore.RESET + "[" + Fore.GREEN  + "ONLINE" + Fore.RESET + "]" + Style.RESET_ALL + "\\n")'
    OFFLINEPLUSREGEL = 'sys.stdout.write(Style.BRIGHT + Fore.RESET + "[" + Fore.RED    + "OFFLNE" + Fore.RESET + "]" + Style.RESET_ALL + "\\n")'
else:
    sys.exit()

def escapeKnopAlsAfsluiterInstellen(self):
    ## Snelkoppeling maken voor de Escape-knop
    escapeknop = QtGui.QShortcut(self)
    escapeknop.setKey("Esc")
    self.connect(escapeknop, QtCore.SIGNAL("activated()"), self.close)
