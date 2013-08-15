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



