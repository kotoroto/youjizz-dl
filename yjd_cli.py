#!/usr/bin/python2.7

import sys, os, urlgrabber, mechanize, re
import urlgrabber.progress
import terminalwaarschuwingen as tw
from bs4 import BeautifulSoup
from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from colorama import Fore, init, Style ## Deze installeren uit repo's

## Te doen: Downloader sturen op de ID in de paginabron ipv via de titel te sturen. Zie website_hulp.html:



def downloaderAansturen():
    normale_pagina_url = str(sys.argv[1]) ## URL laden uit het ingetypte commando.
    videoid = re.search("[0-9]*[0-9]", normale_pagina_url).group()
    print videoid
    embedpagina_url = "http://www.youjizz.com/videos/embed/" + videoid
    print embedpagina_url
    paginatitel = re.sub("http://www.youjizz.com/videos/", "", normale_pagina_url)
    paginatitel = re.sub("-[0-9]*[0-9].html", "", paginatitel)
    print "Paginatitel is " + paginatitel
    opslaantitel = paginatitel + ".flv"
    print "Opslaantitel is " + opslaantitel
    dl = Downloader(embedpagina_url, opslaantitel)
    dl.openEmbedpagina()
    dl.vind_oorspronkelijke_video()
    dl.oorspronkelijke_video_downloaden()

class Downloader():
    def __init__(self, embedpagina_url, opslaantitel):
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        self.embedpagina_url = embedpagina_url
        self.opslaantitel = opslaantitel
        
    def openEmbedpagina(self):
        sys.stdout.write("URL is... "),
        exec(tw.WAIT)
        sys.stdout.flush()
        
        try:
            self.embedpagina_bron = self.browser.open(self.embedpagina_url).read()
            exec(tw.ONLINE)
            sys.stdout.flush()
            #print "URL online: " + self.embedpagina_url
        except mechanize._mechanize.BrowserStateError:
            exec(tw.OFFLINEPLUSREGEL)
            sys.stdout.flush()
            sys.exit()
        
        self.soup = BeautifulSoup(self.embedpagina_bron)
        
        print "Paginabron geopend"
        #print self.embedpagina_bron
        
    def vind_oorspronkelijke_video(self):
        self.oorspronkelijke_video_url = re.findall("http://im.*.youjizz.com.*\"\\)\\)", self.embedpagina_bron)[0]
        self.oorspronkelijke_video_url = re.sub("\"\\)\\)", "", self.oorspronkelijke_video_url)
        
        print self.oorspronkelijke_video_url
        
    def oorspronkelijke_video_downloaden(self):
        urlgrabber.urlgrab(self.oorspronkelijke_video_url, self.opslaantitel, progress_obj=urlgrabber.progress.text_progress_meter())

downloaderAansturen()
