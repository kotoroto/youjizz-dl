#!/usr/bin/python2.7

import sys, os, urlgrabber, mechanize, re
import urlgrabber.progress
from bs4 import BeautifulSoup
from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

def escapeKnopAlsAfsluiterInstellen(self):
    ## Snelkoppeling maken voor de Escape-knop
    escapeknop = QtGui.QShortcut(self)
    escapeknop.setKey("Esc")
    self.connect(escapeknop, QtCore.SIGNAL("activated()"), self.close)

def vensterAanmaken():
    ve = Venster()
    ve.tekstvak.returnPressed.connect(lambda: downloaderAansturen(ve))
    ve.drukknop.clicked.connect(lambda: downloaderAansturen(ve))
    #normale_pagina_url = raw_input("Video-URL = ")
    

def downloaderAansturen(ve):
    normale_pagina_url = str(ve.tekstvak.text())
    ve.close()
    print "link = " + normale_pagina_url
    dl = Downloader(normale_pagina_url)
    dl.normale_pagina()
    dl.vind_videopagina()
    dl.vind_oorspronkelijke_video()
    dl.oorspronkelijke_video_downloaden()

class Venster(QtGui.QWidget):
    def __init__(self):
        super(Venster, self).__init__()
        
        self.label = QtGui.QLabel("Voer URL in")
        
        self.tekstvak = QtGui.QLineEdit()
                
        self.drukknop = QtGui.QPushButton("Downloaden")
        
        self.normale_pagina_url = self.tekstvak.text()
        
        #self.tekstvak.setPlaceholderText("Pagina-URL")

        ## Knoppen in een 'Box'-layout zetten
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.label)
        
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.tekstvak)
        hbox2.addWidget(self.drukknop)
                
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        
        self.setLayout(vbox)
        
        escapeKnopAlsAfsluiterInstellen(self)
        
        self.setWindowTitle("YJ-downloader")
        
        self.show()
        
    def Down(self):
        address = QUrl("http://stackoverflow.com") #URL from the remote file.
        self.manager.get(QNetworkRequest(address))
    def replyFinished(self, reply):
        self.connect(reply,SIGNAL("downloadProgress(int,int)"),self.progressBar, SLOT("setValue(int)"))
        self.reply = reply
        self.progressBar.setMaximum(reply.size())
        alltext = self.reply.readAll()

class Downloader():
    def __init__(self, normale_pagina_url):
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        self.normale_pagina_url = normale_pagina_url
       
    def normale_pagina(self):
        print "Gevonden URL is " + self.normale_pagina_url
        self.normale_pagina_bron = self.browser.open(self.normale_pagina_url).read()
        self.soup = BeautifulSoup(self.normale_pagina_bron)
        
        print "Paginabron geopend"
        #self.titel = re.findall("<title>*</title>", self.normale_pagina_bron)
        self.hakentitel = str(self.soup.html.head.title)
        self.titel = (re.sub("<[^<]+?>", "", self.hakentitel)).rstrip()
        self.opzoektitel = self.titel.replace(" ", "%20")
        self.opslaantitel = self.titel.replace(" ", "_") + ".mp4" 
        print "Opzoektitel is " + self.opzoektitel
        print "Opslaantitel is " + self.opslaantitel
        print "Opzoek-URL is " + "http://m.youjizz.com/search/" + self.opzoektitel + "/page1.html"
        #print self.normale_pagina_bron
        
    def vind_videopagina(self):
        self.videopagina_bron = self.browser.open("http://m.youjizz.com/search/" + self.opzoektitel + "/page1.html").read()
        #print(videopagina_bron)
    
    def vind_oorspronkelijke_video(self):
        self.oorspronkelijke_video_url = re.findall("http://cdn[0-9][a-z].youjizz.com/videos/.*", self.videopagina_bron)[1]
        print self.oorspronkelijke_video_url
        

    def oorspronkelijke_video_downloaden(self):
        urlgrabber.urlgrab(self.oorspronkelijke_video_url, self.opslaantitel, progress_obj=urlgrabber.progress.text_progress_meter())
    
app = QtGui.QApplication(sys.argv)
ex = vensterAanmaken()
sys.exit(app.exec_())


from PyQt4.QtCore import QUrl, QFileInfo, QFile, QIODevice
from PyQt4.QtGui import QApplication, QDialog, QProgressBar, QLabel, QPushButton, QDialogButtonBox, \
                    QVBoxLayout, QMessageBox
from PyQt4.QtNetwork import QHttp

url_to_download = 'http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.12.3.zip'

class Kjoetiedownloader(QDialog):
    def __init__(self, parent=None):
        super(Downloader, self).__init__(parent)

        self.httpGetId = 0
        self.httpRequestAborted = False
        self.statusLabel = QLabel('Downloading %s' % url_to_download)
        self.closeButton = QPushButton("Close")
        self.closeButton.setAutoDefault(False)
        self.progressBar = QProgressBar()

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.closeButton, QDialogButtonBox.RejectRole)

        self.http = QHttp(self)
        self.http.requestFinished.connect(self.httpRequestFinished)
        self.http.dataReadProgress.connect(self.updateDataReadProgress)
        self.http.responseHeaderReceived.connect(self.readResponseHeader)
        self.closeButton.clicked.connect(self.cancelDownload)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(self.progressBar)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle('Download Example')
        self.downloadFile()

    def downloadFile(self):
        url = QUrl(url_to_download)
        fileInfo = QFileInfo(url.path())
        fileName = fileInfo.fileName()

        if QFile.exists(fileName):
            QFile.remove(fileName)

        self.outFile = QFile(fileName)
        if not self.outFile.open(QIODevice.WriteOnly):
            QMessageBox.information(self, 'Error',
                    'Unable to save the file %s: %s.' % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        mode = QHttp.ConnectionModeHttp
        port = url.port()
        if port == -1:
            port = 0
        self.http.setHost(url.host(), mode, port)
        self.httpRequestAborted = False

        path = QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/")
        if path:
            path = str(path)
        else:
            path = '/'

        # Download the file.
        self.httpGetId = self.http.get(path, self.outFile)

    def cancelDownload(self):
        self.statusLabel.setText("Download canceled.")
        self.httpRequestAborted = True
        self.http.abort()
        self.close()

    def httpRequestFinished(self, requestId, error):
        if requestId != self.httpGetId:
            return

        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None
            return

        self.outFile.close()

        if error:
            self.outFile.remove()
            QMessageBox.information(self, 'Error',
                    'Download failed: %s.' % self.http.errorString())

        self.statusLabel.setText('Done')       

    def readResponseHeader(self, responseHeader):
        # Check for genuine error conditions.
        if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
            QMessageBox.information(self, 'Error',
                    'Download failed: %s.' % responseHeader.reasonPhrase())
            self.httpRequestAborted = True
            self.http.abort()

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return
        self.progressBar.setMaximum(totalBytes)
        self.progressBar.setValue(bytesRead)



