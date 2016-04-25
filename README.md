# FontTool
This tool takes a font file with the format .bcfnt, which can be generated using the CTR SDK, and converts it into a CIA installable onto a 3DS system

It requires 3dstool, ctrtool, and makerom to function.

In addition, it requires a decrypted CIA of the system font file.


## Installing
Drop the generated CIA into the /D9Game directory of your SD card and use Decrypt9 to encrypt NCCH

It can then be installed using any CIA manager

## Usage
See `FontTool.py -h`

## License / Credits
* `FontTool.py` is under the MIT license.
* All other tools (makerom, ctrtool, and 3dstool) are under their respective licenses

HUGE thanks to ihaveamac for making this possible