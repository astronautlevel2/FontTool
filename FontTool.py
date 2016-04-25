#!/usr/bin/env python2

# FontTool.py by Alex Taber
# License: MIT License
# https://github.com/astronautlevel2/FontTool

import os
import argparse
import subprocess

argParser = argparse.ArgumentParser()

argParser.add_argument('-font', action='store', dest='fontFile', help='The font file location', required=True)
argParser.add_argument('-output', action='store', dest='output',  help='Output location. Don\'t include file extension. Default is the name of the font file')

args = argParser.parse_args()

fontFile = args.fontFile
output = args.output

def runCmd(cmd):
	process = subprocess.Popen(cmd)
	process.wait()
	processoutput = process.communicate()[0]
	if process.returncode != 0:
		print("An error occured somewhere in the script. I was running: " + cmd)
		sys.exit()

if output is None:
	output = os.path.splitext(fontFile)[0]

runCmd(["3dstool", "-zvf", "%s" % fontFile, "--compress-type", "lzex", "--compress-out", "cbf_std.bcfnt.lz"])
os.mkdir("romfs")
os.rename("cbf_std.bcfnt.lz", "romfs/cbf_std.bcfnt.lz")
runCmd(["3dstool", "-cvtf", "romfs", "romfs-mod.bin", "--romfs-dir", "romfs"])
runCmd(["3dstool", "-cvtf", "cfa", "%s.cfa" % output, "--header", "ncchheader.bin", "--romfs", "romfs-mod.bin"])
runCmd(["makerom", "-f", "cia", "-content", "%s.cfa:0" % output])
os.remove("romfs/cbf_std.bcfnt.lz")
os.rmdir("romfs/")
os.remove(output + ".cfa")
os.remove("romfs-mod.bin")
