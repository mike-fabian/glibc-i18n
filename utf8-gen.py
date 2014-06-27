#!/usr/bin/python
# -*- coding: UTF-8 -i*-
# Copyright (C) 2014 Free Software Foundation, Inc.
# This file is part of the GNU C Library.
# Contributed by Pravin Satpute <psatpute@redhat.com>, 2014.
#
# The GNU C Library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# The GNU C Library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with the GNU C Library; if not, see
# <http://www.gnu.org/licenses/>.

import os
import sys		

def process_range(start, end, outfile, name):
#	print "start:", start
#	print "\nend:", end
	for i in range(int(start, 16), int(end, 16), 64 ):
		unihex = unichr(i).encode("UTF-8")
         	length_hex = len(unihex)
         	hexword = ""
         	for x in range(0, length_hex):
         		hexword =hexword + "/x" + ('%x' % ord(unihex[x]))
		if len(start) == 4:
			outfile.write("<U"+('%x' % i).upper()+">.." +  "<U"+('%x' % (i+63)).upper()+">     " + hexword + "         " + name.split(",")[0] + ">" + "\n")
		else:
			outfile.write("<U000"+('%x' % i).upper()+">.." +  "<U000"+('%x' % (i+63)).upper()+">     " + hexword + "         " + name.split(",")[0] + ">" + "\n")
		
		if i > (int(end, 16)-64):
			if len(start) == 4:
				outfile.write("<U"+('%x' % i).upper()+">.." +  "<U"+('%x' % int(end, 16)).upper()+">     " + hexword + "         " + name.split(",")[0] + ">" + "\n")
			else:
				outfile.write("<U000"+('%x' % i).upper()+">.." +  "<U000"+('%x' % int(end, 16)).upper()+">     " + hexword + "         " + name.split(",")[0] + ">" + "\n")

			break

#	print start
#	print end

def process_unidata(flines, outfile):
	l = 0
	while l < len(flines):
		w = flines[l].split(";")

		# Getting UTF8 of Unicode characters
                unihex = unichr(int(w[0],16)).encode("UTF-8")
		length_hex = len(unihex)
		hexword = ""
                for i in range(0, length_hex):
                      hexword =hexword + "/x" + ('%x' % ord(unihex[i]))

		# Some characters have <control> as a name, so using "Unicode 1.0 Name"  
		if w[1] == "<control>":
			if w[10] == "":
			#   4 characters U+0080, U+0081, U+0084 and U+0099 has "<control>" as a name and even no "Unicode 1.0 Name" (10th field) in UnicodeData.txt
			#   We can write code to take there alternate name from NameAliases.txt
				print "No alternate"
			else:
			       w[1] = w[10]

		# Handling case of CJK IDEAOGRAPH Start (3400) and End(4DB5), ADD 0x3F and create range. some more cases like this
		if w[1].find(", First>")!=-1:
			start = w[0]
			end = flines[l+1].split(";")[0]
			process_range(start, end, outfile, w[1])
			l = l +2
			continue

		if len(w[0]) == 4:
		    outfile.write("<U"+w[0]+">     " + hexword + "         " + w[1] + "\n")
		else:
		    outfile.write("<U000"+w[0]+">     " + hexword + "         " + w[1] + "\n")
		l = l +1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print  "USAGE: python utf8-gen.py UnicodeData.txt"
    else:
        unidata_file = open(sys.argv[1]) 
        outfile=open("UTF-8","w")
	flines = unidata_file.readlines()
	# Writing lines from existing UTF-8 to new UTF-8
        outfile.write("<code_set_name> UTF-8\n")
	outfile.write("<comment_char> %\n")
	outfile.write("<escape_char> /\n")
	outfile.write("<mb_cur_min> 1\n")
	outfile.write("<mb_cur_max> 6\n\n")
	# Processing UnicodeData.txt
	process_unidata(flines, outfile)

        outfile.close()
	unidata_file.close()
