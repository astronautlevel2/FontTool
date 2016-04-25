#!/usr/bin/env python2

# FontTool.py by Alex Taber
# License: MIT License
# https://github.com/astronautlevel2/FontTool

import os
import sys
import argparse
import subprocess

argParser = argparse.ArgumentParser()

argParser.add_argument('-font', action='store', dest='fontFile', help='The font file location', required=True)
argParser.add_argument('-output', action='store', dest='output',  help='Output location. Don\'t include file extension. Default is the name of the font file')
argParser.add_argument('-force', action='store_true', dest='force', help='Overwrite existing files if they exist')

args = argParser.parse_args()

fontFile = args.fontFile
output = args.output
force = args.force

def runCmd(cmd):
	process = subprocess.Popen(cmd)
	process.wait()
	processoutput = process.communicate()[0]
	if process.returncode != 0:
		print(cmd)
		sys.exit(1)

def clean():
	os.remove("romfs/cbf_std.bcfnt.lz")
	os.rmdir("romfs/")
	os.remove(output + ".cfa")
	os.remove("romfs-mod.bin")
	sys.exit(1)

if output is None:
	output = os.path.splitext(fontFile)[0]

if not os.path.exists(args.fontFile):
	print("Font file does not exist!")
	sys.exit(1)

raw_input("Your warranty ends here! Make backups of your NAND before you install this!")

runCmd(["3dstool", "-zvf", "%s" % fontFile, "--compress-type", "lzex", "--compress-out", "cbf_std.bcfnt.lz"])
os.mkdir("romfs")
os.rename("cbf_std.bcfnt.lz", "romfs/cbf_std.bcfnt.lz")
runCmd(["3dstool", "-cvtf", "romfs", "romfs-mod.bin", "--romfs-dir", "romfs"])
runCmd(["3dstool", "-cvtf", "cfa", "%s.cfa" % output, "--header", "ncchheader.bin", "--romfs", "romfs-mod.bin"])
if os.path.exists("%s.cia" % output) and not force:
	uinput = raw_input("Warning! Output CIA already exists! Continue? (y/n): ")
	if (uinput == "n"):
		print("Aborting")
		clean()
	elif (uinput == "y"):
		print("Continuing")
	else:
		print("Aborting due to invalid input")
		clean()

runCmd(["make_cia", "-v", "-o", "%s.cia" % output, "--content0=%s.cfa" % output,  "--index_0=0"])
clean()
