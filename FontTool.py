#!/usr/bin/env python2

# FontTool.py by Alex Taber
# License: MIT License
# https://github.com/astronautlevel2/FontTool

import sys
import os
import argparse
import subprocess

argParser = argparse.ArgumentParser()

argParser.add_argument('-font', action='store', dest='fontFile', help='The font file location')
argParser.add_argument('-output', action='store', dest='output', default="font-patch", help='Output location. Don\'t include file extension. Default is font-patch')
argParser.add_argument('-fontCIA', action='store', dest='fontCIA', default="0004009B00014002.cia", help='Decrypted font CIA location. Default assumes 0004009B00014002.cia')

args = argParser.parse_args()

fontFile = args.fontFile
output = args.output
fontCIA = args.fontCIA

def runCmd(cmd):
	process = subprocess.Popen(cmd)
	process.wait()
	processoutput = process.communicate()[0]
	if process.returncode != 0:
		print("An error occured somewhere in the script. I was running: " + cmd)

if (fontFile is not None):
	runCmd("3dstool -zvf " + fontFile + " --compress-type lzex --compress-out cbf_std.bcfnt.lz")
	runCmd("ctrtool --contents=contents " + fontCIA)
	runCmd("3dstool -xvtf cfa contents.0000.00000000 --header ncchheader.bin --romfs romfs.bin")
	runCmd("3dstool -xvtf romfs romfs.bin --romfs-dir romfs")
	os.remove("romfs/cbf_std.bcfnt.lz")
	os.rename("cbf_std.bcfnt.lz", "romfs/cbf_std.bcfnt.lz")
	runCmd("3dstool -cvtf romfs romfs-mod.bin --romfs-dir romfs")
	runCmd("3dstool -cvtf cfa " + output + ".cfa --header ncchheader.bin --romfs romfs-mod.bin")
	runCmd("makerom -f cia -content " + output + ".cfa:0")
	os.remove("romfs/cbf_std.bcfnt.lz")
	os.rmdir("romfs/")
	os.remove("contents.0000.00000000")
	os.remove(output + ".cfa")
	os.remove("ncchheader.bin")
	os.remove("romfs.bin")
	os.remove("romfs-mod.bin")
	
else:
	print("Make sure you have all the arguments!")
