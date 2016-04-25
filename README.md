# FontTool
This tool takes a font file with the format .bcfnt, which can be generated using the CTR SDK, and converts it into a CIA installable onto a 3DS system

It requires 3dstool, ctrtool, and make_cia to function.


## Installing
Drop the generated CIA into the /D9Game directory of your SD card and use Decrypt9 to encrypt NCCH

**Back up your NAND before installing this! If something goes wrong you'll be bricked**

It's also kind of a pain to remove.

It can then be installed using any CIA manager

## Usage
See `FontTool.py -h`

## License / Credits
* `FontTool.py` is under the MIT license.
* All other tools (make_cia, ctrtool, and 3dstool) are under their respective licenses

HUGE thanks to ihaveamac for teaching me a lot of things and then bearing with my noob questions

Also thanks to everyone on the 3dshacks discord for helping me test
