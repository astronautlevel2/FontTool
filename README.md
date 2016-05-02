# FontTool
This tool takes a font file with the format .bcfnt, which can be generated using the CTR SDK, and converts it into a CIA installable onto a 3DS system

It requires 3dstool, ctrtool, and make_cia to function.


## Installing

Encrypt the NCCH either using xorpad mode or by encrypting it in D9 using the Encrypt (NCCH) option.

**Back up your NAND before installing this! If something goes wrong you'll be bricked**

It can then be installed using any CIA manager

## Usage
See `FontTool.py -h`

## Examples
Build a CIA without xorpads and with the default output file (you'll have to encrypt NCCH):

```FontTool.py -font <FILE>.bcfnt```

Build a CIA with xorpads and a custom output file (no need to encrypt NCCH):

```FontTool.py -font <FILE>.bcfnt -xor -custom <OUTPUT>```

Build a CIA and don't cleanup files after:

```FontTool.py -font <FILE>.bcfnt -nocleanup```

## License / Credits
* `FontTool.py` is under the Smea license. See License.txt for details
* All other tools (make_cia, ctrtool, and 3dstool) are under their respective licenses

HUGE thanks to ihaveamac for teaching me a lot of things and then bearing with my noob questions

Also thanks to everyone on the 3dshacks discord for helping me test
