# VTFPillow
# Copyright (C) 2022 nosoop
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later
# version.

import enum

from PIL import Image, ImageFile
from io import BytesIO

import pyvtflib

def _accept(data):
	return data[:4] == b"VTF\0"

def _is_value_power_of_two(x):
	return x and not (x & x - 1)

# flags are copied from pyvtflib in case we change out the dependency in the future
# we also take this opportunity to rename them so the enum names aren't redundant
_texfmt = pyvtflib.VTFImageFormat
class VTFTextureFormat(enum.IntEnum):
	RGBA8888 = _texfmt.IMAGE_FORMAT_RGBA8888
	ABGR8888 = _texfmt.IMAGE_FORMAT_ABGR8888
	RGB888 = _texfmt.IMAGE_FORMAT_RGB888
	BGR888 = _texfmt.IMAGE_FORMAT_BGR888
	RGB565 = _texfmt.IMAGE_FORMAT_RGB565
	I8 = _texfmt.IMAGE_FORMAT_I8
	IA88 = _texfmt.IMAGE_FORMAT_IA88
	P8 = _texfmt.IMAGE_FORMAT_P8
	A8 = _texfmt.IMAGE_FORMAT_A8
	RGB888_BLUESCREEN = _texfmt.IMAGE_FORMAT_RGB888_BLUESCREEN
	BGR888_BLUESCREEN = _texfmt.IMAGE_FORMAT_BGR888_BLUESCREEN
	ARGB8888 = _texfmt.IMAGE_FORMAT_ARGB8888
	BGRA8888 = _texfmt.IMAGE_FORMAT_BGRA8888
	DXT1 = _texfmt.IMAGE_FORMAT_DXT1
	DXT3 = _texfmt.IMAGE_FORMAT_DXT3
	DXT5 = _texfmt.IMAGE_FORMAT_DXT5
	BGRX8888 = _texfmt.IMAGE_FORMAT_BGRX8888
	BGR565 = _texfmt.IMAGE_FORMAT_BGR565
	BGRX5551 = _texfmt.IMAGE_FORMAT_BGRX5551
	BGRA4444 = _texfmt.IMAGE_FORMAT_BGRA4444
	DXT1_ONEBITALPHA = _texfmt.IMAGE_FORMAT_DXT1_ONEBITALPHA
	BGRA5551 = _texfmt.IMAGE_FORMAT_BGRA5551
	UV88 = _texfmt.IMAGE_FORMAT_UV88
	UVWQ8888 = _texfmt.IMAGE_FORMAT_UVWQ8888
	RGBA16161616F = _texfmt.IMAGE_FORMAT_RGBA16161616F
	RGBA16161616 = _texfmt.IMAGE_FORMAT_RGBA16161616
	UVLX8888 = _texfmt.IMAGE_FORMAT_UVLX8888
	R32F = _texfmt.IMAGE_FORMAT_R32F
	RGB323232F = _texfmt.IMAGE_FORMAT_RGB323232F
	RGBA32323232F = _texfmt.IMAGE_FORMAT_RGBA32323232F
	NV_DST16 = _texfmt.IMAGE_FORMAT_NV_DST16
	NV_DST24 = _texfmt.IMAGE_FORMAT_NV_DST24
	NV_INTZ = _texfmt.IMAGE_FORMAT_NV_INTZ
	NV_RAWZ = _texfmt.IMAGE_FORMAT_NV_RAWZ
	ATI_DST16 = _texfmt.IMAGE_FORMAT_ATI_DST16
	ATI_DST24 = _texfmt.IMAGE_FORMAT_ATI_DST24
	NV_NULL = _texfmt.IMAGE_FORMAT_NV_NULL
	ATI2N = _texfmt.IMAGE_FORMAT_ATI2N
	ATI1N = _texfmt.IMAGE_FORMAT_ATI1N
	NONE = _texfmt.IMAGE_FORMAT_NONE

_texflag = pyvtflib.VTFImageFlag
class VTFTextureFlag(enum.IntFlag):
	POINT_SAMPLE = _texflag.TEXTUREFLAGS_POINTSAMPLE
	TRILINEAR = _texflag.TEXTUREFLAGS_TRILINEAR
	CLAMP_S = _texflag.TEXTUREFLAGS_CLAMPS
	CLAMP_T = _texflag.TEXTUREFLAGS_CLAMPT
	ANISOTROPIC = _texflag.TEXTUREFLAGS_ANISOTROPIC
	HINT_DXT5 = _texflag.TEXTUREFLAGS_HINT_DXT5
	SRGB = _texflag.TEXTUREFLAGS_SRGB
	DEPRECATED_NOCOMPRESS = _texflag.TEXTUREFLAGS_DEPRECATED_NOCOMPRESS
	NORMAL = _texflag.TEXTUREFLAGS_NORMAL
	NO_MIP = _texflag.TEXTUREFLAGS_NOMIP
	NO_LOD = _texflag.TEXTUREFLAGS_NOLOD
	MINMIP = _texflag.TEXTUREFLAGS_MINMIP
	PROCEDURAL = _texflag.TEXTUREFLAGS_PROCEDURAL
	ONE_BIT_ALPHA = _texflag.TEXTUREFLAGS_ONEBITALPHA
	EIGHT_BIT_ALPHA = _texflag.TEXTUREFLAGS_EIGHTBITALPHA
	ENV_MAP = _texflag.TEXTUREFLAGS_ENVMAP
	RENDER_TARGET = _texflag.TEXTUREFLAGS_RENDERTARGET
	DEPTH_RENDER_TARGET = _texflag.TEXTUREFLAGS_DEPTHRENDERTARGET
	NO_DEBUG_OVERRIDE = _texflag.TEXTUREFLAGS_NODEBUGOVERRIDE
	SINGLE_COPY = _texflag.TEXTUREFLAGS_SINGLECOPY
	UNUSED_0 = _texflag.TEXTUREFLAGS_UNUSED0
	DEPRECATED_ONE_OVER_MIP_LEVEL_IN_ALPHA = _texflag.TEXTUREFLAGS_DEPRECATED_ONEOVERMIPLEVELINALPHA
	UNUSED_1 = _texflag.TEXTUREFLAGS_UNUSED1
	PRE_MULT_COLOR_BY_ONE_OVER_MIP_LEVEL = _texflag.TEXTUREFLAGS_DEPRECATED_PREMULTCOLORBYONEOVERMIPLEVEL
	UNUSED_2 = _texflag.TEXTUREFLAGS_UNUSED2
	NORMAL_TO_DUDV = _texflag.TEXTUREFLAGS_DEPRECATED_NORMALTODUDV
	UNUSED_3 = _texflag.TEXTUREFLAGS_UNUSED3
	ALPHA_TEST_MIP_GENERATION = _texflag.TEXTUREFLAGS_DEPRECATED_ALPHATESTMIPGENERATION
	NO_DEPTH_BUFFER = _texflag.TEXTUREFLAGS_NODEPTHBUFFER
	UNUSED_4 = _texflag.TEXTUREFLAGS_UNUSED4
	DEPRECATED_NICE_FILTERED = _texflag.TEXTUREFLAGS_DEPRECATED_NICEFILTERED
	CLAMP_U = _texflag.TEXTUREFLAGS_CLAMPU
	VERTEX_TEXTURE = _texflag.TEXTUREFLAGS_VERTEXTEXTURE
	SS_BUMP = _texflag.TEXTUREFLAGS_SSBUMP
	UNUSED_5 = _texflag.TEXTUREFLAGS_UNUSED5
	DEPRECATED_UNFILTERABLE_OK = _texflag.TEXTUREFLAGS_DEPRECATED_UNFILTERABLE_OK
	BORDER = _texflag.TEXTUREFLAGS_BORDER
	SPEC_VAR_RED = _texflag.TEXTUREFLAGS_DEPRECATED_SPECVAR_RED
	SPEC_VAR_ALPHA = _texflag.TEXTUREFLAGS_DEPRECATED_SPECVAR_ALPHA

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
	texture_format = info.get('texture_format', VTFTextureFormat.DXT5)
	texture_flags = info.get('texture_flags', 0)
	
	vtf = pyvtflib.VTFLib()
	vtf.create_image(
		im.width, im.height,
		img_format = texture_format, thumbnail = create_thumbnail, mipmaps = create_mipmaps
	)
	vtf.image_set_flags(texture_flags)
	
	if im.mode == "RGBA":
		vtf.image_from_rgba8888(data = im.tobytes())
	
	fp.write(vtf.save_image_bytes())
	
	vtf.destroy_image()

Image.register_open(VTFImageFile.format, VTFImageFile, _accept)
Image.register_save(VTFImageFile.format, _save)
Image.register_extension(VTFImageFile.format, ".vtf")
