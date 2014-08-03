littre-kindle
=============

This project aims to create a French-French dictionary for the Kindle. The
dictionary will be based on [XMLittre](http://www.littre.org) and [LeFFF](http://alpage.inria.fr/~sagot/lefff.html).

Kindle issues
-------------

I noticed the following issues while working on the dictionary. I have a Kindle
Paperwhite WiFi (B024) with FW version 5.4.4.2.

1. The Kindle can't handle identical inflections of different words. Only one
   entry is shown.
2. The Kindle can't handle uppercase inflections. Why on earth did they make it
   case-sensitive? The main entry can be in uppercase though, and will be found
   when searched lowercase/captialized.
