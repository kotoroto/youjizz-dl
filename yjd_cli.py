#!/usr/bin/python2.7

import sys, os, urlgrabber, mechanize, re
import urlgrabber.progress
import urllib2
import terminalwaarschuwingen as tw
from bs4 import BeautifulSoup
from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from colorama import Fore, init, Style ## Deze installeren uit repo's

def downloaderAansturen():
    dl = Downloader()
    dl.openEmbedpagina()
    dl.vind_oorspronkelijke_video()
    dl.oorspronkelijke_video_downloaden()

class Downloader():
    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        self.normale_pagina_url = str(sys.argv[1]) ## URL laden uit het ingetypte commando.
        self.videoid = re.search("[0-9]*[0-9]", self.normale_pagina_url).group()
        
        self.embedpagina_url = "http://www.youjizz.com/videos/embed/" + self.videoid
        
        self.paginatitel = re.sub("http://www.youjizz.com/videos/", "", self.normale_pagina_url)
        self.paginatitel = re.sub("-[0-9]*[0-9].html", "", self.paginatitel)
        self.opslaantitel = self.paginatitel + ".flv"
        
        
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
        
        #self.soup = BeautifulSoup(self.embedpagina_bron)
        
        #print self.embedpagina_bron
        
    def vind_oorspronkelijke_video(self):
        self.oorspronkelijke_video_url = re.findall("http://im.*.youjizz.com.*\"\\)\\)", self.embedpagina_bron)[0]
        self.oorspronkelijke_video_url = re.sub("\"\\)\\)", "", self.oorspronkelijke_video_url)
        
        #print self.oorspronkelijke_video_url
        
    def oorspronkelijke_video_downloaden(self):
        #urlgrabber.urlgrab(self.oorspronkelijke_video_url, self.opslaantitel, progress_obj=urlgrabber.progress.text_progress_meter())
        #urlgrabber.urlgrab(self.oorspronkelijke_video_url, self.opslaantitel, progress_obj=self.meter())
        
        u = urllib2.urlopen(self.oorspronkelijke_video_url)
        file_name = self.opslaantitel
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"[%3.0f%%]" % (file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
        
        #urllib.urlretrieve (self.oorspronkelijke_video_url, self.opslaantitel)
        
        #sys.stdout.write("\r%2d%%" % percent)
        #sys.stdout.flush()
        

downloaderAansturen()
