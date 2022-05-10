# VTFPillow

Plugin for Pillow to work with Valve Texture Format files.

Currently only supports importing the first frame / mipmap from VTF and exporting textures in
RGBA format.

[pyvtflib](https://github.com/lasa01/pyvtflib) does all of the heavy lifting here.

## Example Usage

```python
import PIL.Image
import vtfpillow.VTFImagePlugin

from vtfpillow.VTFImagePlugin import VTFTextureFlag as TextureFlag

# convert a VTF to PNG
with PIL.Image.open("test.vtf") as image:
	image.save("test.png")

# convert an image to VTF
# images require dimensions that are a power of two
with PIL.Image.open("default.png") as image:
	image.save(
		"test_export.vtf", thumbnail = False, mipmaps = False,
		texture_flags = TextureFlag.CLAMP_S | TextureFlag.CLAMP_T | TextureFlag.NO_LOD | TextureFlag.NO_MIP,
	)
```
