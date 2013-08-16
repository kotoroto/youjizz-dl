youjizz-dl
==========

Command-line video downloader for Youjizz.com

Installation
------------
You can either put the Python file in /usr/bin, or run it locally. Make sure that it's marked as an executable file (chmod +x youjizz-dl.py).
This application is made for Arch Linux, but it should work on Ubuntu and other distros, too. Just make sure you've got all the dependencies
installed.

Dependencies:
-------------
python2-mechanize  
python2-urllib2  
python2-colorama  

Usage
-----
youjizz-dl [OPTIONS] [URL]  

Available options:  
-a	save as acronym: e.g. 'a video about a man and a woman.flv' becomes 'avaamaaw.flv'  
-i	save as unique YouJizz video ID  
-r	save as a random number  
-n	save as normal video title, with dashes instead of spaces  
-s	secret-mode: precedes the title with a dot to hide the file ('atgsw.flv' --> '.atgsw.flv')  
-t	top-secret-mode: creates the hidden directory ./.bin if it doesn't already exist, and puts the downloaded video in that directory.
-h	print this help message  
  
FAQ  
---  
Q: Why create youjizz-dl? youtube-dl already is capable of downloading videos from YouJizz.com.  
A: Although youtube-dl is a great tool, it doesn't have a lot of options to protect your privacy. You'd have to script them yourself, whereas youjizz-dl 
enables you to change video titles to your likings by just putting the desired flag in the command.  
  
Q: Are you planning on adding support for more websites?  
A: I'm not planning this, as I'm solely using Youjizz. That said, if anyone else can branch youjizz-dl and add support for these websites, 
I'll gladly integrate it in the main branch. It would be great if this could be done in a modular way, just like youtube-dl does it.
