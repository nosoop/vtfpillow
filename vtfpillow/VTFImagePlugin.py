from PIL import Image, ImageFile
from io import BytesIO

import pyvtflib

def _accept(data):
	return data[:4] == b"VTF\0"

def _is_value_power_of_two(x):
	return x and not (x & x - 1)

class VTFImageFile(ImageFile.ImageFile):
	format = "VTF"
	format_description = "Valve Texture Format"
	
	def _open(self):
		self.fc = self.fp.read()
		self._decoder = pyvtflib.VTFLib()
		self._decoder.load_image_bytes(self.fc)
		
		self._size = self._decoder.image_width(), self._decoder.image_height()
		self.mode = self.rawmode = "RGBA"
		
		self.fp = BytesIO(self._decoder.image_as_rgba8888())
		self.tile = [
			("raw", (0, 0) + self._size, 0, self.mode)
		]

def _save(im, fp, filename, save_all = False):
	if im.mode not in {"RGBA"}:
		raise NotImplementedError("Only RGBA is supported.")
	
	if not all(_is_value_power_of_two(value) for value in im.size):
		raise ValueError("Image width / height must be a power of two")
	
	info = im.encoderinfo.copy()
	
	create_thumbnail = info.get('thumbnail', True)
	create_mipmaps = info.get('mipmaps', True)
	
	vtf = pyvtflib.VTFLib()
	vtf.create_image(
		im.width, im.height,
		img_format = pyvtflib.VTFImageFormat.IMAGE_FORMAT_DXT5,
		thumbnail = create_thumbnail, mipmaps = create_mipmaps
	)
	vtf.image_set_flags(
		pyvtflib.VTFImageFlag.TEXTUREFLAGS_CLAMPS | pyvtflib.VTFImageFlag.TEXTUREFLAGS_CLAMPT |
		pyvtflib.VTFImageFlag.TEXTUREFLAGS_NOLOD | pyvtflib.VTFImageFlag.TEXTUREFLAGS_NOMIP
	)
	
	if im.mode == "RGBA":
		vtf.image_from_rgba8888(data = im.tobytes())
	
	fp.write(vtf.save_image_bytes())
	
	vtf.destroy_image()

Image.register_open(VTFImageFile.format, VTFImageFile, _accept)
Image.register_save(VTFImageFile.format, _save)
Image.register_extension(VTFImageFile.format, ".vtf")
