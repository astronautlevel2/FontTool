#!/usr/bin/env python2

# FontTool.py by Alex Taber and ihaveamac
# License: MIT License
# https://github.com/astronautlevel2/FontTool

import os
import sys
import argparse
import subprocess
import binascii

argParser = argparse.ArgumentParser()

argParser.add_argument('-font', action='store', dest='fontFile', help='The font file location', required=True)
argParser.add_argument('-output', action='store', dest='output',  help='Output location. Don\'t include file extension. Default is the name of the font file')
argParser.add_argument('-force', action='store_true', dest='force', help='Overwrite existing files if they exist')
argParser.add_argument('-xor', action='store_true', dest='xor', help='Encrypt NCCH if "0004009B00014002.Main.romfs.xorpad" exists')
argParser.add_argument('-nocleanup', action='store_false', dest='nocleanup', help='Do not delete temporary files')

args = argParser.parse_args()

fontFile = args.fontFile
output = args.output
force = args.force
xor = args.xor
docleanup = args.nocleanup

#Run a command and print the command running in case there's a failure
def runCmd(cmd):
	process = subprocess.Popen(cmd)
	process.wait()
	processoutput = process.communicate()[0]
	if process.returncode != 0:
		print(cmd)
		sys.exit(1)

#Clenup if docleanup is true (which it is by default)
def clean():
	if docleanup:
		os.remove("romfs/cbf_std.bcfnt.lz")
		os.rmdir("romfs/")
		os.remove(output + ".cfa")
		os.remove("romfs-mod.bin")
	sys.exit(1)

#If output is not specified, use the fontFile's name
if output is None:
	output = os.path.splitext(fontFile)[0]

#Check for the existence of fontFile
if not os.path.exists(fontFile):
	print("Font file does not exist!")
	sys.exit(1)

#Warning
print("Your warranty ends here! Make backups of your NAND before you install this!")

#Try to create romfs folder
try:
    os.makedirs("romfs")
except OSError:
    if not os.path.isdir("romfs"):
        raise
        
#Compress the font file using lz compressiong
runCmd(["3dstool", "-zvf", "%s" % fontFile, "--compress-type", "lzex", "--compress-out", "romfs/cbf_std.bcfnt.lz"])
#Build a modified romfs
runCmd(["3dstool", "-cvtf", "romfs", "romfs-mod.bin", "--romfs-dir", "romfs"])
#Build a cfa file using the modified romfs and ncchheader
cmds = ["3dstool", "-cvtf", "cfa", "%s.cfa" % output, "--header", "ncchheader.bin", "--romfs", "romfs-mod.bin"]
if xor:
	print('xor romfs')
	#Add xorpad encryption if xor is enabled
	cmds.extend(["--romfs-xor", "0004009B00014002.Main.romfs.xorpad"])
runCmd(cmds)

#Make cfa file the proper size
with open("%s.cfa" % output, "r+b") as fontcfa:
	if xor:
		fontcfa.seek(0x18F)
		fontcfa.write("\x00")
	# this is probably bad but I can't find a better method right now
	#print(hex(os.path.getsize("romfs-mod.bin")))
	romfssize = int(os.path.getsize("romfs-mod.bin") / 0x200)
	romfssize = format(romfssize, 'x').rjust(8, '0')
	print(romfssize)
	romfssize = binascii.unhexlify(romfssize)[::-1]
	fontcfa.seek(0x1B4)
	fontcfa.write(romfssize)

#Warn user before overwriting file
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

#Make the CIA
runCmd(["make_cia", "-v", "-o", "%s.cia" % output, "--content0=%s.cfa" % output,  "--index_0=0"])
if not xor:
	print("Encrypt NCCH using Decrypt9 before installing or it won't work!")
#Clean stuff up
clean()
