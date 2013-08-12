#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Dependencies:
# python2-requests, python2-mechanize,

import sys, os, urlgrabber, mechanize, re
import urllib2
import terminalwaarschuwingen as tw
import getopt
import random
from colorama import Fore, init, Style ## Deze installeren uit repo's
from time import gmtime, strftime

def downloaderAansturen():
    dl = Downloader()
    dl.titelAanmaken()
    dl.openEmbedpagina()
    dl.vind_oorspronkelijke_video()
    dl.oorspronkelijke_video_downloaden()

class Downloader():
    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        
    def titelAanmaken(self):
        
        titelopties, self.normale_pagina_url = getopt.getopt(sys.argv[1:], "nria")
        
        self.normale_pagina_url = self.normale_pagina_url[0]
        if re.search("http://www.youjizz.com/.*", self.normale_pagina_url) == None:
            print "Please only use YouJizz URLs starting with \'http://www.youjizz.com/\'."
            sys.exit()
            
        #print "titelopties is " + str(titelopties)
        #print "self.normale_pagina_url is " + self.normale_pagina_url
        
        self.videoid = re.search("[0-9]*[0-9]", self.normale_pagina_url).group()
        self.paginatitel = re.sub("http://www.youjizz.com/videos/", "", self.normale_pagina_url)
        self.paginatitel = re.sub("-[0-9]*[0-9].html", "", self.paginatitel)
        
        for titeloptie in titelopties:
            if titeloptie[0] == "-n":
                print "Will use normal title with dashes instead of spaces."
                self.opslaantitel = self.paginatitel + ".flv"
                
            elif titeloptie[0] == "-r":
                print "Will use random number"
                self.opslaantitel = str(random.randint(0,9999)) + ".flv"
                
            elif titeloptie[0] == "-i":
                print "Zal video-ID gebruiken"
                self.opslaantitel = self.videoid + ".flv"
            
            elif titeloptie[0] == "-a":
                print "Will use abbreviated title"
                self.paginatitel_met_spaties = self.paginatitel.replace("-", " ")
                
                self.paginatitel_eerste_letters = ""
                for woord in self.paginatitel_met_spaties.split():
                    eerste_letter = woord[0:1]
                    self.paginatitel_eerste_letters += eerste_letter
                
                self.opslaantitel = self.paginatitel_eerste_letters + ".flv"
            
            else:
                print "Will use normal title with dashes instead of spaces."
                self.opslaantitel = self.paginatitel + ".flv"
                
                
        print self.opslaantitel
        
        
        self.embedpagina_url = "http://www.youjizz.com/videos/embed/" + self.videoid
        
        
        
        #print titelopties
        #print self.normale_pagina_url
        
        
        
        
    def openEmbedpagina(self):
        sys.stdout.write("URL is........"),
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
        
    def vind_oorspronkelijke_video(self):
        self.oorspronkelijke_video_url = re.findall("http://im.*.youjizz.com.*\"\\)\\)", self.embedpagina_bron)[0]
        self.oorspronkelijke_video_url = re.sub("\"\\)\\)", "", self.oorspronkelijke_video_url)
        
        #print self.oorspronkelijke_video_url
        


    def oorspronkelijke_video_downloaden(self):
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
            #status = r"Downloading...[ %2.0f%%  ]" % (file_size_dl * 100. / file_size)
            status = r"Downloading..." + Style.BRIGHT + Fore.RESET + "[ " + Fore.GREEN + "%2.0f%%" % (file_size_dl * 100. / file_size) + Fore.RESET + "  ]" + Style.RESET_ALL 
            status = status + chr(8)*(len(status)+1)
            #print status,
            sys.stdout.write("\r" + status,)
            sys.stdout.flush

        f.close()
        sys.stdout.write("\r" + r"Downloading..." + Style.BRIGHT + Fore.RESET + "[  " + Fore.GREEN + "OK" + Fore.RESET + "   ]" + Style.RESET_ALL )
        sys.stdout.write("\n") # Zorgen dat de prompt weer gewoon op de volgende regel start.
        print "Download completed on",
        print(strftime("%Hh%M"))
        print "Size: %d MB" % (int(file_size/1048576)) ## divide by digit to convert bytes to MB.

downloaderAansturen()
