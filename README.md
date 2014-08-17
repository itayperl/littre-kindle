littre-kindle
=============

This project aims to create a French-French dictionary for the Kindle. The
dictionary will be based on [XMLittre](http://www.littre.org) and [LeFFF](http://alpage.inria.fr/~sagot/lefff.html).

Dependencies
------------

- Kindlegen v2.8 (Linux version [here](http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_8.tar.gz)). The newer v2.9 hangs (at least on Linux).
- Python 2.7
- cURL

Kindle issues
-------------

I noticed the following issues while working on the dictionary. I have a Kindle
Paperwhite WiFi (B024) with FW version 5.4.4.2.

1. The Kindle can't handle identical inflections of different words. Only one
   entry is shown.
2. The Kindle can't handle uppercase inflections. Why on earth did they make it
   case-sensitive? The main entry can be in uppercase though, and will be found
   when searched lowercase/captialized.
